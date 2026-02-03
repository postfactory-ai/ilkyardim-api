import os
import subprocess
import time

# --- RENKLER ---
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

print(f"{BOLD}🤖 GEMINI AJAN MODU BAŞLATILIYOR...{RESET}")
print("-" * 50)

# --- 1. DOSYA YOLLARI KONTROLÜ ---
base_dir = os.getcwd()
templates_dir = os.path.join(base_dir, 'templates')

if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
    print(f"{GREEN}✅ Templates klasörü oluşturuldu.{RESET}")

# --- 2. PREMIUM PREMIUM INDEX.HTML (ZORLA YAZMA) ---
print(f"📝 {BOLD}index.html{RESET} dosyası Premium tasarımla güncelleniyor...")

premium_html = """
{% extends "layout.html" %}

{% block content %}
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    body { background-color: #f4f7f6 !important; font-family: 'Poppins', sans-serif; }
    
    /* HERO BANNER */
    .hero-wrapper {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: white;
        padding: 80px 20px 120px 20px; /* Alttan boşluk kartlar için */
        border-radius: 0 0 40px 40px;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .hero-wrapper::before {
        content: ''; position: absolute; top:0; left:0; width:100%; height:100%;
        background: url('https://www.transparenttextures.com/patterns/medical-icons.png'); opacity: 0.1;
    }
    .hero-title { font-weight: 800; font-size: 3.5rem; letter-spacing: -1px; margin-bottom: 10px; }
    .hero-subtitle { font-weight: 300; font-size: 1.2rem; opacity: 0.8; }

    /* KART ALANI */
    .cards-container { margin-top: -80px; padding-bottom: 50px; position: relative; z-index: 10; }
    
    /* KART TASARIMI */
    .premium-card {
        background: white; border-radius: 20px; border: none;
        box-shadow: 0 15px 35px rgba(0,0,0,0.08);
        transition: all 0.4s ease; overflow: hidden; height: 100%;
        display: flex; flex-direction: column; cursor: pointer;
    }
    .premium-card:hover { transform: translateY(-15px) scale(1.02); box-shadow: 0 25px 50px rgba(0,0,0,0.2); }
    
    .card-img-area { position: relative; height: 200px; overflow: hidden; }
    .card-img-area img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.6s; }
    .premium-card:hover .card-img-area img { transform: scale(1.15); }
    
    .icon-box {
        position: absolute; bottom: -20px; right: 20px;
        width: 60px; height: 60px; background: #d32f2f; color: white;
        border-radius: 15px; display: flex; align-items: center; justify-content: center;
        font-size: 24px; box-shadow: 0 5px 15px rgba(211, 47, 47, 0.4);
        transition: all 0.3s;
    }
    .premium-card:hover .icon-box { bottom: 10px; transform: rotate(10deg); }

    .card-content { padding: 30px 20px 20px 20px; flex-grow: 1; display: flex; flex-direction: column; }
    .card-badge { 
        background: #e3f2fd; color: #1565c0; padding: 5px 10px; 
        border-radius: 8px; font-size: 12px; font-weight: 700; width: fit-content; margin-bottom: 10px;
    }
    .card-title { font-weight: 700; font-size: 1.2rem; color: #333; margin-bottom: 10px; line-height: 1.4; }
    .card-desc { font-size: 0.9rem; color: #777; margin-bottom: 20px; line-height: 1.6; }
    
    .btn-action {
        margin-top: auto; padding: 12px; width: 100%; border: none; border-radius: 12px;
        background: #f8f9fa; color: #333; font-weight: 600; transition: 0.3s; text-align: center;
    }
    .premium-card:hover .btn-action { background: #d32f2f; color: white; }
</style>

<div class="hero-wrapper">
    <div class="container">
        <h1 class="hero-title">İLK YARDIM PRO <span style="font-size:1rem; vertical-align:middle; background:red; padding:3px 8px; border-radius:5px;">CANLI</span></h1>
        <p class="hero-subtitle">T.C. Sağlık Bakanlığı Referanslı İnteraktif Eğitim Platformu</p>
    </div>
</div>

<div class="container cards-container">
    <div class="row g-4">
        {% for konu in konular %}
        <div class="col-md-6 col-lg-4 col-xl-3">
            <a href="{{ url_for('konu_detay', id=konu.id) }}" class="text-decoration-none">
                <div class="premium-card">
                    <div class="card-img-area">
                        <img src="{{ konu.resim if konu.resim else 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=500&q=80' }}" alt="Konu">
                        <div class="icon-box">
                            <i class="fa-solid fa-book-medical auto-icon" data-title="{{ konu.baslik }}"></i>
                        </div>
                    </div>
                    <div class="card-content">
                        <div class="card-badge">MODÜL {{ konu.sira }}</div>
                        <h3 class="card-title">{{ konu.baslik }}</h3>
                        <p class="card-desc">{{ konu.kisa_ozet if konu.kisa_ozet else 'Hayat kurtaran bilgileri öğrenmek için tıklayın.' }}</p>
                        <div class="btn-action">Eğitime Başla <i class="fa-solid fa-arrow-right ms-2"></i></div>
                    </div>
                </div>
            </a>
        </div>
        {% endfor %}
    </div>
</div>

<script>
    // OTOMATİK İKON ATAYICI
    const icons = {
        "GENEL": "fa-kit-medical", "VÜCUT": "fa-person", "TAŞIMA": "fa-stretcher",
        "OED": "fa-bolt", "YAŞAM": "fa-heart-pulse", "HAVA": "fa-lungs",
        "BİLİNÇ": "fa-brain", "KANAMA": "fa-droplet", "ŞOK": "fa-heart-crack",
        "YARALANMA": "fa-bandage", "BOĞULMA": "fa-water", "KIRIK": "fa-bone",
        "HAYVAN": "fa-spider", "ZEHİRLENME": "fa-skull-crossbones", "YANIK": "fa-fire"
    };
    document.querySelectorAll('.auto-icon').forEach(i => {
        let t = i.getAttribute('data-title').toUpperCase();
        for(let k in icons) if(t.includes(k)) { i.className = "fa-solid " + icons[k]; break; }
    });
</script>
{% endblock %}
"""

