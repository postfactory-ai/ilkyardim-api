import os
import subprocess

# AYARLAR
BASE_DIR = os.getcwd()
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

print("\033[96m💎 PREMIUM IKON PAKETİ YÜKLENİYOR (PHOSPHOR DUOTONE)...\033[0m")

# 1. LAYOUT.HTML (Phosphor Icons Kütüphanesini Ekliyoruz)
layout_code = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İlk Yardım Pro | Premium</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Outfit', sans-serif; background-color: #f8fafc; color: #1e293b; }
        
        /* Modern Navbar */
        .navbar { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); border-bottom: 1px solid #e2e8f0; padding: 15px 0; }
        .navbar-brand { font-weight: 700; color: #ef4444 !important; font-size: 1.5rem; letter-spacing: -0.5px; display: flex; align-items: center; gap: 10px; }
        
        .nav-link { color: #64748b !important; font-weight: 600; transition: 0.3s; }
        .nav-link:hover { color: #ef4444 !important; }
        
        .btn-yonetim { 
            background: #eff6ff; color: #3b82f6; border: none; 
            padding: 8px 20px; border-radius: 12px; font-size: 0.9rem; font-weight: 600; transition: 0.3s;
        }
        .btn-yonetim:hover { background: #3b82f6; color: white; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }

        footer { margin-top: 80px; border-top: 1px solid #e2e8f0; padding: 40px 0; color: #94a3b8; font-size: 0.9rem; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="ph-duotone ph-first-aid-kit" style="font-size: 32px;"></i> İLK YARDIM PRO
            </a>
            <div class="ms-auto d-flex gap-3">
                <a class="nav-link" href="/">Eğitimler</a>
                <a class="nav-link btn-yonetim" href="/yonetim"><i class="ph-bold ph-lock-key me-1"></i> Yönetim</a>
            </div>
        </div>
    </nav>
    
    {% block content %}{% endblock %}
    
    <footer class="text-center">
        <div class="container">
            <p>T.C. Sağlık Bakanlığı Standartlarına Uygundur • 2026</p>
        </div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

with open(os.path.join(TEMPLATES_DIR, 'layout.html'), 'w', encoding='utf-8') as f:
    f.write(layout_code)


# 2. INDEX.HTML (Kart Tasarımı + Duotone İkonlar)
index_code = """{% extends "layout.html" %}

{% block content %}
<style>
    /* HERO ALANI: Hafif ve Modern */
    .hero-section {
        background: linear-gradient(180deg, #fff 0%, #f1f5f9 100%);
        padding: 80px 0 100px 0;
        text-align: center;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 50px;
    }
    .hero-badge {
        background: #fee2e2; color: #ef4444; padding: 6px 16px; 
        border-radius: 50px; font-weight: 700; font-size: 0.8rem; letter-spacing: 1px;
        display: inline-block; margin-bottom: 20px;
    }
    .hero-title { font-weight: 800; font-size: 3.5rem; color: #0f172a; margin-bottom: 15px; letter-spacing: -1.5px; }
    .hero-desc { color: #64748b; font-size: 1.25rem; max-width: 600px; margin: 0 auto; line-height: 1.6; }

    /* PREMIUM KART */
    .premium-card {
        background: white;
        border-radius: 24px;
        padding: 30px;
        height: 100%;
        border: 1px solid #f1f5f9;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex; flex-direction: column; align-items: flex-start;
        cursor: pointer; text-decoration: none; color: inherit;
        position: relative; overflow: hidden;
    }
    
    .premium-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px -5px rgba(0, 0, 0, 0.1);
        border-color: #fff;
    }

    /* İKON KUTUSU (Gradiyanlı Arkaplan) */
    .icon-box {
        width: 70px; height: 70px;
        border-radius: 20px;
        display: flex; align-items: center; justify-content: center;
        font-size: 36px;
        margin-bottom: 25px;
        transition: 0.4s;
        /* Varsayılan Renk (Mavi/Gri) */
        background: #f1f5f9; color: #475569;
    }

    /* Renk Temaları (Kategoriye Göre Değişecek) */
    .theme-red .icon-box { background: #fee2e2; color: #ef4444; }
    .theme-blue .icon-box { background: #dbeafe; color: #3b82f6; }
    .theme-orange .icon-box { background: #ffedd5; color: #f97316; }
    .theme-green .icon-box { background: #dcfce7; color: #22c55e; }

    .premium-card:hover .icon-box {
        transform: scale(1.1) rotate(5deg);
    }

    .card-meta { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #94a3b8; letter-spacing: 1px; margin-bottom: 10px; }
    .card-title { font-weight: 700; font-size: 1.3rem; color: #1e293b; margin-bottom: 10px; line-height: 1.3; }
    .card-arrow {
        margin-top: auto; font-weight: 600; font-size: 0.9rem; color: #ef4444; 
        display: flex; align-items: center; gap: 8px; opacity: 0; transform: translateX(-10px); transition: 0.3s;
    }
    .premium-card:hover .card-arrow { opacity: 1; transform: translateX(0); }

</style>

<div class="hero-section">
    <div class="container">
        <span class="hero-badge">VERSİYON 4.0</span>
        <h1 class="hero-title">Hayat Kurtar.</h1>
        <p class="hero-desc">Profesyonel, görsel ve interaktif ilk yardım rehberi. Acil durumlarda saniyeler önemlidir.</p>
    </div>
</div>

<div class="container pb-5">
    <div class="row g-4">
        {% for konu in konular %}
        <div class="col-md-6 col-lg-4 col-xl-3">
            <a href="{{ url_for('konu_detay', id=konu.id) }}" class="premium-card dynamic-card" data-title="{{ konu.baslik }}">
                <div class="card-meta">MODÜL {{ konu.sira }}</div>
                
                <div class="icon-box">
                    <i class="ph-duotone ph-circle-notch auto-icon"></i>
                </div>
                
                <h3 class="card-title">{{ konu.baslik }}</h3>
                
                <div class="card-arrow">
                    İncele <i class="ph-bold ph-arrow-right"></i>
                </div>
            </a>
        </div>
        {% endfor %}
    </div>
</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        // İKON VE RENK EŞLEŞTİRME TABLOSU
        const mapping = {
            "GENEL": { icon: "ph-info", theme: "theme-blue" },
            "VÜCUT": { icon: "ph-person-arms-spread", theme: "theme-blue" },
            "TAŞIMA": { icon: "ph-ambulance", theme: "theme-orange" }, // Ambulance yoksa truck
            "OED": { icon: "ph-lightning", theme: "theme-orange" },
            "YAŞAM": { icon: "ph-heartbeat", theme: "theme-red" },
            "HAVA": { icon: "ph-wind", theme: "theme-blue" },
            "BİLİNÇ": { icon: "ph-brain", theme: "theme-orange" },
            "KANAMA": { icon: "ph-drop", theme: "theme-red" },
            "ŞOK": { icon: "ph-heart-break", theme: "theme-red" },
            "YARALANMA": { icon: "ph-band-aids", theme: "theme-orange" },
            "BOĞULMA": { icon: "ph-waves", theme: "theme-blue" },
            "KIRIK": { icon: "ph-bone", theme: "theme-red" },
            "HAYVAN": { icon: "ph-bug", theme: "theme-green" }, // Spider yerine bug
            "ZEHİRLENME": { icon: "ph-skull", theme: "theme-green" },
            "YANIK": { icon: "ph-fire", theme: "theme-orange" },
            "GÖZ": { icon: "ph-eye", theme: "theme-blue" }
        };

        const cards = document.querySelectorAll('.dynamic-card');
        
        cards.forEach(card => {
            const title = card.getAttribute('data-title').toUpperCase();
            const iconEl = card.querySelector('.auto-icon');
            
            let matchedIcon = "ph-first-aid-kit"; // Varsayılan İkon
            let matchedTheme = "theme-blue";      // Varsayılan Renk

            for (const [key, val] of Object.entries(mapping)) {
                if (title.includes(key)) {
                    matchedIcon = val.icon;
                    matchedTheme = val.theme;
                    break;
                }
            }
            
            // İkonu Değiştir
            iconEl.className = `ph-duotone ${matchedIcon} auto-icon`;
            
            // Rengi Değiştir
            card.classList.add(matchedTheme);
        });
    });
</script>
{% endblock %}"""

with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_code)

print("\n🚀 GITHUB'A YOLLANIYOR (PHOSPHOR UPGRADE)...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "TASARIM V4: Premium DuoTone Ikonlar"', shell=True)
subprocess.run("git push", shell=True)
print("✅ İşlem Tamam! Vercel'i bekle ve CTRL+F5 yap.")