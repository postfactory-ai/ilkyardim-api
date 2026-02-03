import os
import subprocess

print("\033[91m🚑 SİSTEM KURTARMA OPERASYONU BAŞLATILIYOR...\033[0m")

# EKSİKSİZ, SAĞLAM APP.PY
# Bu kodda "Try/Except" blokları artırıldı. Hata olsa bile site çökmez.
app_code = """import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from datetime import datetime
from dotenv import load_dotenv

load_dotenv() # .env varsa oku

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cok-gizli-anahtar-yedek')
app.config['JSON_AS_ASCII'] = False

# VERİTABANI BAĞLANTISI
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'giris_yap'

# --- GOOGLE AYARLARI (Hata verirse site çökmesin diye kontrol) ---
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

oauth = OAuth(app)
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    google = oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        access_token_url='https://accounts.google.com/o/oauth2/token',
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'},
    )
else:
    google = None # Ayarlar yoksa google objesi boş olsun

# --- MODELLER ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password = db.Column(db.String(250), nullable=True) # Hash uzun olabilir
    google_id = db.Column(db.String(200), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    # Profil Bilgileri
    acil_no_1 = db.Column(db.String(20), nullable=True)
    acil_no_2 = db.Column(db.String(20), nullable=True)

class Konu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    icerik = db.Column(db.Text, nullable=True) 
    sira = db.Column(db.Integer, default=0)
    resim = db.Column(db.String(500), nullable=True)

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
        return "Sistem Başlatılıyor... Lütfen /kurulum-yap adresine giderek veritabanını onarın."

# GİRİŞ YAP (DÜZELTİLDİ)
@app.route('/giris', methods=['GET', 'POST'])
def giris_yap():
    if request.method == 'POST':
        girdi = request.form.get('username')
        sifre = request.form.get('password')
        
        # Kullanıcı Adı VEYA Email ile ara
        user = User.query.filter((User.username == girdi) | (User.email == girdi)).first()
        
        if user:
            # Şifre kontrolü (Google kullanıcılarının şifresi None olabilir, hata vermesin)
            if user.password and check_password_hash(user.password, sifre):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Şifre hatalı!', 'danger')
        else:
            flash('Kullanıcı bulunamadı!', 'warning')
            
    return render_template('login.html')

# GOOGLE LOGIN (Hata Önleyici Mod)
@app.route('/login/google')
def google_login():
    if not google:
        return "Google Ayarları (Client ID/Secret) Vercel panelinde eksik! Lütfen ekleyin."
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def google_authorize():
    if not google: return "Hata: Google servisi aktif değil."
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()
        
        # Kullanıcı var mı?
        user = User.query.filter_by(google_id=user_info['id']).first()
        if not user:
            user = User.query.filter_by(email=user_info['email']).first()
            if user:
                user.google_id = user_info['id'] # Mevcut kullanıcıyı Google ile bağla
            else:
                # Yeni Kullanıcı
                user = User(
                    username=user_info['name'],
                    email=user_info['email'],
                    google_id=user_info['id'],
                    password=None # Şifresiz
                )
                db.session.add(user)
        
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Google Giriş Hatası: {str(e)}"

# KAYIT OL
@app.route('/kayit', methods=['GET', 'POST'])
def kayit_ol():
    if request.method == 'POST':
        kadi = request.form.get('username')
        email = request.form.get('email')
        sifre = request.form.get('password')
        
        if User.query.filter((User.username==kadi) | (User.email==email)).first():
            flash('Bu kullanıcı zaten var.', 'warning')
            return redirect(url_for('kayit_ol'))
        
        # Şifre Hashleme (Varsayılan yöntem)
        hashed_pw = generate_password_hash(sifre)
        yeni_user = User(username=kadi, email=email, password=hashed_pw)
        
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
        flash('Kaydedildi.', 'success')
    return render_template('profile.html', user=current_user)

# YÖNETİM (Admin Yetki Kontrolü)
@app.route('/yonetim')
@login_required
def yonetim_index():
    # Admin yetkisi kontrolü: is_admin True OLMALI veya kullanıcı adı 'admin' olmalı
    if not current_user.is_admin and current_user.username != 'admin':
        return render_template('index.html') # Yetkisizse anasayfaya at
    
    konular = Konu.query.order_by(Konu.sira).all()
    return render_template('admin/index.html', konular=konular)

@app.route('/yonetim/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def yonetim_duzenle(id):
    if not current_user.is_admin and current_user.username != 'admin': return "Yetkisiz"
    konu = Konu.query.get_or_404(id)
    if request.method == 'POST':
        konu.baslik = request.form['baslik']
        konu.icerik = request.form['icerik']
        konu.resim = request.form['resim']
        db.session.commit()
        return redirect(url_for('yonetim_index'))
    return render_template('admin/duzenle.html', konu=konu)

@app.route('/arama')
def arama():
    kelime = request.args.get('q', '')
    sonuclar = []
    if kelime:
        sonuclar = Konu.query.filter(or_(Konu.baslik.ilike(f'%{kelime}%'), Konu.icerik.ilike(f'%{kelime}%'))).all()
    return render_template('arama.html', kelime=kelime, sonuclar=sonuclar)

@app.route('/quiz')
def quiz_page():
    return render_template('quiz.html')

@app.route('/konu/<int:id>')
def konu_detay(id):
    konu = Konu.query.get_or_404(id)
    return render_template('detay.html', konu=konu)

# --- HAYAT KURTARAN KURULUM ROTASI ---
@app.route('/kurulum-yap')
def kurulum():
    with app.app_context():
        db.create_all()
        
        # Admin Kontrolü ve ONARIMI
        admin = User.query.filter_by(username='admin').first()
        if admin:
            # Admin varsa şifresini 1234 olarak GÜNCELLE (Bozuksa düzelir)
            admin.password = generate_password_hash('1234')
            admin.is_admin = True
            db.session.commit()
            durum = "Admin şifresi '1234' olarak SIFIRLANDI."
        else:
            # Admin yoksa YARAT
            yeni_admin = User(
                username='admin', 
                email='admin@sistem.com', 
                password=generate_password_hash('1234'), 
                is_admin=True
            )
            db.session.add(yeni_admin)
            db.session.commit()
            durum = "Admin kullanıcısı OLUŞTURULDU (admin / 1234)."
            
    return f"Sistem Onarıldı! <br> {durum} <br><br> <a href='/giris'>Giriş Yap</a>"

if __name__ == '__main__':
    app.run(debug=True)
"""

with open(os.path.join(os.getcwd(), 'app.py'), 'w', encoding='utf-8') as f:
    f.write(app_code)

print("\n🚀 TAMİR EDİLEN KODLAR GITHUB'A YOLLANIYOR...")
subprocess.run("git add app.py", shell=True)
subprocess.run('git commit -m "HOTFIX: Admin Girisi Kurtarildi & Sistem Stabilize Edildi"', shell=True)
subprocess.run("git push", shell=True)

print("\n✅ İŞLEM TAMAM! ŞİMDİ ŞUNU YAP:")
print("1. Vercel'in güncellemesini bekle (1-2 dk).")
print("2. Siteye gir ve şu adrese git: https://ilkyardim-api.vercel.app/kurulum-yap")
print("3. Ekranda 'Admin şifresi SIFIRLANDI' yazısını gör.")
print("4. Sonra 'Giriş' sayfasına git ve admin / 1234 ile gir.")