import os
import subprocess

# AYARLAR
BASE_DIR = os.getcwd()
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

print("\033[92m🚑 SİSTEM REVİZYONU: QUIZ + SOS + YÜZEN ARAMA + 3D İKONLAR...\033[0m")

# --- 3D SVG İKONLAR (GERİ GELDİ) ---
SVG_GENEL = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5" result="coloredBlur"/><feMerge><feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/></feMerge></filter><path d="M50 15C50 15 85 25 85 50C85 75 50 90 50 90C50 90 15 75 15 50C15 25 50 15 50 15Z" fill="url(#grad_shield)" filter="url(#glow)"/><path d="M35 50H65M50 35V65" stroke="white" stroke-width="8" stroke-linecap="round"/><defs><linearGradient id="grad_shield" x1="15" y1="15" x2="85" y2="90"><stop stop-color="#4facfe"/><stop offset="1" stop-color="#00f2fe"/></linearGradient></defs></svg>"""
SVG_VUCUT = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M50 25C50 25 35 35 35 55C35 75 45 85 50 85C55 85 65 75 65 55C65 35 50 25 50 25Z" fill="url(#grad_body)"/><circle cx="50" cy="40" r="5" fill="white" opacity="0.8"/><defs><linearGradient id="grad_body" x1="0" y1="0" x2="100" y2="100"><stop stop-color="#43e97b"/><stop offset="1" stop-color="#38f9d7"/></linearGradient></defs></svg>"""
SVG_TASIMA = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="35" stroke="url(#grad_transport)" stroke-width="8" stroke-dasharray="160" stroke-linecap="round"/><path d="M50 30V50L65 65" stroke="#FF512F" stroke-width="6" stroke-linecap="round"/><defs><linearGradient id="grad_transport" x1="0" y1="0" x2="100" y2="100"><stop stop-color="#FF512F"/><stop offset="1" stop-color="#DD2476"/></linearGradient></defs></svg>"""
SVG_OED = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M50 10L20 50H45L40 90L70 50H45L50 10Z" fill="url(#grad_oed)" filter="url(#glow)"/><defs><linearGradient id="grad_oed" x1="20" y1="10" x2="70" y2="90"><stop stop-color="#f093fb"/><stop offset="1" stop-color="#f5576c"/></linearGradient></defs></svg>"""
SVG_YASAM = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 50H35L45 20L55 80L65 50H80" stroke="url(#grad_life)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><defs><linearGradient id="grad_life" x1="0" y1="0" x2="100" y2="0"><stop stop-color="#ff9a9e"/><stop offset="1" stop-color="#fecfef"/></linearGradient></defs></svg>"""
SVG_HAVA = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M50 20V50" stroke="#a18cd1" stroke-width="12" stroke-linecap="round"/><path d="M30 60C30 75 40 85 50 85C60 85 70 75 70 60" stroke="#fbc2eb" stroke-width="12" stroke-linecap="round"/><circle cx="50" cy="20" r="8" fill="#a18cd1"/></svg>"""
SVG_BILINC = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M25 50C25 35 35 25 50 25C65 25 75 35 75 50" stroke="url(#grad_brain)" stroke-width="6" stroke-linecap="round"/><circle cx="50" cy="50" r="10" fill="url(#grad_brain)"/><defs><linearGradient id="grad_brain" x1="0" y1="0" x2="100" y2="100"><stop stop-color="#89f7fe"/><stop offset="1" stop-color="#66a6ff"/></linearGradient></defs></svg>"""
SVG_KANAMA = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M50 20C50 20 80 50 80 65C80 82 66 95 50 95C34 95 20 82 20 65C20 50 50 20 50 20Z" fill="url(#grad_blood)" filter="url(#glow)"/><defs><linearGradient id="grad_blood" x1="50" y1="20" x2="50" y2="95"><stop stop-color="#ff0844"/><stop offset="1" stop-color="#ffb199"/></linearGradient></defs></svg>"""
SVG_SOK = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M55 10L30 45H50L45 90L70 55H50L55 10Z" fill="url(#grad_shock)" stroke="white" stroke-width="2"/><defs><linearGradient id="grad_shock" x1="30" y1="10" x2="70" y2="90"><stop stop-color="#a18cd1"/><stop offset="1" stop-color="#fbc2eb"/></linearGradient></defs></svg>"""
SVG_YARALANMA = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="20" y="35" width="60" height="30" rx="8" fill="#ff9a9e" transform="rotate(-10 50 50)"/><rect x="40" y="35" width="20" height="30" fill="white" opacity="0.5" transform="rotate(-10 50 50)"/><circle cx="30" cy="50" r="2" fill="#d64c4c"/><circle cx="70" cy="42" r="2" fill="#d64c4c"/></svg>"""
SVG_BOGULMA = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="50" cy="50" r="35" stroke="#4facfe" stroke-width="15"/><path d="M50 15V25M50 75V85M15 50H25M75 50H85" stroke="#f093fb" stroke-width="4"/></svg>"""
SVG_KIRIK = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M20 30C15 30 15 40 20 40H35L25 60H20C15 60 15 70 20 70H35C40 70 40 60 35 60L45 40H60C65 40 65 30 60 30H20Z" fill="white" stroke="#a18cd1" stroke-width="3"/><path d="M40 40L30 60" stroke="#FF512F" stroke-width="2"/></svg>"""
SVG_HAYVAN = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M30 30C30 30 40 20 50 20C60 20 70 30 70 30" stroke="#0ba360" stroke-width="5" stroke-linecap="round"/><path d="M40 40L35 60M60 40L65 60" stroke="#0ba360" stroke-width="4" stroke-linecap="round"/></svg>"""
SVG_ZEHIRLENME = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M40 30H60L70 80H30L40 30Z" fill="url(#grad_poison)"/><rect x="45" y="15" width="10" height="15" fill="#333"/><defs><linearGradient id="grad_poison" x1="0" y1="0" x2="0" y2="100"><stop stop-color="#434343"/><stop offset="1" stop-color="#000000"/></linearGradient></defs></svg>"""
SVG_YANIK = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M50 15C50 15 75 45 75 65C75 80 65 90 50 90C35 90 25 80 25 65C25 45 50 15 50 15Z" fill="url(#grad_fire)"/><defs><linearGradient id="grad_fire" x1="50" y1="90" x2="50" y2="15"><stop stop-color="#fa709a"/><stop offset="1" stop-color="#fee140"/></linearGradient></defs></svg>"""
SVG_GOZ = """<svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M15 50C15 50 30 25 50 25C70 25 85 50 85 50C85 50 70 75 50 75C30 75 15 50 15 50Z" fill="white" stroke="#66a6ff" stroke-width="3"/><circle cx="50" cy="50" r="15" fill="#66a6ff"/><circle cx="50" cy="50" r="6" fill="#000"/></svg>"""


# 1. APP.PY (Quiz Rotası Eklendi)
app_path = os.path.join(BASE_DIR, 'app.py')
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

# Quiz rotası yoksa ekle
if "/quiz" not in app_content:
    new_route = """
# QUIZ ROTASI
@app.route('/quiz')
def quiz_page():
    return render_template('quiz.html')
"""
    # Dosyanın sonundaki if __name__ öncesine ekle
    app_content = app_content.replace("if __name__ == '__main__':", new_route + "\nif __name__ == '__main__':")
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("✅ app.py güncellendi: Quiz rotası eklendi.")


# 2. LAYOUT.HTML (Yüzen Arama Butonu)
layout_code = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Acil Asistanı</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://unpkg.com/@phosphor-icons/web"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Outfit', sans-serif; background-color: #fcfcfc; color: #1e293b; padding-bottom: 80px; }
        
        /* Floating Search Button (FAB) */
        .fab-search {
            position: fixed; bottom: 90px; right: 20px;
            width: 60px; height: 60px;
            background: #d32f2f; color: white;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 24px;
            box-shadow: 0 10px 25px rgba(211, 47, 47, 0.4);
            z-index: 1000; cursor: pointer; transition: 0.3s;
        }
        .fab-search:hover { transform: scale(1.1); background: #b71c1c; }

        /* Full Screen Search Overlay */
        .search-overlay {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255,255,255,0.95); backdrop-filter: blur(10px);
            z-index: 2000; display: none;
            flex-direction: column; align-items: center; justify-content: flex-start;
            padding-top: 100px;
        }
        .search-overlay.active { display: flex; animation: fadeIn 0.3s; }
        
        .big-search-input {
            width: 80%; font-size: 1.5rem; padding: 15px;
            border: none; border-bottom: 3px solid #d32f2f;
            background: transparent; outline: none; text-align: center;
        }
        .close-search {
            position: absolute; top: 30px; right: 30px;
            font-size: 2rem; cursor: pointer; color: #333;
        }

        /* Alt Navigasyon */
        .bottom-nav {
            position: fixed; bottom: 0; left: 0; width: 100%;
            background: white; border-top: 1px solid #f1f5f9;
            display: flex; justify-content: space-around; padding: 12px 0;
            z-index: 999; box-shadow: 0 -5px 20px rgba(0,0,0,0.03);
        }
        .nav-item-m { text-align: center; color: #94a3b8; text-decoration: none; font-size: 0.7rem; flex: 1; font-weight: 600; }
        .nav-item-m i { display: block; font-size: 1.6rem; margin-bottom: 4px; }
        .nav-item-m.active { color: #d32f2f; }
        
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    </style>
</head>
<body>
    
    <div class="fab-search" onclick="toggleSearch()">
        <i class="ph-bold ph-magnifying-glass"></i>
    </div>

    <div class="search-overlay" id="searchOverlay">
        <i class="ph-bold ph-x close-search" onclick="toggleSearch()"></i>
        <h3 class="fw-bold mb-4">Ne arıyorsun?</h3>
        <input type="text" id="liveSearch" class="big-search-input" placeholder="Yanık, Kırık, Kalp...">
        <div id="searchResults" class="mt-5 container text-center"></div>
    </div>

    {% block content %}{% endblock %}

    <div class="bottom-nav">
        <a href="/" class="nav-item-m active"><i class="ph-duotone ph-house"></i>Ana Sayfa</a>
        <a href="/quiz" class="nav-item-m"><i class="ph-duotone ph-exam"></i>Quiz</a>
        <a href="/profil" class="nav-item-m"><i class="ph-duotone ph-user"></i>Profil</a>
        {% if current_user.is_authenticated and current_user.username == 'admin' %}
        <a href="/yonetim" class="nav-item-m"><i class="ph-duotone ph-lock-key"></i>Yönetim</a>
        {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function toggleSearch() {
            let overlay = document.getElementById('searchOverlay');
            if (overlay.style.display === 'flex') {
                overlay.style.display = 'none';
            } else {
                overlay.style.display = 'flex';
                document.getElementById('liveSearch').focus();
            }
        }

        // Live Search Mantığı (Sayfadaki kartları arar)
        document.getElementById('liveSearch').addEventListener('keyup', function(e) {
            let term = e.target.value.toLowerCase();
            // Bu kısım index.html'deki kart verilerini arayacak (istemci tarafı)
            // Detaylı arama için API isteği de atılabilir ama şimdilik hızlı çözüm:
            // Kullanıcı enter'a basarsa /arama sayfasına git
            if(e.key === 'Enter') {
                window.location.href = '/arama?q=' + term;
            }
        });
    </script>
</body>
</html>"""
with open(os.path.join(TEMPLATES_DIR, 'layout.html'), 'w', encoding='utf-8') as f:
    f.write(layout_code)


# 3. INDEX.HTML (3D SVG Entegreli & Premium Kırmızı Tema)
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
    .header-area {
        padding: 40px 20px 30px 20px;
        background: white;
        border-bottom-left-radius: 30px;
        border-bottom-right-radius: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.03);
    }
    .user-greet { font-size: 0.9rem; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .main-slogan { font-size: 1.8rem; font-weight: 800; color: #1e293b; line-height: 1.2; margin-top: 5px; }
    
    /* ACTIONS */
    .actions-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: -30px; padding: 0 20px; position: relative; z-index: 10; }
    .act-btn {
        background: white; border-radius: 20px; padding: 15px 5px;
        display: flex; flex-direction: column; align-items: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05); text-decoration: none;
        transition: 0.2s; border: 1px solid white;
    }
    .act-btn:active { transform: scale(0.95); }
    .act-icon { font-size: 1.8rem; margin-bottom: 5px; }
    .act-label { font-size: 0.7rem; font-weight: 800; color: #64748b; }
    
    /* Renk Kodları */
    .act-call { color: #ef4444; } /* Kırmızı */
    .act-sos { color: #f97316; } /* Turuncu */
    .act-quiz { color: #3b82f6; } /* Mavi */
    .act-map { color: #22c55e; } /* Yeşil */

    /* KONU KARTLARI */
    .topic-card {
        background: white; border-radius: 24px; padding: 25px;
        position: relative; overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        text-decoration: none; color: inherit; height: 100%;
        display: flex; flex-direction: column; align-items: center; text-align: center;
        border: 1px solid #f8fafc;
    }
    .topic-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(211, 47, 47, 0.1); border-color: #fca5a5; }
    
    .svg-wrapper { width: 90px; height: 90px; margin-bottom: 20px; transition: 0.5s; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1)); }
    .topic-card:hover .svg-wrapper { transform: scale(1.15) rotate(5deg); }
    
    .t-title { font-weight: 700; font-size: 1.2rem; color: #333; margin-bottom: 5px; line-height: 1.3; }
    .t-meta { font-size: 0.75rem; font-weight: 700; color: #cbd5e1; letter-spacing: 1px; }

</style>

<div class="header-area">
    <div class="container">
        <div class="user-greet">{% if current_user.is_authenticated %}{{ current_user.username }}{% else %}Misafir{% endif %}</div>
        <h1 class="main-slogan">Acil Durum<br><span style="color:#d32f2f">Asistanı.</span></h1>
    </div>
</div>

<div class="container actions-row">
    <a href="tel:112" class="act-btn act-call">
        <i class="ph-duotone ph-phone-call act-icon"></i>
        <span class="act-label">112</span>
    </a>
    <a href="#" onclick="sendSOS()" class="act-btn act-sos">
        <i class="ph-duotone ph-warning-circle act-icon"></i>
        <span class="act-label">SOS</span>
    </a>
    <a href="/quiz" class="act-btn act-quiz">
        <i class="ph-duotone ph-exam act-icon"></i>
        <span class="act-label">QUIZ</span>
    </a>
    <a href="#" onclick="openMap()" class="act-btn act-map">
        <i class="ph-duotone ph-map-pin act-icon"></i>
        <span class="act-label">KONUM</span>
    </a>
</div>

<div class="container mt-5 pb-5">
    <h6 class="fw-bold text-muted ps-2 mb-3 small">EĞİTİM MODÜLLERİ</h6>
    <div class="row g-3">
        {% for konu in konular %}
        <div class="col-6 col-md-4 col-lg-3">
            <a href="{{ url_for('konu_detay', id=konu.id) }}" class="topic-card">
                <div class="svg-wrapper">
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
                <span class="t-meta">MODÜL {{ "%02d" % konu.sira }}</span>
                <h3 class="t-title">{{ konu.baslik }}</h3>
            </a>
        </div>
        {% endfor %}
    </div>
</div>

<script>
    function sendSOS() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                let lat = position.coords.latitude;
                let lon = position.coords.longitude;
                let msg = `ACİL DURUM! Yardıma ihtiyacım var. Konumum: https://www.google.com/maps?q=${lat},${lon}`;
                window.open(`https://wa.me/?text=${encodeURIComponent(msg)}`, '_blank');
            }, function(error) {
                alert("Konum alınamadı. Lütfen GPS izni verin.");
            });
        } else {
            alert("Tarayıcınız konum servisini desteklemiyor.");
        }
    }

    function openMap() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                let lat = position.coords.latitude;
                let lon = position.coords.longitude;
                window.open(`https://www.google.com/maps?q=${lat},${lon}`, '_blank');
            });
        }
    }
</script>
{% endblock %}"""
with open(os.path.join(TEMPLATES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(index_code)


# 4. QUIZ.HTML (JS Tabanlı Sınav Sistemi)
quiz_code = """
{% extends "layout.html" %}
{% block content %}
<div class="container mt-4">
    <div class="card border-0 shadow-sm p-4 text-center" id="quiz-box">
        <h4 class="fw-bold mb-3" id="q-text">Soru Yükleniyor...</h4>
        <div class="d-grid gap-2 mt-4" id="options">
            </div>
        <div class="mt-4 text-muted small">
            Soru: <span id="q-index">1</span> / <span id="q-total">5</span>
        </div>
    </div>
    
    <div class="card border-0 shadow-sm p-5 text-center d-none" id="result-box">
        <i class="ph-duotone ph-trophy text-warning" style="font-size: 4rem;"></i>
        <h2 class="fw-bold mt-3">Tebrikler!</h2>
        <p class="lead">Puanınız: <span id="score" class="fw-bold text-danger">0</span></p>
        <button onclick="location.reload()" class="btn btn-dark mt-3">Tekrar Dene</button>
    </div>
</div>

<script>
    const questions = [
        { q: "Yetişkin bir insanda kalp masajı basısı göğüs kemiğini kaç cm aşağı indirmelidir?", a: ["2 cm", "5 cm", "8 cm", "10 cm"], correct: 1 },
        { q: "Aşağıdakilerden hangisi şok belirtisidir?", a: ["Yüzde kızarıklık", "Hızlı ve zayıf nabız", "Sıcak cilt", "Yavaş solunum"], correct: 1 },
        { q: "Burun kanamasında yapılması gereken ilk yardım nedir?", a: ["Başı geriye yaslamak", "Burun kanatlarını sıkıp öne eğilmek", "Sırt üstü yatmak", "Burnu yıkamak"], correct: 1 },
        { q: "112 aranırken verilmesi gereken en önemli bilgi nedir?", a: ["Hastanın adı", "Adres tarifi", "Olayın tanımı ve konum", "Arayanın kimliği"], correct: 2 },
        { q: "OED (Otomatik Şok Cihazı) hangi durumda kullanılır?", a: ["Kırıklarda", "Yanıklarda", "Kalp durmasında", "Zehirlenmede"], correct: 2 }
    ];

    let currentQ = 0;
    let score = 0;

    function loadQuestion() {
        if(currentQ >= questions.length) {
            document.getElementById('quiz-box').classList.add('d-none');
            document.getElementById('result-box').classList.remove('d-none');
            document.getElementById('score').innerText = score * 20;
            return;
        }
        let q = questions[currentQ];
        document.getElementById('q-text').innerText = q.q;
        document.getElementById('q-index').innerText = currentQ + 1;
        document.getElementById('q-total').innerText = questions.length;
        
        let optsDiv = document.getElementById('options');
        optsDiv.innerHTML = "";
        
        q.a.forEach((opt, index) => {
            let btn = document.createElement('button');
            btn.className = "btn btn-outline-dark py-3 fw-bold text-start ps-4";
            btn.innerText = opt;
            btn.onclick = () => checkAnswer(index);
            optsDiv.appendChild(btn);
        });
    }

    function checkAnswer(index) {
        if(index === questions[currentQ].correct) {
            score++;
            alert("✅ Doğru!");
        } else {
            alert("❌ Yanlış!");
        }
        currentQ++;
        loadQuestion();
    }

    loadQuestion();
</script>
{% endblock %}
"""
with open(os.path.join(TEMPLATES_DIR, 'quiz.html'), 'w', encoding='utf-8') as f:
    f.write(quiz_code)


print("\n🚀 GIT & VERCEL GÜNCELLEMESİ BAŞLIYOR...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "FINAL REVIZYON: Quiz + SOS + Floating Search + 3D Icons"', shell=True)
subprocess.run("git push", shell=True)
print("✅ İşlem Tamam! Vercel'i bekle ve siteyi yenile.")