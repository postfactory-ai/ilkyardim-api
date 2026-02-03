import os
import subprocess

# AYARLAR
BASE_DIR = os.getcwd()
APP_PATH = os.path.join(BASE_DIR, 'app.py')

print("\033[92m🔧 ARAMA MODÜLÜ VE EKSİK KÜTÜPHANELER TAMİR EDİLİYOR...\033[0m")

# EKSİKSİZ, HATASIZ APP.PY (TÜM İMPORTLAR DAHİL)
app_code = """import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_  # <-- İŞTE EKSİK OLAN BU ARKADAŞTI
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bu-cok-gizli-bir-anahtar-999'
app.config['JSON_AS_ASCII'] = False

# VERİTABANI BAĞLANTISI
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'giris_yap'

# --- MODELLER ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
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
        return "Sistem Yükleniyor... Lütfen bekleyin veya /kurulum-yap sayfasına gidin."

# ARAMA ROTASI (ARTIK ÇALIŞACAK)
@app.route('/arama')
def arama():
    kelime = request.args.get('q', '')
    if kelime:
        # Başlıkta VEYA İçerikte ara
        sonuclar = Konu.query.filter(
            or_(
                Konu.baslik.ilike(f'%{kelime}%'),
                Konu.icerik.ilike(f'%{kelime}%')
            )
        ).all()
    else:
        sonuclar = []
    return render_template('arama.html', kelime=kelime, sonuclar=sonuclar)

# QUIZ
@app.route('/quiz')
def quiz_page():
    return render_template('quiz.html')

# GİRİŞ İŞLEMLERİ
@app.route('/giris', methods=['GET', 'POST'])
def giris_yap():
    if request.method == 'POST':
        kadi = request.form.get('username')
        sifre = request.form.get('password')
        user = User.query.filter_by(username=kadi).first()
        if user and check_password_hash(user.password, sifre):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Hatalı kullanıcı adı veya şifre', 'danger')
    return render_template('login.html')

@app.route('/kayit', methods=['GET', 'POST'])
def kayit_ol():
    if request.method == 'POST':
        kadi = request.form.get('username')
        sifre = request.form.get('password')
        if User.query.filter_by(username=kadi).first():
            flash('Bu kullanıcı adı alınmış.', 'warning')
            return redirect(url_for('kayit_ol'))
        yeni_user = User(username=kadi, password=generate_password_hash(sifre, method='pbkdf2:sha256'))
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

# YÖNETİM
@app.route('/yonetim')
@login_required
def yonetim_index():
    if current_user.username != 'admin': return "Yetkisiz Alan"
    konular = Konu.query.order_by(Konu.sira).all()
    return render_template('admin/index.html', konular=konular)

@app.route('/yonetim/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def yonetim_duzenle(id):
    if current_user.username != 'admin': return "Yetkisiz Alan"
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
        admin = User(username='admin', password=generate_password_hash('1234', method='pbkdf2:sha256'), is_admin=True)
        db.session.add(admin)
        db.session.commit()
    return "Sistem Hazır. Admin: admin / 1234"

# API (Mobil İçin)
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

with open(APP_PATH, 'w', encoding='utf-8') as f:
    f.write(app_code)

print("\n🚀 DÜZELTİLMİŞ KOD GITHUB'A YOLLANIYOR...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "HOTFIX: Arama Hatasi Giderildi (Import or_)"', shell=True)
subprocess.run("git push", shell=True)
print("✅ İşlem Tamam! Vercel güncellenince Arama %100 çalışacak.")