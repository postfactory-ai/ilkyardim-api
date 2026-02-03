import os
import subprocess

# AYARLAR
BASE_DIR = os.getcwd()
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

print("\033[95m🎨 GEMINI AI ÖZEL ÇİZİM SETİ: 16 ADET VEKTÖR SANATI YÜKLENİYOR...\033[0m")

# --- SVG İKON SETİ (BU BÖLÜMÜ AI OLARAK SIFIRDAN ÇİZDİM) ---
# Her biri birer sanat eseri. Degrade, gölge ve detay içerir.

# 1. GENEL BİLGİ (Kitap ve Kalp)
SVG_GENEL = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint0_linear)"/>
<path d="M25 30H55C57.2091 30 59 31.7909 59 34V54H21V34C21 31.7909 22.7909 30 25 30Z" fill="white" fill-opacity="0.9"/>
<path d="M21 54H59V58C59 60.2091 57.2091 62 55 62H25C22.7909 62 21 60.2091 21 58V54Z" fill="white" fill-opacity="0.7"/>
<path d="M40 25C43 22 48 22 51 25C54 28 54 33 51 36L40 47L29 36C26 33 26 28 29 25C32 22 37 22 40 25Z" fill="#FF3B3B"/>
<defs>
<linearGradient id="paint0_linear" x1="0" y1="0" x2="80" y2="80" gradientUnits="userSpaceOnUse">
<stop stop-color="#4facfe"/>
<stop offset="1" stop-color="#00f2fe"/>
</linearGradient>
</defs>
</svg>"""

# 2. VÜCUT SİSTEMLERİ (Anatomi)
SVG_VUCUT = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint1_linear)"/>
<circle cx="40" cy="25" r="10" stroke="white" stroke-width="4"/>
<path d="M40 35V65M25 45H55" stroke="white" stroke-width="4" stroke-linecap="round"/>
<circle cx="40" cy="50" r="12" fill="white" fill-opacity="0.3"/>
<defs>
<linearGradient id="paint1_linear" x1="40" y1="0" x2="40" y2="80" gradientUnits="userSpaceOnUse">
<stop stop-color="#43e97b"/>
<stop offset="1" stop-color="#38f9d7"/>
</linearGradient>
</defs>
</svg>"""

# 3. ACİL TAŞIMA (Sirenli Ambulans)
SVG_TASIMA = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint2_linear)"/>
<path d="M15 40H65V60H15V40Z" fill="white"/>
<path d="M45 30H65V40H45V30Z" fill="white" fill-opacity="0.8"/>
<circle cx="25" cy="60" r="6" fill="#333"/>
<circle cx="55" cy="60" r="6" fill="#333"/>
<path d="M50 20L55 25H45L50 20Z" fill="#FF3B3B"/>
<rect x="38" y="45" width="14" height="4" fill="#FF3B3B"/>
<rect x="43" y="40" width="4" height="14" fill="#FF3B3B"/>
<defs>
<linearGradient id="paint2_linear" x1="0" y1="0" x2="80" y2="0" gradientUnits="userSpaceOnUse">
<stop stop-color="#ff9a44"/>
<stop offset="1" stop-color="#fc6076"/>
</linearGradient>
</defs>
</svg>"""

# 4. OED (Yıldırımlı Kalp Cihazı)
SVG_OED = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint3_linear)"/>
<rect x="20" y="30" width="40" height="35" rx="5" fill="white"/>
<path d="M35 20V30H45V20H35Z" fill="white" fill-opacity="0.6"/>
<path d="M40 38L45 45H38L42 55L36 48H43L40 38Z" fill="#FFD700" stroke="#FFA500" stroke-width="1"/>
<defs>
<linearGradient id="paint3_linear" x1="40" y1="0" x2="40" y2="80" gradientUnits="userSpaceOnUse">
<stop stop-color="#fa709a"/>
<stop offset="1" stop-color="#fee140"/>
</linearGradient>
</defs>
</svg>"""

