import os
import subprocess
import psycopg2

# ==========================================================
# BURAYA NEON DB KODUNU YAPIŞTIR
DATABASE_URL = "postgresql://neondb_owner:npg_OAFxzgdw76ta@ep-long-brook-agzcx4dh-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" 
# ==========================================================

print("\033[96m📧 ÜYELİK SİSTEMİ GÜNCELLENİYOR (GMAIL + EMAIL)...\033[0m")

# 1. KÜTÜPHANE EKLEME (Authlib gerekli)
req_path = os.path.join(os.getcwd(), 'requirements.txt')
with open(req_path, 'a') as f:
    f.write("\nauthlib\nrequests")
print("✅ Gerekli kütüphaneler listeye eklendi.")

# 2. VERİTABANI GÜNCELLEME (Sütun Ekleme)
# Kullanıcı tablosuna 'email' ve 'google_id' eklememiz lazım yoksa hata verir.
def db_guncelle():
    print("⏳ Veritabanı tabloları güncelleniyor...")
    url = DATABASE_URL.replace("postgres://", "postgresql://") if "postgres://" in DATABASE_URL else DATABASE_URL
    try:
        conn = psycopg2.connect(url)
        cursor = conn.cursor()
        
        # Eğer sütun yoksa ekle (Hata vermesin diye try-catch bloğu gibi ALTER kullanıyoruz)
        komutlar = [
            "ALTER TABLE user ADD COLUMN IF NOT EXISTS email VARCHAR(150) UNIQUE;",
            "ALTER TABLE user ADD COLUMN IF NOT EXISTS google_id VARCHAR(200) UNIQUE;",
            "ALTER TABLE user ADD COLUMN IF NOT EXISTS avatar VARCHAR(500);"
        ]
        
        for komut in komutlar:
            try:
                cursor.execute(komut)
                conn.commit()
            except:
                conn.rollback() # Zaten varsa pas geç
                
        print("✅ Veritabanı sütunları (email, google_id) hazır.")
        conn.close()
    except Exception as e:
        print(f"⚠️ Veritabanı uyarısı: {e}")

db_guncelle()

