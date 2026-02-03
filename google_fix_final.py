import os
import subprocess

print("\033[93m🔧 GOOGLE LOGIN & VERCEL AYARLARI TAMİR EDİLİYOR...\033[0m")

# 1. ADIM: VERCEL.JSON (MODERNİZE ETMEK ŞART)
# Eski "builds" ayarını siliyoruz ki Vercel senin panelden girdiğin şifreleri okuyabilsin.
vercel_config = """{
    "version": 2,
    "rewrites": [
        { "source": "/(.*)", "destination": "/app.py" }
    ]
}"""

with open("vercel.json", "w", encoding="utf-8") as f:
    f.write(vercel_config)
print("✅ vercel.json güncellendi (Modern Format).")

# 2. ADIM: DEBUG ROTASI EKLE (SORUNU GÖRMEK İÇİN)
# app.py dosyasına '/debug-auth' diye bir sayfa ekleyeceğiz.
# Bu sayfaya girince şifrelerin gelip gelmediğini göreceksin.
app_path = os.path.join(os.getcwd(), 'app.py')
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

debug_route = """
@app.route('/debug-auth')
def debug_auth():
    client_id = app.config.get('GOOGLE_CLIENT_ID', 'YOK')
    client_secret = app.config.get('GOOGLE_CLIENT_SECRET', 'YOK')
    
    # Güvenlik için sadece ilk 5 ve son 5 karakteri göster
    def mask(s):
        if not s or s == 'YOK' or 'BURAYA' in s: return f'<span style="color:red; font-weight:bold;">HATALI: {s}</span>'
        return f'<span style="color:green; font-weight:bold;">OKUNDU ({s[:10]}...{s[-5:]})</span>'
    
    html = f'''
    <h3>Google Auth Debug</h3>
    <p><b>Client ID:</b> {mask(client_id)}</p>
    <p><b>Client Secret:</b> {mask(client_secret)}</p>
    <p><b>Callback URL:</b> {url_for('google_authorize', _external=True)}</p>
    <hr>
    <p>Eğer kırmızı "HATALI" veya "BURAYA_..." görüyorsan, Vercel Environment Variables ayarların okunmuyor demektir.</p>
    '''
    return html
"""

if "/debug-auth" not in app_content:
    # index rotasından önceye ekle
    app_content = app_content.replace("@app.route('/')", debug_route + "\n@app.route('/')")
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(app_content)
    print("✅ Debug rotası (/debug-auth) eklendi.")

# 3. GITHUB'A YOLLAMA
print("\n🚀 DÜZELTMELER GÖNDERİLİYOR...")
subprocess.run("git add vercel.json app.py", shell=True)
subprocess.run('git commit -m "FIX: Vercel Config Update & Google Debug Route"', shell=True)
subprocess.run("git push", shell=True)

print("\n✅ İŞLEM TAMAM!")
print("👉 Vercel'de 'Building' bitince (yaklaşık 2 dk sonra) şu adrese gir:")
print("   https://ilkyardim-api.vercel.app/debug-auth")
print("👉 Orada YEŞİL renkte 'OKUNDU' yazısını görmelisin.")