# 5. TEMEL YAŞAM (El ve Nabız)
SVG_YASAM = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint4_linear)"/>
<path d="M30 45C30 55 40 65 40 65C40 65 50 55 50 45C50 40 45 35 40 40C35 35 30 40 30 45Z" fill="#FF3B3B"/>
<path d="M20 30L25 20H55L60 30" stroke="white" stroke-width="4" stroke-linecap="round"/>
<path d="M10 40H25L30 30L40 50L50 30L55 40H70" stroke="white" stroke-width="3" fill="none"/>
<defs>
<linearGradient id="paint4_linear" x1="0" y1="80" x2="80" y2="0" gradientUnits="userSpaceOnUse">
<stop stop-color="#ff0844"/>
<stop offset="1" stop-color="#ffb199"/>
</linearGradient>
</defs>
</svg>"""

# 6. HAVA YOLU (Akciğer ve Boru)
SVG_HAVA = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint5_linear)"/>
<path d="M40 20V40" stroke="white" stroke-width="6" stroke-linecap="round"/>
<path d="M25 45C25 55 35 65 38 65H42C45 65 55 55 55 45C55 35 42 40 42 40H38C38 40 25 35 25 45Z" fill="white" fill-opacity="0.8"/>
<circle cx="40" cy="20" r="5" fill="#B0E0E6"/>
<defs>
<linearGradient id="paint5_linear" x1="40" y1="0" x2="40" y2="80" gradientUnits="userSpaceOnUse">
<stop stop-color="#a1c4fd"/>
<stop offset="1" stop-color="#c2e9fb"/>
</linearGradient>
</defs>
</svg>"""

# 7. BİLİNÇ (Beyin ve Soru İşareti)
SVG_BILINC = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint6_linear)"/>
<path d="M30 30C30 20 50 20 50 30C50 35 40 40 40 40V50" stroke="white" stroke-width="5" stroke-linecap="round"/>
<circle cx="40" cy="60" r="4" fill="white"/>
<path d="M20 40C20 50 25 60 40 60C55 60 60 50 60 40C60 35 55 25 40 25C25 25 20 35 20 40Z" fill="white" fill-opacity="0.3"/>
<defs>
<linearGradient id="paint6_linear" x1="0" y1="0" x2="80" y2="80" gradientUnits="userSpaceOnUse">
<stop stop-color="#a8edea"/>
<stop offset="1" stop-color="#fed6e3"/>
</linearGradient>
</defs>
</svg>"""

# 8. KANAMA (Damla ve Bandaj)
SVG_KANAMA = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint7_linear)"/>
<path d="M40 20C40 20 55 40 55 50C55 60 48 65 40 65C32 65 25 60 25 50C25 40 40 20 40 20Z" fill="#8B0000"/>
<rect x="30" y="45" width="20" height="10" rx="2" fill="white" fill-opacity="0.8"/>
<defs>
<linearGradient id="paint7_linear" x1="40" y1="80" x2="40" y2="0" gradientUnits="userSpaceOnUse">
<stop stop-color="#eb3349"/>
<stop offset="1" stop-color="#f45c43"/>
</linearGradient>
</defs>
</svg>"""

# 9. ŞOK (Yıldırım Çarpması)
SVG_SOK = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint8_linear)"/>
<path d="M45 15L25 40H40L35 65L55 40H40L45 15Z" fill="white" stroke="#FFD700" stroke-width="2"/>
<defs>
<linearGradient id="paint8_linear" x1="0" y1="0" x2="80" y2="0" gradientUnits="userSpaceOnUse">
<stop stop-color="#42275a"/>
<stop offset="1" stop-color="#734b6d"/>
</linearGradient>
</defs>
</svg>"""

# 10. YARALANMA (Dikişli Yara)
SVG_YARALANMA = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint9_linear)"/>
<path d="M20 40C30 30 50 30 60 40C50 50 30 50 20 40Z" fill="#FFcccb"/>
<path d="M25 35L35 45M35 35L45 45M45 35L55 45" stroke="#8B0000" stroke-width="3"/>
<defs>
<linearGradient id="paint9_linear" x1="40" y1="0" x2="40" y2="80" gradientUnits="userSpaceOnUse">
<stop stop-color="#ffecd2"/>
<stop offset="1" stop-color="#fcb69f"/>
</linearGradient>
</defs>
</svg>"""