# 3. APP.PY (GOOGLE LOGIN ENTEGRASYONU)
app_code = """import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli-anahtar-999'
app.config['JSON_AS_ASCII'] = False

# DB AYARI
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'giris_yap'

# --- GOOGLE OAUTH AYARLARI ---
# KANKA DİKKAT: Bu bilgileri Google Cloud Console'dan alıp buraya veya Vercel Environment Variables'a yazman lazım.
# Şimdilik boş bırakıyorum, çalışmazsa normal login çalışmaya devam eder.
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID', 'BURAYA_GOOGLE_CLIENT_ID_GELECEK')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET', 'BURAYA_GOOGLE_SECRET_GELECEK')

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

# --- MODELLER ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=True) # Google ile gelirse username başta olmayabilir
    email = db.Column(db.String(150), unique=True, nullable=True) # Yeni Eklendi
    password = db.Column(db.String(200), nullable=True) # Google ile girenlerin şifresi olmaz
    google_id = db.Column(db.String(200), unique=True, nullable=True) # Google ID
    avatar = db.Column(db.String(500), nullable=True) # Profil resmi
    is_admin = db.Column(db.Boolean, default=False)
    acil_no_1 = db.Column(db.String(20), nullable=True)
    acil_no_2 = db.Column(db.String(20), nullable=True)

class Konu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    icerik = db.Column(db.Text, nullable=True) 
    sira = db.Column(db.Integer, default=0)
    resim = db.Column(db.String(500), nullable=True)
    eklenme_tarihi = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROTALAR ---

@app.route('/')
def index():
    try:
        konular = Konu.query.order_by(Konu.sira).all()
        return render_template('index.html', konular=konular)
    except:
        return "Sistem Yükleniyor... Lütfen bekleyin."

# NORMAL GİRİŞ
@app.route('/giris', methods=['GET', 'POST'])
def giris_yap():
    if request.method == 'POST':
        email_or_user = request.form.get('username') # Artık hem mail hem kullanıcı adı olabilir
        sifre = request.form.get('password')
        
        # Hem username hem email alanında ara
        user = User.query.filter(or_(User.username==email_or_user, User.email==email_or_user)).first()
        
        if user and user.password and check_password_hash(user.password, sifre):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Hatalı bilgiler veya bu hesap Google ile oluşturulmuş.', 'danger')
    return render_template('login.html')

# GOOGLE İLE GİRİŞ BAŞLAT
@app.route('/login/google')
def google_login():
    try:
        redirect_uri = url_for('google_authorize', _external=True)
        return google.authorize_redirect(redirect_uri)
    except:
        return "Google API Anahtarları Eksik! (Vercel Ayarlarını Kontrol Et)"

# GOOGLE DÖNÜŞÜ (CALLBACK)
@app.route('/authorize/google')
def google_authorize():
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()
        
        # Bu Google ID ile kullanıcı var mı?
        user = User.query.filter_by(google_id=user_info['id']).first()
        
        if not user:
            # Yoksa, Email ile var mı? (Varsa birleştirelim)
            user = User.query.filter_by(email=user_info['email']).first()
            
            if user:
                # Emaili varmış, Google ID'sini ekleyelim
                user.google_id = user_info['id']
                user.avatar = user_info['picture']
            else:
                # Hiç yok, yeni kayıt açalım
                user = User(
                    username=user_info['name'],
                    email=user_info['email'],
                    google_id=user_info['id'],
                    avatar=user_info['picture'],
                    password=None # Şifre yok
                )
                db.session.add(user)
        
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
        
    except Exception as e:
        return f"Google Giriş Hatası: {e}"

@app.route('/kayit', methods=['GET', 'POST'])
def kayit_ol():
    if request.method == 'POST':
        kadi = request.form.get('username')
        email = request.form.get('email')
        sifre = request.form.get('password')
        
        if User.query.filter((User.username==kadi) | (User.email==email)).first():
            flash('Bu kullanıcı adı veya e-posta zaten kullanımda.', 'warning')
            return redirect(url_for('kayit_ol'))
            
        yeni_user = User(username=kadi, email=email, password=generate_password_hash(sifre, method='pbkdf2:sha256'))
        db.session.add(yeni_user)
        db.session.commit()
        login_user(yeni_user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/cikis')
@login_required
def cikis_yap():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    if request.method == 'POST':
        current_user.acil_no_1 = request.form.get('no1')
        current_user.acil_no_2 = request.form.get('no2')
        db.session.commit()
        flash('Bilgiler güncellendi.', 'success')
    return render_template('profile.html', user=current_user)

# ARAMA
@app.route('/arama')
def arama():
    kelime = request.args.get('q', '')
    if kelime:
        sonuclar = Konu.query.filter(or_(Konu.baslik.ilike(f'%{kelime}%'), Konu.icerik.ilike(f'%{kelime}%'))).all()
    else:
        sonuclar = []
    return render_template('arama.html', kelime=kelime, sonuclar=sonuclar)

# QUIZ
@app.route('/quiz')
def quiz_page():
    return render_template('quiz.html')

# YÖNETİM
@app.route('/yonetim')
@login_required
def yonetim_index():
    if not current_user.is_admin and current_user.username != 'admin': return "Yetkisiz Alan"
    konular = Konu.query.order_by(Konu.sira).all()
    return render_template('admin/index.html', konular=konular)

@app.route('/yonetim/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def yonetim_duzenle(id):
    if not current_user.is_admin and current_user.username != 'admin': return "Yetkisiz Alan"
    konu = Konu.query.get_or_404(id)
    if request.method == 'POST':
        konu.baslik = request.form['baslik']
        konu.icerik = request.form['icerik']
        konu.resim = request.form['resim']
        db.session.commit()
        return redirect(url_for('yonetim_index'))
    return render_template('admin/duzenle.html', konu=konu)

@app.route('/konu/<int:id>')
def konu_detay(id):
    konu = Konu.query.get_or_404(id)
    return render_template('detay.html', konu=konu)

@app.route('/kurulum-yap')
def kurulum():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@ilkyardim.com', password=generate_password_hash('1234', method='pbkdf2:sha256'), is_admin=True)
        db.session.add(admin)
        db.session.commit()
    return "DB Güncellendi."

# API
@app.route('/api/konular', methods=['GET'])
def api_konular():
    konular = Konu.query.order_by(Konu.sira).all()
    data = [{'id': k.id, 'baslik': k.baslik, 'resim': k.resim, 'sira': k.sira} for k in konular]
    return jsonify(data)

@app.route('/api/konu/<int:id>', methods=['GET'])
def api_detay(id):
    k = Konu.query.get_or_404(id)
    return jsonify({'id': k.id, 'baslik': k.baslik, 'icerik': k.icerik, 'resim': k.resim})

if __name__ == '__main__':
    app.run(debug=True)
"""
with open(os.path.join(os.getcwd(), 'app.py'), 'w', encoding='utf-8') as f:
    f.write(app_code)


