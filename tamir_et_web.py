import os
import subprocess

# --- AYARLAR ---
BASE_DIR = os.getcwd() # Şu anki klasör (C:\ilkyardim_proje)
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Renkli Çıktılar
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

print(f"{GREEN}🚀 GOOGLE ANTIGRAVITY MODU: WEB TAMİRİ BAŞLIYOR...{RESET}")

# 1. TEMPLATES KLASÖRÜNÜ KONTROL ET
if not os.path.exists(TEMPLATES_DIR):
    os.makedirs(TEMPLATES_DIR)

# 2. PREMIUM LAYOUT.HTML (ZORLA YAZ)
print("📝 layout.html yenileniyor...")
layout_code = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İlk Yardım Pro | Eğitim Platformu</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Poppins', sans-serif; background-color: #f0f2f5; }
        .navbar { background: white; box-shadow: 0 2px 15px rgba(0,0,0,0.04); padding: 15px 0; }
        .navbar-brand { font-weight: 800; color: #d32f2f !important; letter-spacing: -0.5px; font-size: 1.5rem; }
        .footer { background: #2c3e50; color: white; padding: 40px 0; margin-top: 80px; text-align: center; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a class="navbar-brand" href="/"><i class="fa-solid fa-heart-pulse me-2"></i>İLK YARDIM PRO</a>
        </div>
    </nav>
    
    {% block content %}{% endblock %}
    
    <div class="footer">
        <div class="container">
            <p class="mb-0 opacity-75">© 2026 T.C. Sağlık Bakanlığı Referanslı Eğitim Projesi</p>
        </div>
    </div>
</body>
</html>"""

with open(os.path.join(TEMPLATES_DIR, 'layout.html'), 'w', encoding='utf-8') as f:
    f.write(layout_code)


# 3. PREMIUM INDEX.HTML (ZORLA YAZ - NETFLIX TARZI)
print("📝 index.html yenileniyor (Premium Tasarım)...")
index_code = """{% extends "layout.html" %}

{% block content %}
<style>
    /* HERO SECTION */
    .hero-header {
        background: linear-gradient(135deg, #0b0f19 0%, #1a2a3a 100%);
        color: white;
        padding: 100px 0 150px 0;
        margin-bottom: -80px;
        position: relative;
        overflow: hidden;
        border-radius: 0 0 50px 50px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .hero-header::before {
        content: ''; position: absolute; top:0; left:0; width:100%; height:100%;
        background: url('https://www.transparenttextures.com/patterns/medical-icons.png');
        opacity: 0.05;
    }
    .main-title { font-size: 3.5rem; font-weight: 800; margin-bottom: 10px; }
    .sub-title { font-size: 1.2rem; opacity: 0.8; font-weight: 300; max-width: 600px; margin: 0 auto; }

    /* CARDS */
    .content-area { position: relative; z-index: 5; padding-bottom: 50px; }
    
    .pro-card {
        background: white; border-radius: 20px; border: none;
        overflow: hidden; height: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex; flex-direction: column;
        cursor: pointer; text-decoration: none; color: inherit;
    }
    .pro-card:hover { transform: translateY(-15px); box-shadow: 0 20px 50px rgba(0,0,0,0.2); }
    
    .card-img-box { position: relative; height: 220px; overflow: hidden; }
    .card-img-box img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s; }
    .pro-card:hover .card-img-box img { transform: scale(1.1); }
    
    .card-overlay {
        position: absolute; bottom: 0; left: 0; right: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
        padding: 20px; display: flex; align-items: flex-end; justify-content: space-between;
    }
    .card-icon {
        background: #d32f2f; color: white; width: 45px; height: 45px;
        border-radius: 12px; display: flex; align-items: center; justify-content: center;
        font-size: 20px; box-shadow: 0 4px 10px rgba(211, 47, 47, 0.5);
    }

    .card-body { padding: 25px; flex-grow: 1; display: flex; flex-direction: column; }
    .module-badge { font-size: 0.75rem; font-weight: 700; color: #d32f2f; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
    .card-title { font-size: 1.25rem; font-weight: 700; color: #2c3e50; line-height: 1.4; margin-bottom: 10px; }
    .card-desc { font-size: 0.9rem; color: #7f8c8d; line-height: 1.6; margin-bottom: 20px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;}
    
    .btn-go {
        margin-top: auto; background: #f8f9fa; color: #2c3e50; border: none;
        width: 100%; padding: 12px; border-radius: 12px; font-weight: 600;
        transition: 0.3s; display: flex; justify-content: space-between; align-items: center;
    }
    .pro-card:hover .btn-go { background: #d32f2f; color: white; }
</style>

<div class="hero-header">
    <div class="container">
        <h1 class="main-title">İLK YARDIM <span class="text-danger">PRO</span></h1>
        <p class="sub-title">Hayat kurtaran profesyonel bilgiler, modern arayüz ve güncel müfredat ile şimdi yayında.</p>
    </div>
</div>

<div class="container content-area">
    <div class="row g-4">
        {% for konu in konular %}
        <div class="col-md-6 col-lg-4 col-xl-3">
            <a href="{{ url_for('konu_detay', id=konu.id) }}" class="pro-card text-decoration-none">
                <div class="card-img-box">
                    <img src="{{ konu.resim if konu.resim else 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&q=80' }}" alt="{{ konu.baslik }}">
                    <div class="card-overlay">
                        <div class="card-icon">
                            <i class="fa-solid fa-book-medical auto-icon" data-title="{{ konu.baslik }}"></i>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="module-badge">MODÜL {{ konu.sira }}</div>
                    <h3 class="card-title">{{ konu.baslik }}</h3>
                    <p class="card-desc">{{ konu.kisa_ozet if konu.kisa_ozet else 'Bu modülün içeriği yükleniyor...' }}</p>
                    <div class="btn-go">
                        İncele <i class="fa-solid fa-arrow-right"></i>
                    </div>
                </div>
            </a>
        </div>
        {% endfor %}
    </div>
</div>

<script>
    const iconMap = {
        "GENEL": "fa-kit-medical", "VÜCUT": "fa-person", "TAŞIMA": "fa-truck-medical",
        "OED": "fa-bolt", "YAŞAM": "fa-heart-pulse", "HAVA": "fa-lungs", "BİLİNÇ": "fa-brain",
        "KANAMA": "fa-droplet", "ŞOK": "fa-heart-crack", "YARALANMA": "fa-bandage",
        "BOĞULMA": "fa-life-ring", "KIRIK": "fa-bone", "HAYVAN": "fa-spider",
        "ZEHİRLENME": "fa-flask", "YANIK": "fa-fire", "GÖZ": "fa-eye"
    };
    document.querySelectorAll('.auto-icon').forEach(icon => {
        const title = icon.getAttribute('data-title').toUpperCase();
        for (const [key, val] of Object.entries(iconMap)) {
            if (title.includes(key)) { icon.className = `fa-solid ${val} card-icon-i`; break; }
        }
    });
</script>
{% endblock %}"""

with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_code)


# 4. GIT VE VERCEL'İ TETİKLE
print("\n🔄 GIT GÜNCELLEMESİ YAPILIYOR...")

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True, text=True)
        print(f"✅ Çalıştı: {cmd}")
    except subprocess.CalledProcessError as e:
        print(f"{RED}❌ Hata: {cmd} -> {e}{RESET}")

# Git komutları (Force Push benzeri etki için)
run_cmd("git add -A")
run_cmd('git commit -m "GOOGLE ANTIGRAVITY FIX: Zorla Tasarim Guncellemesi"')
run_cmd("git push")

print(f"\n{GREEN}🎉 İŞLEM TAMAMLANDI!{RESET}")
print("👉 Şimdi Vercel paneline git ve 'Building' işleminin bitmesini bekle.")
print("👉 Sonra siteye gir ve CTRL+F5 yap.")