# 11. BOĞULMA (Dalgalar ve Cankurtaran)
SVG_BOGULMA = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint10_linear)"/>
<path d="M10 50C20 45 30 55 40 50C50 45 60 55 70 50V70H10V50Z" fill="white" fill-opacity="0.7"/>
<circle cx="40" cy="35" r="12" stroke="white" stroke-width="4"/>
<path d="M40 28V42M33 35H47" stroke="white" stroke-width="4"/>
<defs>
<linearGradient id="paint10_linear" x1="0" y1="0" x2="80" y2="80" gradientUnits="userSpaceOnUse">
<stop stop-color="#00c6fb"/>
<stop offset="1" stop-color="#005bea"/>
</linearGradient>
</defs>
</svg>"""

# 12. KIRIK (Kırık Kemik)
SVG_KIRIK = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint11_linear)"/>
<path d="M30 20C25 20 25 30 30 30H35L25 50H20C15 50 15 60 20 60H30C35 60 35 50 30 50L40 30H50C55 30 55 20 50 20H30Z" fill="white"/>
<path d="M35 30L45 50" stroke="#8B0000" stroke-width="3"/>
<defs>
<linearGradient id="paint11_linear" x1="40" y1="0" x2="40" y2="80" gradientUnits="userSpaceOnUse">
<stop stop-color="#e0c3fc"/>
<stop offset="1" stop-color="#8ec5fc"/>
</linearGradient>
</defs>
</svg>"""

# 13. HAYVAN (Yılan ve Diş)
SVG_HAYVAN = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint12_linear)"/>
<path d="M40 20C50 20 60 30 60 40C60 50 50 60 40 60C35 60 30 55 30 50V30C30 25 35 20 40 20Z" fill="white"/>
<circle cx="50" cy="30" r="3" fill="#000"/>
<path d="M35 40L30 50M45 40L50 50" stroke="#8B0000" stroke-width="3"/>
<defs>
<linearGradient id="paint12_linear" x1="0" y1="80" x2="80" y2="0" gradientUnits="userSpaceOnUse">
<stop stop-color="#0ba360"/>
<stop offset="1" stop-color="#3cba92"/>
</linearGradient>
</defs>
</svg>"""

# 14. ZEHİRLENME (Kuru Kafa ve Şişe)
SVG_ZEHIRLENME = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint13_linear)"/>
<rect x="35" y="15" width="10" height="10" fill="white"/>
<path d="M30 25H50L55 55H25L30 25Z" fill="white" fill-opacity="0.8"/>
<circle cx="35" cy="40" r="3" fill="#000"/>
<circle cx="45" cy="40" r="3" fill="#000"/>
<path d="M35 50C35 50 40 45 45 50" stroke="#000" stroke-width="2"/>
<defs>
<linearGradient id="paint13_linear" x1="40" y1="0" x2="40" y2="80" gradientUnits="userSpaceOnUse">
<stop stop-color="#434343"/>
<stop offset="1" stop-color="#000000"/>
</linearGradient>
</defs>
</svg>"""

