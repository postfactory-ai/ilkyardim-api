import os
import subprocess

# AYARLAR
BASE_DIR = os.getcwd()
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
APP_PATH = os.path.join(BASE_DIR, 'app.py')

print("\033[93m🔍 ARAMA FONKSİYONU TAMİR EDİLİYOR...\033[0m")

# 1. APP.PY ROTASINI DÜZELT
with open(APP_PATH, 'r', encoding='utf-8') as f:
    app_content = f.read()

# Arama rotası kodu
search_route_code = """
@app.route('/arama')
def arama():
    kelime = request.args.get('q', '')
    if kelime:
        sonuclar = Konu.query.filter(
            or_(
                Konu.baslik.ilike(f'%{kelime}%'),
                Konu.icerik.ilike(f'%{kelime}%')
            )
        ).all()
    else:
        sonuclar = []
    return render_template('arama.html', kelime=kelime, sonuclar=sonuclar)
"""

if "@app.route('/arama')" not in app_content:
    # 'app = Flask(__name__)' satırından sonraya değil, route'ların olduğu yere ekleyelim.
    # En güvenli yer: index rotasının hemen öncesi veya sonrası.
    if "@app.route('/')" in app_content:
        app_content = app_content.replace("@app.route('/')", search_route_code + "\n@app.route('/')")
        
        with open(APP_PATH, 'w', encoding='utf-8') as f:
            f.write(app_content)
        print("✅ app.py güncellendi: '/arama' rotası eklendi.")
    else:
        print("⚠️ app.py içinde index rotası bulunamadı, manuel ekleme gerekebilir.")
else:
    print("ℹ️ app.py içinde '/arama' rotası zaten var. (Yine de şablonu kontrol edeceğiz)")


# 2. ARAMA.HTML ŞABLONU (Sonuç Sayfası)
arama_html = """
{% extends "layout.html" %}

{% block content %}
<div class="container mt-5">
    <h3 class="fw-bold mb-4">
        <i class="ph-duotone ph-magnifying-glass text-danger"></i> 
        "{{ kelime }}" için Arama Sonuçları
    </h3>

    {% if sonuclar %}
        <div class="row g-3">
            {% for konu in sonuclar %}
            <div class="col-md-6">
                <a href="{{ url_for('konu_detay', id=konu.id) }}" class="text-decoration-none text-dark">
                    <div class="card border-0 shadow-sm h-100 p-3">
                        <div class="d-flex align-items-center gap-3">
                            <div class="bg-light rounded-circle p-3">
                                <i class="ph-duotone ph-first-aid text-danger fs-4"></i>
                            </div>
                            <div>
                                <h5 class="fw-bold m-0">{{ konu.baslik }}</h5>
                                <small class="text-muted">MODÜL {{ konu.sira }}</small>
                            </div>
                            <i class="ph-bold ph-caret-right ms-auto text-muted"></i>
                        </div>
                    </div>
                </a>
            </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-warning text-center p-5 rounded-4">
            <i class="ph-duotone ph-warning-circle fs-1 mb-3"></i>
            <h4>Sonuç Bulunamadı</h4>
            <p>Farklı bir anahtar kelime deneyin (Örn: Yanık, Kırık, Kalp).</p>
            <a href="/" class="btn btn-outline-dark mt-2">Ana Sayfaya Dön</a>
        </div>
    {% endif %}
</div>
{% endblock %}
"""

with open(os.path.join(TEMPLATES_DIR, 'arama.html'), 'w', encoding='utf-8') as f:
    f.write(arama_html)
print("✅ arama.html şablonu oluşturuldu.")


# 3. GITHUB PUSH
print("\n🚀 TAMİR PAKETİ GITHUB'A YOLLANIYOR...")
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "FIX: Arama Rotasi ve Sablonu Eklendi"', shell=True)
subprocess.run("git push", shell=True)
print("✅ İşlem Tamam! Vercel güncellenince arama çalışacak.")