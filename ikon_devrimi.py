import os
import subprocess

# AYARLAR
BASE_DIR = os.getcwd()
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

print("\033[92m🚑 KÖKLÜ DEĞİŞİM: RESİMLER GİDİYOR, İKONLAR GELİYOR...\033[0m")

# 1. LAYOUT.HTML (FontAwesome Kütüphanesi Garanti Olsun)
layout_code = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İlk Yardım Pro | Eğitim Platformu</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f4f6f8; }
        
        .navbar { background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 15px 0; }
        .navbar-brand { font-family: 'Poppins', sans-serif; font-weight: 700; color: #d32f2f !important; font-size: 1.4rem; }
        
        .nav-link { color: #555 !important; font-weight: 500; transition: 0.3s; }
        .nav-link:hover { color: #d32f2f !important; }
        
        .btn-yonetim { 
            background: #f8f9fa; color: #333; border: 1px solid #ddd; 
            padding: 8px 20px; border-radius: 50px; font-size: 0.85rem; font-weight: 600;
        }
        .btn-yonetim:hover { background: #333; color: white; border-color: #333; }

        footer { background: #fff; color: #777; padding: 30px 0; margin-top: 60px; border-top: 1px solid #eee; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fa-solid fa-staff-snake me-2"></i>İLK YARDIM PRO
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto align-items-center gap-3">
                    <li class="nav-item"><a class="nav-link" href="/">Modüller</a></li>
                    <li class="nav-item"><a class="nav-link btn-yonetim" href="/yonetim"><i class="fa-solid fa-lock me-1"></i> Yönetim</a></li>
                </ul>
            </div>
        </div>
    </nav>
    
    {% block content %}{% endblock %}
    
    <footer class="text-center">
        <div class="container">
            <small>© 2026 T.C. Sağlık Bakanlığı Referanslı Eğitim Projesi</small>
        </div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

with open(os.path.join(TEMPLATES_DIR, 'layout.html'), 'w', encoding='utf-8') as f:
    f.write(layout_code)


# 2. INDEX.HTML (İkon Tabanlı Temiz Tasarım)
index_code = """{% extends "layout.html" %}

{% block content %}
<style>
    /* HERO: Modern ve Temiz */
    .hero-box {
        background: #fff;
        padding: 60px 20px;
        text-align: center;
        border-bottom: 1px solid #eee;
        margin-bottom: 40px;
    }
    .hero-title { font-family: 'Poppins', sans-serif; font-weight: 700; color: #2c3e50; font-size: 2.5rem; margin-bottom: 10px; }
    .hero-desc { color: #6c757d; font-size: 1.1rem; max-width: 600px; margin: 0 auto; }

    /* İKON KARTLARI */
    .icon-card {
        background: #fff;
        border: 1px solid #eef2f5;
        border-radius: 16px;
        padding: 30px 20px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
        text-decoration: none;
        color: inherit;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    .icon-card:hover {
        transform: translateY(-5px);
        border-color: #ffcdd2;
        box-shadow: 0 10px 25px rgba(211, 47, 47, 0.1);
    }

    /* İKON DAİRESİ */
    .icon-circle {
        width: 80px; height: 80px;
        background: #fff5f5; /* Çok açık kırmızı */
        color: #d32f2f; /* Ana Kırmızı */
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .icon-card:hover .icon-circle {
        background: #d32f2f;
        color: white;
        transform: scale(1.1);
    }

    .card-title { font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 1.1rem; color: #333; margin-bottom: 8px; line-height: 1.4; }
    .card-meta { font-size: 0.8rem; color: #999; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 15px; }
    
    .btn-arrow {
        margin-top: auto;
        width: 40px; height: 40px;
        border-radius: 50%;
        background: #f8f9fa; color: #ccc;
        display: flex; align-items: center; justify-content: center;
        transition: 0.3s;
    }
    .icon-card:hover .btn-arrow { background: #333; color: white; }
</style>

<div class="hero-box">
    <div class="container">
        <h1 class="hero-title">Hayat Kurtaran Bilgiler</h1>
        <p class="hero-desc">Acil durumlarda yapılması gerekenler, güncel müfredat ve anlaşılır modüllerle elinizin altında.</p>
    </div>
</div>

<div class="container pb-5">
    <div class="row g-4">
        {% for konu in konular %}
        <div class="col-md-6 col-lg-4 col-xl-3">
            <a href="{{ url_for('konu_detay', id=konu.id) }}" class="icon-card">
                <div class="card-meta">MODÜL {{ konu.sira }}</div>
                
                <div class="icon-circle">
                    <i class="fa-solid fa-book-medical auto-icon" data-title="{{ konu.baslik }}"></i>
                </div>
                
                <h3 class="card-title">{{ konu.baslik }}</h3>
                
                <div class="btn-arrow">
                    <i class="fa-solid fa-arrow-right"></i>
                </div>
            </a>
        </div>
        {% endfor %}
    </div>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        const iconMap = {
            "GENEL": "fa-kit-medical",
            "VÜCUT": "fa-person-rays",
            "TAŞIMA": "fa-truck-medical",
            "OED": "fa-heart-pulse",
            "YAŞAM": "fa-hands-holding-circle",
            "HAVA": "fa-lungs",
            "BİLİNÇ": "fa-brain",
            "KANAMA": "fa-droplet",
            "ŞOK": "fa-bolt",
            "YARALANMA": "fa-crutch",
            "BOĞULMA": "fa-life-ring",
            "KIRIK": "fa-bone",
            "HAYVAN": "fa-spider",
            "ZEHİRLENME": "fa-flask-vial",
            "YANIK": "fa-fire-flame-curved",
            "GÖZ": "fa-eye",
            "YABANCI": "fa-ear-listen"
        };

        const icons = document.querySelectorAll('.auto-icon');
        icons.forEach(icon => {
            const title = icon.getAttribute('data-title').toUpperCase();
            let matchedClass = "fa-briefcase-medical"; // Varsayılan İkon

            for (const [key, value] of Object.entries(iconMap)) {
                if (title.includes(key)) {
                    matchedClass = value;
                    break;
                }
            }
            // Classları temizle ve yenisini ekle
            icon.className = ""; 
            icon.className = "fa-solid " + matchedClass + " auto-icon";
        });
    });
</script>
{% endblock %}"""

with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_code)

print("\n🚀 GIT'E GÖNDERİLİYOR...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "TASARIM DEVRIMI: Ikon Modu Aktif"', shell=True)
subprocess.run("git push", shell=True)
print("✅ Vercel güncelleniyor. Siteye girip CTRL+F5 yap.")