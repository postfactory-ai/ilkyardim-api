import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cok-gizli-kurtulus-anahtari'
app.config['JSON_AS_ASCII'] = False

# DB BAĞLANTISI
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'giris_yap'

# --- MODELLER (SADE VE NET) ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Hata vermesin diye email sütununu tutuyoruz ama zorunlu değil
    email = db.Column(db.String(150), nullable=True)

class Konu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    icerik = db.Column(db.Text, nullable=True) 
    sira = db.Column(db.Integer, default=0)
    resim = db.Column(db.String(500), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ACİL DURUM BUTONU (BU SEFER KESİN ÇALIŞACAK) ---
@app.route('/acil-reset')
def reset_db():
    try:
        # Tabloları komple uçur
        db.drop_all()
        # Yeniden oluştur
        db.create_all()
        
        # Admini Elle Ekle
        # Şifre: 1234
        admin_pass = generate_password_hash('1234', method='pbkdf2:sha256')
        new_admin = User(username='admin', password=admin_pass, is_admin=True)
        
        db.session.add(new_admin)
        db.session.commit()
        
        return "<h1>✅ SİSTEM SIFIRLANDI!</h1><p>Veritabanı temizlendi, Admin oluşturuldu.</p><h2>Kullanıcı: admin<br>Şifre: 1234</h2><br><a href='/giris'>GİRİŞ YAP</a>"
    except Exception as e:
        return f"<h1>HATA OLDU:</h1> {str(e)}"

# --- ROTALAR ---
@app.route('/')
def index():
    try:
        konular = Konu.query.order_by(Konu.sira).all()
        return render_template('index.html', konular=konular)
    except:
        return "Veritabanı hatası! Lütfen /acil-reset adresine gidin."

@app.route('/giris', methods=['GET', 'POST'])
def giris_yap():
    if request.method == 'POST':
        kadi = request.form.get('username')
        sifre = request.form.get('password')
        
        user = User.query.filter_by(username=kadi).first()
        
        if user:
            if check_password_hash(user.password, sifre):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('Şifre Yanlış!', 'danger')
        else:
            flash('Kullanıcı Bulunamadı!', 'warning')
            
    return render_template('login.html')

@app.route('/yonetim')
@login_required
def yonetim_index():
    # Basit admin kontrolü
    if not current_user.is_admin and current_user.username != 'admin':
        return "Bu alana yetkiniz yok!"
    konular = Konu.query.order_by(Konu.sira).all()
    return render_template('admin/index.html', konular=konular)

# Diğer rotalar (Admin panelinin çalışması için gerekli)
@app.route('/yonetim/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def yonetim_duzenle(id):
    if not current_user.is_admin: return "Yetkisiz"
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

@app.route('/cikis')
@login_required
def cikis_yap():
    logout_user()
    return redirect(url_for('index'))

# Quiz ve Arama rotaları (Hata vermesin diye boş ekliyoruz, sonra doldururuz)
@app.route('/quiz')
def quiz_page(): return render_template('quiz.html')
@app.route('/arama')
def arama(): return render_template('arama.html')

if __name__ == '__main__':
    app.run(debug=True)