# 15. YANIK (Alev ve Derece)
SVG_YANIK = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint14_linear)"/>
<path d="M40 20C40 20 55 40 55 55C55 65 48 70 40 70C32 70 25 65 25 55C25 40 40 20 40 20Z" fill="#FF4500"/>
<path d="M40 30C40 30 50 45 50 55C50 60 45 65 40 65C35 65 30 60 30 55C30 45 40 30 40 30Z" fill="#FFD700"/>
<defs>
<linearGradient id="paint14_linear" x1="40" y1="80" x2="40" y2="0" gradientUnits="userSpaceOnUse">
<stop stop-color="#f5576c"/>
<stop offset="1" stop-color="#f093fb"/>
</linearGradient>
</defs>
</svg>"""

# 16. GÖZ (Göz ve Mercek)
SVG_GOZ = """<svg width="100%" height="100%" viewBox="0 0 80 80" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect width="80" height="80" rx="20" fill="url(#paint15_linear)"/>
<path d="M10 40C10 40 25 25 40 25C55 25 70 40 70 40C70 40 55 55 40 55C25 55 10 40 10 40Z" fill="white"/>
<circle cx="40" cy="40" r="10" fill="#4682B4"/>
<circle cx="40" cy="40" r="5" fill="#000"/>
<defs>
<linearGradient id="paint15_linear" x1="0" y1="0" x2="80" y2="80" gradientUnits="userSpaceOnUse">
<stop stop-color="#89f7fe"/>
<stop offset="1" stop-color="#66a6ff"/>
</linearGradient>
</defs>
</svg>"""

# --------------------------------------------------

# 1. LAYOUT.HTML (Gerekirse diye)
layout_code = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İlk Yardım Pro | Premium</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Montserrat', sans-serif; background: #f0f2f5; }
        .navbar { background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .navbar-brand { font-weight: 800; color: #ff3b3b !important; letter-spacing: -1px; }
        .nav-link { font-weight: 600; color: #333 !important; }
        .btn-yonetim { background: #333; color: white; padding: 8px 20px; border-radius: 30px; }
        footer { background: #333; color: white; padding: 30px 0; margin-top: 50px; text-align: center; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg sticky-top">
        <div class="container">
            <a class="navbar-brand" href="/">İLK YARDIM PRO</a>
            <div class="ms-auto">
                <a class="nav-link d-inline me-3" href="/">Eğitimler</a>
                <a class="nav-link d-inline btn-yonetim" href="/yonetim">Yönetim</a>
            </div>
        </div>
    </nav>
    {% block content %}{% endblock %}
    <footer>
        <small>© 2026 Özel Tasarım Eğitim Platformu</small>
    </footer>
</body>
</html>"""
with open(os.path.join(TEMPLATES_DIR, 'layout.html'), 'w', encoding='utf-8') as f:
    f.write(layout_code)