with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(premium_html)
print(f"{GREEN}✅ index.html dosyası başarıyla yeniden yazıldı!{RESET}")


# --- 3. LAYOUT.HTML (MODERN) ---
print(f"📝 {BOLD}layout.html{RESET} dosyası güncelleniyor...")
layout_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İlk Yardım Pro | Premium</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg bg-white shadow-sm sticky-top">
        <div class="container">
            <a class="navbar-brand fw-bold text-danger" href="/">🚑 İLK YARDIM PRO</a>
        </div>
    </nav>
    {% block content %}{% endblock %}
    <footer class="bg-dark text-white py-4 mt-5 text-center"><small>2026 Proje</small></footer>
</body>
</html>
"""
with open(os.path.join(templates_dir, 'layout.html'), 'w', encoding='utf-8') as f:
    f.write(layout_html)
print(f"{GREEN}✅ layout.html dosyası başarıyla yeniden yazıldı!{RESET}")


# --- 4. GITHUB'A ZORLA GÖNDERME (AUTOMATED GIT) ---
print(f"\n{BOLD}🚀 GITHUB'A YÜKLENİYOR (Lütfen bekleyin)...{RESET}")

def run_git(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"   Executed: {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}❌ HATA ({command}): {e.stderr}{RESET}")
        return False

# Git komut zinciri
steps = [
    "git add -A",  # Tüm değişiklikleri (silinenler dahil) ekle
    'git commit -m "AJAN MODU: Tasarimi Zorla Guncelle v9.9"',
    "git push"
]

success = True
for step in steps:
    if not run_git(step):
        success = False
        break

print("-" * 50)
if success:
    print(f"{GREEN}{BOLD}🎉 İŞLEM BAŞARILI! Kodlar GitHub'a yollandı.{RESET}")
    print("⏳ Vercel şimdi otomatik olarak güncellemeyi algılayacak.")
    print(f"{BOLD}👉 2 dakika sonra siteye gir ve CTRL+F5 yap.{RESET}")
else:
    print(f"{RED}⚠️ Git yüklemesinde sorun oluştu. Lütfen terminal çıktısını kontrol et.{RESET}")