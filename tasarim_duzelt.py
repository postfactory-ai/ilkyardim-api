import os
import subprocess

# --- AYARLAR ---
BASE_DIR = os.getcwd()
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

print("\033[92m🚑 TASARIM DÜZELTİLİYOR: ACİL KIRMIZI MODU AKTİF...\033[0m")

# 1. LAYOUT.HTML (Menüye Yönetim Linki Eklendi)
layout_code = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İlk Yardım Pro | Hayat Kurtar</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f8f9fa; }
        .navbar { background: white; border-bottom: 3px solid #dc3545; padding: 15px 0; }
        .navbar-brand { font-weight: 800; color: #dc3545 !important; font-size: 1.5rem; letter-spacing: -0.5px; }
        .nav-link { color: #333 !important; font-weight: 600; margin-left: 15px; transition: 0.3s; }
        .nav-link:hover { color: #dc3545 !important; }
        .btn-yonetim { background: #333; color: white; border-radius: 50px; padding: 5px 20px; font-size: 0.9rem; }
        .btn-yonetim:hover { background: #000; color: white; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg sticky-top shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="/"><i class="fa-solid fa-heart-pulse me-2"></i>İLK YARDIM PRO</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto align-items-center">
                    <li class="nav-item"><a class="nav-link" href="/">Eğitimler</a></li>
                    <li class="nav-item"><a class="nav-link btn-yonetim" href="/yonetim"><i class="fa-solid fa-lock me-1"></i> Yönetici Girişi</a></li>
                </ul>
            </div>
        </div>
    </nav>
    
    {% block content %}{% endblock %}
    
    <footer class="text-center py-4 mt-5 text-muted border-top">
        <small>© 2026 İlk Yardım Eğitim Platformu</small>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

with open(os.path.join(TEMPLATES_DIR, 'layout.html'), 'w', encoding='utf-8') as f:
    f.write(layout_code)

# 2. INDEX.HTML (Kırmızı Tema & Düzgün Kartlar)
index_code = """{% extends "layout.html" %}

{% block content %}
<style>
    /* HERO: Acil Durum Kırmızısı */
    .hero-section {
        background: linear-gradient(135deg, #dc3545 0%, #b02a37 100%);
        color: white;
        padding: 80px 0 100px 0;
        margin-bottom: -60px;
        text-align: center;
        border-radius: 0 0 40px 40px;
        box-shadow: 0 10px 30px rgba(220, 53, 69, 0.3);
    }
    .hero-title { font-weight: 800; font-size: 3rem; margin-bottom: 10px; }
    .hero-subtitle { font-size: 1.2rem; opacity: 0.9; max-width: 700px; margin: 0 auto; font-weight: 300; }

    /* KARTLAR */
    .topic-card {
        background: white;
        border-radius: 16px;
        border: none;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        height: 100%;
        overflow: hidden;
        text-decoration: none;
        display: block;
        color: inherit;
    }
    .topic-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(220, 53, 69, 0.2); /* Kırmızı Gölge */
    }

    /* RESİM ALANI */
    .img-container {
        height: 180px;
        position: relative;
        overflow: hidden;
        background: #f1f1f1;
    }
    .img-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .status-badge {
        position: absolute;
        top: 10px; left: 10px;
        background: #dc3545; color: white;
        font-size: 0.75rem; font-weight: 700;
        padding: 4px 10px; border-radius: 6px;
    }

    .card-body { padding: 20px; }
    .card-title { font-weight: 700; font-size: 1.1rem; margin-bottom: 10px; color: #212529; line-height: 1.4; }
    .read-more {
        color: #dc3545; font-weight: 600; font-size: 0.9rem;
        display: flex; align-items: center; margin-top: 10px;
    }
    .read-more i { transition: 0.3s; }
    .topic-card:hover .read-more i { transform: translateX(5px); }

</style>

<div class="hero-section">
    <div class="container">
        <h1 class="hero-title">Hayat Kurtaran Bilgiler</h1>
        <p class="hero-subtitle">T.C. Sağlık Bakanlığı onaylı güncel ilk yardım rehberi. Her an hazırlıklı olun.</p>
    </div>
</div>

<div class="container" style="padding-bottom: 50px;">
    <div class="row g-4">
        {% for konu in konular %}
        <div class="col-md-6 col-lg-4 col-xl-3">
            <a href="{{ url_for('konu_detay', id=konu.id) }}" class="topic-card">
                <div class="img-container">
                    <span class="status-badge">MODÜL {{ konu.sira }}</span>
                    <img src="{{ konu.resim if konu.resim else 'https://dummyimage.com/600x400/eeeeee/999999&text=Resim+Yok' }}" alt="{{ konu.baslik }}">
                </div>
                <div class="card-body">
                    <h5 class="card-title">{{ konu.baslik }}</h5>
                    <div class="read-more">
                        İncele <i class="fa-solid fa-arrow-right ms-2"></i>
                    </div>
                </div>
            </a>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}"""

with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_code)

print("\n🚀 GIT GÜNCELLEMESİ BAŞLIYOR...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "TASARIM DUZELTME: Kirmizi Tema ve Yonetim Paneli"', shell=True)
subprocess.run("git push", shell=True)
print("✅ İşlem Tamam! Vercel güncelleniyor...")