# 4. LOGIN.HTML (GOOGLE BUTONU EKLE)
login_html = """
{% extends "layout.html" %}
{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card border-0 shadow-lg p-4 rounded-4">
                <h2 class="fw-bold mb-4 text-center">Giriş Yap</h2>
                
                <a href="/login/google" class="btn btn-outline-dark w-100 py-2 mb-3 fw-bold d-flex align-items-center justify-content-center gap-2">
                    <img src="https://www.svgrepo.com/show/475656/google-color.svg" width="20" height="20">
                    Google ile Devam Et
                </a>
                
                <div class="text-center text-muted mb-3 small">VEYA E-POSTA İLE</div>
                
                <form method="POST">
                    <div class="mb-3">
                        <label class="fw-bold small text-muted">Kullanıcı Adı veya E-Posta</label>
                        <input type="text" name="username" class="form-control form-control-lg bg-light border-0" required>
                    </div>
                    <div class="mb-3">
                        <label class="fw-bold small text-muted">Şifre</label>
                        <input type="password" name="password" class="form-control form-control-lg bg-light border-0" required>
                    </div>
                    <button class="btn btn-danger w-100 py-2 fw-bold rounded-3">Giriş Yap</button>
                </form>
                <div class="mt-4 text-center">
                    <a href="/kayit" class="text-muted text-decoration-none">Hesabın yok mu? <span class="fw-bold text-dark">Kayıt Ol</span></a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(os.getcwd(), 'templates', 'login.html'), 'w', encoding='utf-8') as f:
    f.write(login_html)


# 5. REGISTER.HTML (EMAIL ALANI EKLE)
register_html = """
{% extends "layout.html" %}
{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card border-0 shadow-lg p-4 rounded-4">
                <h2 class="fw-bold mb-4 text-center">Kayıt Ol</h2>
                
                <a href="/login/google" class="btn btn-outline-dark w-100 py-2 mb-3 fw-bold d-flex align-items-center justify-content-center gap-2">
                    <img src="https://www.svgrepo.com/show/475656/google-color.svg" width="20" height="20">
                    Google ile Kayıt Ol
                </a>
                
                <div class="text-center text-muted mb-3 small">VEYA FORM DOLDUR</div>

                <form method="POST">
                    <div class="mb-3">
                        <label class="fw-bold small text-muted">Kullanıcı Adı</label>
                        <input type="text" name="username" class="form-control form-control-lg bg-light border-0" required>
                    </div>
                    <div class="mb-3">
                        <label class="fw-bold small text-muted">E-Posta Adresi</label>
                        <input type="email" name="email" class="form-control form-control-lg bg-light border-0" required>
                    </div>
                    <div class="mb-3">
                        <label class="fw-bold small text-muted">Şifre</label>
                        <input type="password" name="password" class="form-control form-control-lg bg-light border-0" required>
                    </div>
                    <button class="btn btn-dark w-100 py-2 fw-bold rounded-3">Hesap Oluştur</button>
                </form>
                 <div class="mt-4 text-center">
                    <a href="/giris" class="text-muted text-decoration-none">Zaten üye misin? <span class="fw-bold text-dark">Giriş Yap</span></a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(os.getcwd(), 'templates', 'register.html'), 'w', encoding='utf-8') as f:
    f.write(register_html)

# GIT GÖNDERİMİ
print("\n🚀 GITHUB'A YOLLANIYOR (GMAIL + EMAIL DB)...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "FEATURE: Gmail Login ve Email Kayit Sistemi"', shell=True)
subprocess.run("git push", shell=True)
print("✅ Kodlar gönderildi! Şimdi Google API Key alman lazım.")