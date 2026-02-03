import os
import subprocess

# AYARLAR
BASE_DIR = os.getcwd()
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

print("\033[93m🚧 SİSTEM GÜNCELLEMESİ: UI TEMİZLİĞİ + ÜYELİK SİSTEMİ + ACİL BUTONLAR...\033[0m")

# 1. REQUIREMENTS.TXT (Flask-Login Ekliyoruz)
req_path = os.path.join(BASE_DIR, 'requirements.txt')
with open(req_path, 'r') as f:
    content = f.read()
if "Flask-Login" not in content:
    with open(req_path, 'a') as f:
        f.write("\nFlask-Login\nWerkzeug")
    print("✅ Flask-Login kütüphanesi eklendi.")


# 2. APP.PY (Kullanıcı Tablosu ve Login Mantığı Eklendi)
app_code = """import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bu-cok-gizli-bir-anahtar-999'
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

# --- MODELLER ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Acil Durum Kişileri (JSON formatında veya virgülle ayrılmış tutabiliriz şimdilik basit olsun)
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
        return "Sistem Hazırlanıyor... Lütfen /kurulum-yap adresine gidin."

# GİRİŞ SİSTEMİ
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
        
        # Kullanıcı var mı?
        if User.query.filter_by(username=kadi).first():
            flash('Bu kullanıcı adı zaten alınmış.', 'warning')
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

# PROFİL VE ACİL NO EKLEME
@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    if request.method == 'POST':
        current_user.acil_no_1 = request.form.get('no1')
        current_user.acil_no_2 = request.form.get('no2')
        db.session.commit()
        flash('Acil durum kişileri güncellendi.', 'success')
    return render_template('profile.html', user=current_user)

# YÖNETİM (SADECE ADMIN)
@app.route('/yonetim')
@login_required
def yonetim_index():
    if not current_user.username == 'admin': # Basit admin kontrolü
        return "Bu sayfaya yetkiniz yok."
    konular = Konu.query.order_by(Konu.sira).all()
    return render_template('admin/index.html', konular=konular)

@app.route('/yonetim/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def yonetim_duzenle(id):
    if not current_user.username == 'admin': return "Yetkisiz Erişim"
    konu = Konu.query.get_or_404(id)
    if request.method == 'POST':
        konu.baslik = request.form['baslik']
        konu.icerik = request.form['icerik']
        konu.resim = request.form['resim']
        db.session.commit()
        return redirect(url_for('yonetim_index'))
    return render_template('admin/duzenle.html', konu=konu)

# DETAY
@app.route('/konu/<int:id>')
def konu_detay(id):
    konu = Konu.query.get_or_404(id)
    return render_template('detay.html', konu=konu)

# KURULUM (DB GÜNCELLEME)
@app.route('/kurulum-yap')
def kurulum():
    db.create_all()
    # Varsayılan Admin Oluştur
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password=generate_password_hash('1234', method='pbkdf2:sha256'), is_admin=True)
        db.session.add(admin)
        db.session.commit()
    return "Tablolar ve Admin (admin/1234) oluşturuldu."

if __name__ == '__main__':
    app.run(debug=True)
"""
with open(os.path.join(BASE_DIR, 'app.py'), 'w', encoding='utf-8') as f:
    f.write(app_code)


