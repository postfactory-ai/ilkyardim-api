import os
import subprocess

# AYARLAR
BASE_DIR = os.getcwd()
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

print("\033[96m🎨 GEMINI MASTERPIECE MODU: 3D, ANIMASYON VE GLASSMORPHISM YÜKLENİYOR...\033[0m")

# --- 3D SVG KOLEKSİYONU (Gölge, Işık ve Hacim Efektli) ---

# 1. GENEL (3D Kalkan ve Artı)
SVG_GENEL = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<path d="M50 15C50 15 85 25 85 50C85 75 50 90 50 90C50 90 15 75 15 50C15 25 50 15 50 15Z" fill="url(#grad_shield)" filter="url(#glow)"/>
<path d="M35 50H65M50 35V65" stroke="white" stroke-width="8" stroke-linecap="round"/>
<defs><linearGradient id="grad_shield" x1="15" y1="15" x2="85" y2="90"><stop stop-color="#4facfe"/><stop offset="1" stop-color="#00f2fe"/></linearGradient></defs>
</svg>"""

# 2. VÜCUT (Anatomi Silüeti)
SVG_VUCUT = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="50" r="40" fill="url(#grad_body)" opacity="0.1"/>
<path d="M50 25C50 25 35 35 35 55C35 75 45 85 50 85C55 85 65 75 65 55C65 35 50 25 50 25Z" fill="url(#grad_body_fill)"/>
<circle cx="50" cy="40" r="5" fill="white" opacity="0.8"/>
<path d="M50 50L60 60M50 50L40 60" stroke="white" stroke-width="3" opacity="0.5"/>
<defs><linearGradient id="grad_body_fill" x1="35" y1="25" x2="65" y2="85"><stop stop-color="#43e97b"/><stop offset="1" stop-color="#38f9d7"/></linearGradient>
<linearGradient id="grad_body" x1="0" y1="0" x2="100" y2="100"><stop stop-color="#43e97b"/><stop offset="1" stop-color="#38f9d7"/></linearGradient></defs>
</svg>"""

# 3. TAŞIMA (Hızlı Ambulans Tekerleği)
SVG_TASIMA = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="50" r="35" stroke="url(#grad_transport)" stroke-width="8" stroke-dasharray="160" stroke-linecap="round"/>
<path d="M50 30V50L65 65" stroke="#FF512F" stroke-width="6" stroke-linecap="round"/>
<circle cx="50" cy="50" r="5" fill="#FF512F"/>
<defs><linearGradient id="grad_transport" x1="0" y1="0" x2="100" y2="100"><stop stop-color="#FF512F"/><stop offset="1" stop-color="#DD2476"/></linearGradient></defs>
</svg>"""

# 4. OED (Elektrik Şoku)
SVG_OED = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M50 10L20 50H45L40 90L70 50H45L50 10Z" fill="url(#grad_oed)" filter="url(#glow)"/>
<defs><linearGradient id="grad_oed" x1="20" y1="10" x2="70" y2="90"><stop stop-color="#f093fb"/><stop offset="1" stop-color="#f5576c"/></linearGradient></defs>
</svg>"""

