import os
import subprocess

# --- YAPILANDIRMA ---
BASE_DIR = os.getcwd()
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
ADMIN_DIR = os.path.join(TEMPLATES_DIR, 'admin')

# Klasörleri Garantiye Al
if not os.path.exists(ADMIN_DIR):
    os.makedirs(ADMIN_DIR)

print("🛠️ SİSTEM ONARIMI BAŞLATILIYOR (Yönetim Paneli & Rotalar)...")

# 1. APP.PY (YÖNETİM ROTALARI DAHİL - EKSİKSİZ)
app_code = """import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli-anahtar-pro-123'
app.config['JSON_AS_ASCII'] = False

# VERİTABANI BAĞLANTISI
db_url = os.environ.get("DATABASE_URL")
if db_url:
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MODEL
class Konu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    icerik = db.Column(db.Text, nullable=True) 
    sira = db.Column(db.Integer, default=0)
    resim = db.Column(db.String(500), nullable=True)
    eklenme_tarihi = db.Column(db.DateTime, default=datetime.utcnow)

# --- ANA ROTALAR ---
@app.route('/')
def index():
    try:
        konular = Konu.query.order_by(Konu.sira).all()
        return render_template('index.html', konular=konular)
    except:
        return "Veritabani Baglanti Hatasi - Lutfen /kurulum-yap adresine gidin."

@app.route('/konu/<int:id>')
def konu_detay(id):
    konu = Konu.query.get_or_404(id)
    return render_template('detay.html', konu=konu)

# --- KURULUM ROTASI (TABLOLARI OLUŞTURUR) ---
@app.route('/kurulum-yap')
def kurulum():
    db.create_all()
    return "Tablolar oluşturuldu/güncellendi."

# --- YÖNETİM PANELİ ROTALARI (404 SORUNU ÇÖZÜMÜ) ---
@app.route('/yonetim')
def yonetim_index():
    konular = Konu.query.order_by(Konu.sira).all()
    return render_template('admin/index.html', konular=konular)

@app.route('/yonetim/duzenle/<int:id>', methods=['GET', 'POST'])
def yonetim_duzenle(id):
    konu = Konu.query.get_or_404(id)
    if request.method == 'POST':
        konu.baslik = request.form['baslik']
        konu.icerik = request.form['icerik']
        konu.resim = request.form['resim']
        db.session.commit()
        return redirect(url_for('yonetim_index'))
    return render_template('admin/duzenle.html', konu=konu)

# --- API ROTALARI (MOBİL İÇİN) ---
@app.route('/api/konular', methods=['GET'])
def api_konular():
    konular = Konu.query.order_by(Konu.sira).all()
    data = []
    for k in konular:
        resim_url = k.resim if k.resim else "https://via.placeholder.com/400x200?text=Resim+Yok"
        data.append({
            'id': k.id, 'baslik': k.baslik, 'resim': resim_url, 'sira': k.sira
        })
    return jsonify(data)

@app.route('/api/konu/<int:id>', methods=['GET'])
def api_detay(id):
    k = Konu.query.get_or_404(id)
    resim_url = k.resim if k.resim else "https://via.placeholder.com/400x200?text=Resim+Yok"
    return jsonify({'id': k.id, 'baslik': k.baslik, 'icerik': k.icerik, 'resim': resim_url})

if __name__ == '__main__':
    app.run(debug=True)
"""

with open(os.path.join(BASE_DIR, 'app.py'), 'w', encoding='utf-8') as f:
    f.write(app_code)
print("✅ app.py (Full Rotalı) yeniden yazıldı.")


# 2. ADMIN HTML DOSYALARI (YÖNETİM PANELİ GÖRÜNÜMÜ)
admin_index_html = """
{% extends "layout.html" %}
{% block content %}
<div class="container mt-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fa-solid fa-gear text-danger"></i> Yönetim Paneli</h2>
        <a href="/" class="btn btn-outline-secondary">Siteye Dön</a>
    </div>
    <div class="card shadow-sm">
        <div class="card-body p-0">
            <table class="table table-hover mb-0">
                <thead class="table-light">
                    <tr>
                        <th>ID</th>
                        <th>Başlık</th>
                        <th>İşlemler</th>
                    </tr>
                </thead>
                <tbody>
                    {% for k in konular %}
                    <tr>
                        <td>{{ k.sira }}</td>
                        <td>{{ k.baslik }}</td>
                        <td>
                            <a href="{{ url_for('yonetim_duzenle', id=k.id) }}" class="btn btn-sm btn-primary">Düzenle</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
"""

admin_duzenle_html = """
{% extends "layout.html" %}
{% block content %}
<div class="container mt-5">
    <h3>Konuyu Düzenle</h3>
    <form method="POST" class="mt-4">
        <div class="mb-3">
            <label>Başlık</label>
            <input type="text" name="baslik" class="form-control" value="{{ konu.baslik }}" required>
        </div>
        <div class="mb-3">
            <label>Resim URL</label>
            <input type="text" name="resim" class="form-control" value="{{ konu.resim if konu.resim else '' }}">
            <small class="text-muted">Unsplash veya başka bir yerden resim linki yapıştırın.</small>
        </div>
        <div class="mb-3">
            <label>İçerik (HTML)</label>
            <textarea name="icerik" class="form-control" rows="10">{{ konu.icerik }}</textarea>
        </div>
        <button type="submit" class="btn btn-success">Kaydet</button>
        <a href="/yonetim" class="btn btn-secondary">İptal</a>
    </form>
</div>
{% endblock %}
"""

with open(os.path.join(ADMIN_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(admin_index_html)

with open(os.path.join(ADMIN_DIR, 'duzenle.html'), 'w', encoding='utf-8') as f:
    f.write(admin_duzenle_html)

print("✅ Admin HTML şablonları oluşturuldu.")

# 3. GITHUB PUSH
print("\n🚀 DEĞİŞİKLİKLER GITHUB'A YOLLANIYOR...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "Yonetim Paneli ve Rotalar TAMIR EDILDI"', shell=True)
subprocess.run("git push", shell=True)
print("🏁 İşlem tamam. Vercel güncellenince /yonetim sayfası çalışacak.")