# 3. LAYOUT.HTML (Live Search Bar ve Profil Menüsü)
layout_code = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acil Asistanı</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Outfit', sans-serif; background-color: #f8fafc; color: #1e293b; padding-bottom: 80px; }
        
        /* Alt Navigasyon (Mobil App Havası) */
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%;
            background: white; border-top: 1px solid #e2e8f0;
            display: flex; justify-content: space-around; padding: 10px 0;
            z-index: 1000; box-shadow: 0 -5px 20px rgba(0,0,0,0.05);
        }
        .nav-item-m { text-align: center; color: #64748b; text-decoration: none; font-size: 0.75rem; flex: 1; }
        .nav-item-m i { display: block; font-size: 1.5rem; margin-bottom: 2px; }
        .nav-item-m.active { color: #ef4444; }
        
        /* Arama Çubuğu */
        .search-container {
            position: sticky; top: 0; z-index: 900;
            background: rgba(255,255,255,0.9); backdrop-filter: blur(5px);
            padding: 10px 20px; border-bottom: 1px solid #eee;
        }
        .search-input {
            border-radius: 20px; border: 1px solid #e2e8f0; padding: 10px 20px;
            width: 100%; background: #f1f5f9; outline: none; transition: 0.3s;
        }
        .search-input:focus { background: white; border-color: #ef4444; box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1); }
    </style>
</head>
<body>
    
    <div class="search-container">
        <div class="container d-flex align-items-center gap-3">
            <input type="text" id="liveSearch" class="search-input" placeholder="Ne arıyorsun? (Yanık, Kırık, Kalp...)">
            {% if current_user.is_authenticated %}
                <a href="/profil" class="text-dark"><i class="ph-duotone ph-user-circle" style="font-size: 2rem;"></i></a>
            {% else %}
                <a href="/giris" class="text-danger fw-bold text-decoration-none">Giriş</a>
            {% endif %}
        </div>
    </div>

    {% block content %}{% endblock %}

    <div class="bottom-nav">
        <a href="/" class="nav-item-m active">
            <i class="ph-duotone ph-house"></i> Ana Sayfa
        </a>
        <a href="/profil" class="nav-item-m">
            <i class="ph-duotone ph-user"></i> Profilim
        </a>
        <a href="#" onclick="alert('Quiz Modülü Hazırlanıyor!')" class="nav-item-m">
            <i class="ph-duotone ph-exam"></i> Quiz
        </a>
        {% if current_user.is_authenticated and current_user.username == 'admin' %}
        <a href="/yonetim" class="nav-item-m">
            <i class="ph-duotone ph-lock-key"></i> Admin
        </a>
        {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Live Search Scripti
        document.getElementById('liveSearch').addEventListener('keyup', function(e) {
            let term = e.target.value.toLowerCase();
            let cards = document.querySelectorAll('.filter-card');
            
            cards.forEach(card => {
                let title = card.getAttribute('data-title').toLowerCase();
                if (title.includes(term)) {
                    card.parentElement.style.display = 'block';
                } else {
                    card.parentElement.style.display = 'none';
                }
            });
        });
    </script>
</body>
</html>"""
with open(os.path.join(TEMPLATES_DIR, 'layout.html'), 'w', encoding='utf-8') as f:
    f.write(layout_code)


# 4. INDEX.HTML (Temiz Başlık + Acil Butonları)
index_code = """{% extends "layout.html" %}

{% block content %}
<style>
    .app-header {
        padding: 30px 20px;
        background: white;
        border-bottom-left-radius: 30px;
        border-bottom-right-radius: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        margin-bottom: 20px;
    }
    .welcome-text { font-size: 0.9rem; color: #64748b; font-weight: 600; }
    .main-heading { font-family: 'Outfit', sans-serif; font-weight: 800; font-size: 1.8rem; color: #1e293b; margin: 0; }

    /* ACİL DURUM GRID */
    .action-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-bottom: 30px;
        padding: 0 15px;
    }
    .action-btn {
        background: white; border-radius: 16px; padding: 15px 5px;
        text-align: center; border: 1px solid #f1f5f9;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
        transition: 0.2s; text-decoration: none; color: #333;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .action-btn:active { transform: scale(0.95); }
    .action-icon {
        width: 45px; height: 45px; border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.5rem; margin-bottom: 8px;
    }
    .action-label { font-size: 0.7rem; font-weight: 700; color: #64748b; }

    /* Buton Renkleri */
    .btn-112 .action-icon { background: #fee2e2; color: #ef4444; }
    .btn-sos .action-icon { background: #ffedd5; color: #f97316; }
    .btn-quiz .action-icon { background: #dbeafe; color: #3b82f6; }
    .btn-map .action-icon { background: #dcfce7; color: #22c55e; }

    /* DERS KARTLARI (Önceki 3D Stil Korundu ama Başlık Temizlendi) */
    .art-card {
        background: white; border-radius: 20px; padding: 20px;
        border: 1px solid #f1f5f9; position: relative; overflow: hidden;
        display: flex; align-items: center; gap: 15px;
        text-decoration: none; color: inherit; transition: 0.3s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.03);
    }
    .art-card:hover { transform: translateY(-5px); border-color: #ef4444; }
    
    .icon-holder {
        width: 60px; height: 60px; flex-shrink: 0;
    }
    .card-info h3 { font-size: 1.1rem; font-weight: 700; margin: 0; color: #1e293b; }
    .card-info span { font-size: 0.75rem; color: #94a3b8; font-weight: 600; }

</style>

<div class="app-header">
    <div class="container">
        <p class="welcome-text">{% if current_user.is_authenticated %}Merhaba, {{ current_user.username }} 👋{% else %}Merhaba Misafir 👋{% endif %}</p>
        <h1 class="main-heading">Acil durumda ne yapman gerektiğini biliyor musun?</h1>
    </div>
</div>

<div class="container">
    <div class="action-grid">
        <a href="tel:112" class="action-btn btn-112">
            <div class="action-icon"><i class="ph-duotone ph-phone-call"></i></div>
            <span class="action-label">112 ARA</span>
        </a>
        
        <a href="#" onclick="sendLocation()" class="action-btn btn-sos">
            <div class="action-icon"><i class="ph-duotone ph-warning-circle"></i></div>
            <span class="action-label">SOS</span>
        </a>

        <a href="#" class="action-btn btn-quiz">
            <div class="action-icon"><i class="ph-duotone ph-exam"></i></div>
            <span class="action-label">QUIZ</span>
        </a>

        <a href="#" class="action-btn btn-map">
            <div class="action-icon"><i class="ph-duotone ph-map-pin"></i></div>
            <span class="action-label">KONUM</span>
        </a>
    </div>
</div>

<div class="container mb-3">
    <h6 class="fw-bold text-muted ps-2">EĞİTİM MODÜLLERİ</h6>
</div>

<div class="container pb-5">
    <div class="row g-3">
        {% for konu in konular %}
        <div class="col-md-6 col-lg-4">
            <a href="{{ url_for('konu_detay', id=konu.id) }}" class="art-card filter-card" data-title="{{ konu.baslik }}">
                <div class="icon-holder">
                     <img src="{{ konu.resim }}" style="width:100%; height:100%; object-fit:contain;" 
                          onerror="this.src='https://cdn-icons-png.flaticon.com/512/2966/2966327.png'">
                </div>
                <div class="card-info">
                    <span>MODÜL {{ "%02d" % konu.sira }}</span>
                    <h3>{{ konu.baslik }}</h3>
                </div>
                <i class="ph-bold ph-caret-right ms-auto text-muted"></i>
            </a>
        </div>
        {% endfor %}
    </div>
</div>

<script>
    function sendLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                let lat = position.coords.latitude;
                let lon = position.coords.longitude;
                let msg = `ACİL DURUM! Konumum: https://www.google.com/maps?q=${lat},${lon}`;
                // WhatsApp Linki (Numara dinamik olacak, şimdilik boş)
                window.open(`https://wa.me/?text=${encodeURIComponent(msg)}`, '_blank');
            });
        } else {
            alert("Konum servisi desteklenmiyor.");
        }
    }
</script>
{% endblock %}"""
with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_code)


# 5. LOGIN & REGISTER HTML (Temiz Form)
login_html = """
{% extends "layout.html" %}
{% block content %}
<div class="container mt-5">
    <div class="card border-0 shadow-sm p-4">
        <h2 class="fw-bold mb-4">Giriş Yap</h2>
        <form method="POST">
            <div class="mb-3">
                <label>Kullanıcı Adı</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div class="mb-3">
                <label>Şifre</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button class="btn btn-danger w-100 py-2 fw-bold">Giriş</button>
        </form>
        <div class="mt-3 text-center">
            <a href="/kayit" class="text-muted">Hesabın yok mu? Kayıt Ol</a>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(TEMPLATES_DIR, 'login.html'), 'w', encoding='utf-8') as f:
    f.write(login_html)

register_html = """
{% extends "layout.html" %}
{% block content %}
<div class="container mt-5">
    <div class="card border-0 shadow-sm p-4">
        <h2 class="fw-bold mb-4">Kayıt Ol</h2>
        <form method="POST">
            <div class="mb-3">
                <label>Kullanıcı Adı</label>
                <input type="text" name="username" class="form-control" required>
            </div>
            <div class="mb-3">
                <label>Şifre</label>
                <input type="password" name="password" class="form-control" required>
            </div>
            <button class="btn btn-dark w-100 py-2 fw-bold">Hesap Oluştur</button>
        </form>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(TEMPLATES_DIR, 'register.html'), 'w', encoding='utf-8') as f:
    f.write(register_html)
    
# 6. PROFILE HTML
profile_html = """
{% extends "layout.html" %}
{% block content %}
<div class="container mt-4">
    <div class="d-flex align-items-center gap-3 mb-4">
        <div class="bg-light rounded-circle p-3">
            <i class="ph-duotone ph-user" style="font-size: 2rem;"></i>
        </div>
        <div>
            <h3 class="fw-bold m-0">{{ user.username }}</h3>
            <span class="text-muted">Üye</span>
        </div>
        <a href="/cikis" class="btn btn-sm btn-outline-danger ms-auto">Çıkış</a>
    </div>

    <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
            <h5 class="fw-bold"><i class="ph-duotone ph-phone-plus text-danger"></i> Acil Durum Kişileri</h5>
            <p class="small text-muted">SOS butonuna basınca bu kişilere mesaj atılacak (Yakında).</p>
            <form method="POST">
                <div class="mb-2">
                    <input type="text" name="no1" class="form-control" placeholder="1. Kişi (Anne, Baba...)" value="{{ user.acil_no_1 or '' }}">
                </div>
                <div class="mb-2">
                    <input type="text" name="no2" class="form-control" placeholder="2. Kişi (Eş, Kardeş...)" value="{{ user.acil_no_2 or '' }}">
                </div>
                <button class="btn btn-primary btn-sm w-100">Kaydet</button>
            </form>
        </div>
    </div>
    
    <div class="card border-0 shadow-sm">
        <div class="card-body">
            <h5 class="fw-bold">İstatistikler</h5>
            <div class="d-flex justify-content-between mt-3">
                <div class="text-center">
                    <h4 class="fw-bold m-0">0</h4>
                    <small>Tamamlanan</small>
                </div>
                <div class="text-center">
                    <h4 class="fw-bold m-0">0</h4>
                    <small>Quiz Puanı</small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
with open(os.path.join(TEMPLATES_DIR, 'profile.html'), 'w', encoding='utf-8') as f:
    f.write(profile_html)

# GIT GÖNDERİMİ
print("\n🚀 GITHUB'A YOLLANIYOR (V5.0 UYGULAMA MODU)...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "UI CLEANUP + LOGIN + SOS FEATURES"', shell=True)
subprocess.run("git push", shell=True)
print("✅ Tamamlandı. Vercel güncellendikten sonra '/kurulum-yap' adresine gidip veritabanını güncelle!")