# 5. YAŞAM (Kalp Atışı)
SVG_YASAM = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M20 50H35L45 20L55 80L65 50H80" stroke="url(#grad_life)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<defs><linearGradient id="grad_life" x1="0" y1="0" x2="100" y2="0"><stop stop-color="#ff9a9e"/><stop offset="1" stop-color="#fecfef"/></linearGradient></defs>
</svg>"""

# 6. HAVA (Nefes Borusu)
SVG_HAVA = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M50 20V50" stroke="#a18cd1" stroke-width="12" stroke-linecap="round"/>
<path d="M30 60C30 75 40 85 50 85C60 85 70 75 70 60" stroke="#fbc2eb" stroke-width="12" stroke-linecap="round"/>
<circle cx="50" cy="20" r="8" fill="#a18cd1"/>
</svg>"""

# 7. BİLİNÇ (Beyin Dalgaları)
SVG_BILINC = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M25 50C25 35 35 25 50 25C65 25 75 35 75 50" stroke="url(#grad_brain)" stroke-width="6" stroke-linecap="round"/>
<circle cx="50" cy="50" r="10" fill="url(#grad_brain)"/>
<path d="M35 70C35 70 45 80 50 80C55 80 65 70 65 70" stroke="url(#grad_brain)" stroke-width="6" stroke-linecap="round"/>
<defs><linearGradient id="grad_brain" x1="0" y1="0" x2="100" y2="100"><stop stop-color="#89f7fe"/><stop offset="1" stop-color="#66a6ff"/></linearGradient></defs>
</svg>"""

# 8. KANAMA (3D Damla)
SVG_KANAMA = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M50 20C50 20 80 50 80 65C80 82 66 95 50 95C34 95 20 82 20 65C20 50 50 20 50 20Z" fill="url(#grad_blood)" filter="url(#glow)"/>
<ellipse cx="60" cy="55" rx="5" ry="10" fill="white" opacity="0.4" transform="rotate(-15 60 55)"/>
<defs><linearGradient id="grad_blood" x1="50" y1="20" x2="50" y2="95"><stop stop-color="#ff0844"/><stop offset="1" stop-color="#ffb199"/></linearGradient></defs>
</svg>"""

# 9. ŞOK (Şimşek)
SVG_SOK = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M55 10L30 45H50L45 90L70 55H50L55 10Z" fill="url(#grad_shock)" stroke="white" stroke-width="2"/>
<defs><linearGradient id="grad_shock" x1="30" y1="10" x2="70" y2="90"><stop stop-color="#a18cd1"/><stop offset="1" stop-color="#fbc2eb"/></linearGradient></defs>
</svg>"""

# 10. YARALANMA (Yara Bandı)
SVG_YARALANMA = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="20" y="35" width="60" height="30" rx="8" fill="#ff9a9e" transform="rotate(-10 50 50)"/>
<rect x="40" y="35" width="20" height="30" fill="white" opacity="0.5" transform="rotate(-10 50 50)"/>
<circle cx="30" cy="50" r="2" fill="#d64c4c"/>
<circle cx="70" cy="42" r="2" fill="#d64c4c"/>
</svg>"""

# 11. BOĞULMA (Can Simidi)
SVG_BOGULMA = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<circle cx="50" cy="50" r="35" stroke="#4facfe" stroke-width="15"/>
<path d="M50 15V25M50 75V85M15 50H25M75 50H85" stroke="#f093fb" stroke-width="4"/>
</svg>"""

# 12. KIRIK (Kemik)
SVG_KIRIK = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M20 30C15 30 15 40 20 40H35L25 60H20C15 60 15 70 20 70H35C40 70 40 60 35 60L45 40H60C65 40 65 30 60 30H20Z" fill="white" stroke="#a18cd1" stroke-width="3"/>
<path d="M40 40L30 60" stroke="#FF512F" stroke-width="2"/>
</svg>"""

# 13. HAYVAN (Yılan Dişi)
SVG_HAYVAN = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M30 30C30 30 40 20 50 20C60 20 70 30 70 30" stroke="#0ba360" stroke-width="5" stroke-linecap="round"/>
<path d="M40 40L35 60M60 40L65 60" stroke="#0ba360" stroke-width="4" stroke-linecap="round"/>
</svg>"""

# 14. ZEHİRLENME (İksir)
SVG_ZEHIRLENME = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M40 30H60L70 80H30L40 30Z" fill="url(#grad_poison)"/>
<rect x="45" y="15" width="10" height="15" fill="#333"/>
<circle cx="45" cy="50" r="4" fill="white" opacity="0.5"/>
<circle cx="55" cy="65" r="6" fill="white" opacity="0.3"/>
<defs><linearGradient id="grad_poison" x1="0" y1="0" x2="0" y2="100"><stop stop-color="#434343"/><stop offset="1" stop-color="#000000"/></linearGradient></defs>
</svg>"""

# 15. YANIK (Alev)
SVG_YANIK = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M50 15C50 15 75 45 75 65C75 80 65 90 50 90C35 90 25 80 25 65C25 45 50 15 50 15Z" fill="url(#grad_fire)"/>
<path d="M50 35C50 35 60 55 60 65C60 70 55 75 50 75C45 75 40 70 40 65C40 55 50 35 50 35Z" fill="#ff9a9e"/>
<defs><linearGradient id="grad_fire" x1="50" y1="90" x2="50" y2="15"><stop stop-color="#fa709a"/><stop offset="1" stop-color="#fee140"/></linearGradient></defs>
</svg>"""

# 16. GÖZ (Göz Küresi)
SVG_GOZ = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M15 50C15 50 30 25 50 25C70 25 85 50 85 50C85 50 70 75 50 75C30 75 15 50 15 50Z" fill="white" stroke="#66a6ff" stroke-width="3"/>
<circle cx="50" cy="50" r="15" fill="#66a6ff"/>
<circle cx="50" cy="50" r="6" fill="#000"/>
</svg>"""


# ------------------------------------------------------------------

# 2. INDEX.HTML OLUŞTURMA (Modern Animasyonlu CSS)
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
    /* ARKA PLAN */
    body {
        background-color: #f0f4f8;
        background-image: radial-gradient(#e2e8f0 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* HERO ALANI */
    .hero-section {
        background: white;
        padding: 100px 0 80px 0;
        border-bottom-left-radius: 50px;
        border-bottom-right-radius: 50px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.03);
        text-align: center;
        margin-bottom: 60px;
        position: relative;
        overflow: hidden;
    }
    .hero-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 800;
        font-size: 3.5rem;
        background: linear-gradient(135deg, #1a1a1a 0%, #d32f2f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    .hero-tag {
        background: #ffebee; color: #d32f2f;
        padding: 8px 16px; border-radius: 30px;
        font-weight: 700; font-size: 0.8rem; letter-spacing: 1px;
        display: inline-block; margin-bottom: 20px;
    }

    /* GLASSMORPHISM KART */
    .art-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 30px;
        padding: 30px;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-decoration: none;
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.02);
    }
    
    .art-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 30px 60px rgba(211, 47, 47, 0.15);
        background: white;
        border-color: #ffcdd2;
    }

    /* 3D İKON KONTEYNER */
    .icon-stage {
        width: 120px;
        height: 120px;
        margin-bottom: 20px;
        filter: drop-shadow(0 15px 25px rgba(0,0,0,0.1));
        transition: transform 0.5s ease;
        animation: float 6s ease-in-out infinite;
    }
    
    .art-card:hover .icon-stage {
        transform: scale(1.2) rotate(5deg);
        filter: drop-shadow(0 20px 30px rgba(211, 47, 47, 0.3));
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    /* TYPOGRAPHY */
    .card-id {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem; font-weight: 800; color: #cbd5e1;
        letter-spacing: 2px; margin-bottom: 5px;
    }
    .card-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 700; font-size: 1.4rem; color: #1e293b;
        margin-bottom: 10px; text-align: center;
    }

    /* BUTON */
    .btn-circle {
        margin-top: auto;
        width: 50px; height: 50px;
        border-radius: 50%;
        background: #f1f5f9; color: #94a3b8;
        display: flex; align-items: center; justify-content: center;
        transition: 0.4s;
        font-size: 1.2rem;
    }
    .art-card:hover .btn-circle {
        background: #d32f2f; color: white;
        transform: rotate(-45deg);
    }

</style>

<div class="hero-section">
    <div class="container">
        <span class="hero-tag">PREMIUM SÜRÜM 5.0</span>
        <h1 class="hero-title">İlk Yardım Sanatı.</h1>
        <p class="text-muted fs-5">3D Görselleştirme ile öğrenmeyi kolaylaştırın.</p>
    </div>
</div>

<div class="container pb-5">
    <div class="row g-4">
        {% for konu in konular %}
        <div class="col-md-6 col-lg-4 col-xl-3">
            <a href="{{ url_for('konu_detay', id=konu.id) }}" class="art-card">
                <div class="card-id">MODÜL {{ "%02d" % konu.sira }}</div>
                
                <div class="icon-stage">
                    {% set title_upper = konu.baslik.upper() %}
                    {% set selected_svg = svg_map["GENEL"] %}
                    
                    {% if "GENEL" in title_upper %} {% set selected_svg = svg_map["GENEL"] %}
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
                
                <div class="btn-circle">
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

print("\n🚀 GITHUB'A YOLLANIYOR (MASTERPIECE SVG EDITION)...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "TASARIM FINAL: 3D SVG, Animasyon ve Glassmorphism"', shell=True)
subprocess.run("git push", shell=True)
print("✅ İşlem Tamam! Şimdi siteye gir ve o 'Hadi Ordan' lafını geri al :)")