# 2. INDEX.HTML (SVG İKONLARI GÖMÜYORUZ)
# Burada Jinja2'nin 'set' özelliğini kullanarak SVG'leri değişkenlere atıyoruz.
# Sonra loop içinde doğru SVG'yi çağırıyoruz.
index_code = """{% extends "layout.html" %}
{% block content %}

{% set svg_map = {
    "GENEL": '""" + SVG_GENEL + """',
    "VÜCUT": '""" + SVG_VUCUT + """',
    "TAŞIMA": '""" + SVG_TASIMA + """',
    "OED": '""" + SVG_OED + """',
    "YAŞAM": '""" + SVG_YASAM + """',
    "HAVA": '""" + SVG_HAVA + """',
    "BİLİNÇ": '""" + SVG_BILINC + """',
    "KANAMA": '""" + SVG_KANAMA + """',
    "ŞOK": '""" + SVG_SOK + """',
    "YARALANMA": '""" + SVG_YARALANMA + """',
    "BOĞULMA": '""" + SVG_BOGULMA + """',
    "KIRIK": '""" + SVG_KIRIK + """',
    "HAYVAN": '""" + SVG_HAYVAN + """',
    "ZEHİRLENME": '""" + SVG_ZEHIRLENME + """',
    "YANIK": '""" + SVG_YANIK + """',
    "GÖZ": '""" + SVG_GOZ + """'
} %}

<style>
    .hero-section {
        background: white; padding: 80px 0; text-align: center; margin-bottom: 50px;
    }
    .hero-title { font-weight: 800; font-size: 3rem; color: #1a1a1a; margin-bottom: 10px; }
    
    .svg-card {
        background: white; border-radius: 24px; padding: 25px; height: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex; flex-direction: column; align-items: center;
        text-decoration: none; color: inherit;
    }
    .svg-card:hover {
        transform: translateY(-15px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.1);
    }

    .svg-container {
        width: 100px; height: 100px; margin-bottom: 25px;
        filter: drop-shadow(0 10px 20px rgba(0,0,0,0.1));
        transition: 0.4s;
    }
    .svg-card:hover .svg-container { transform: scale(1.1) rotate(5deg); }

    .card-meta { font-size: 0.8rem; font-weight: 700; color: #999; margin-bottom: 10px; }
    .card-title { font-weight: 700; font-size: 1.25rem; color: #333; margin-bottom: 15px; text-align: center; }
    
    .btn-arrow {
        margin-top: auto; width: 45px; height: 45px; border-radius: 50%;
        background: #f8f9fa; color: #ccc; display: flex; align-items: center; justify-content: center;
        transition: 0.3s; font-size: 1.2rem;
    }
    .svg-card:hover .btn-arrow { background: #ff3b3b; color: white; }
</style>

<div class="hero-section">
    <div class="container">
        <h1 class="hero-title">Hayat Kurtaran Sanat.</h1>
        <p class="lead text-muted">Özel olarak tasarlanmış görsel modüllerle ilk yardımı öğrenin.</p>
    </div>
</div>

<div class="container pb-5">
    <div class="row g-4">
        {% for konu in konular %}
        <div class="col-md-6 col-lg-4 col-xl-3">
            <a href="{{ url_for('konu_detay', id=konu.id) }}" class="svg-card">
                <div class="card-meta">MODÜL {{ konu.sira }}</div>
                
                <div class="svg-container">
                    {% set title_upper = konu.baslik.upper() %}
                    {% set selected_svg = svg_map["GENEL"] %} {% if "GENEL" in title_upper %} {% set selected_svg = svg_map["GENEL"] %}
                    {% elif "VÜCUT" in title_upper %} {% set selected_svg = svg_map["VÜCUT"] %}
                    {% elif "TAŞIMA" in title_upper %} {% set selected_svg = svg_map["TAŞIMA"] %}
                    {% elif "OED" in title_upper %} {% set selected_svg = svg_map["OED"] %}
                    {% elif "YAŞAM" in title_upper %} {% set selected_svg = svg_map["YAŞAM"] %}
                    {% elif "HAVA" in title_upper %} {% set selected_svg = svg_map["HAVA"] %}
                    {% elif "BİLİNÇ" in title_upper %} {% set selected_svg = svg_map["BİLİNÇ"] %}
                    {% elif "KANAMA" in title_upper %} {% set selected_svg = svg_map["KANAMA"] %}
                    {% elif "ŞOK" in title_upper %} {% set selected_svg = svg_map["ŞOK"] %}
                    {% elif "YARALANMA" in title_upper %} {% set selected_svg = svg_map["YARALANMA"] %}
                    {% elif "BOĞULMA" in title_upper %} {% set selected_svg = svg_map["BOĞULMA"] %}
                    {% elif "KIRIK" in title_upper %} {% set selected_svg = svg_map["KIRIK"] %}
                    {% elif "HAYVAN" in title_upper %} {% set selected_svg = svg_map["HAYVAN"] %}
                    {% elif "ZEHİRLENME" in title_upper %} {% set selected_svg = svg_map["ZEHİRLENME"] %}
                    {% elif "YANIK" in title_upper %} {% set selected_svg = svg_map["YANIK"] %}
                    {% elif "GÖZ" in title_upper %} {% set selected_svg = svg_map["GÖZ"] %}
                    {% endif %}
                    
                    {{ selected_svg | safe }}
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
{% endblock %}
"""

with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_code)

print("\n🚀 GITHUB'A SANAT ESERİ YOLLANIYOR...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "GEMINI OZEL CIZIM SVG IKON SETİ (16 ADET)"', shell=True)
subprocess.run("git push", shell=True)
print("✅ İşlem Tamam! Vercel güncellenince site şaheser olacak.")