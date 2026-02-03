import os
import shutil
import subprocess
import time

print("\033[91m🔥 GIT GEÇMİŞİ SIFIRLANIYOR (GÜVENLİK TEMİZLİĞİ)...\033[0m")

REPO_URL = "https://github.com/postfactory-ai/ilkyardim-api.git"

# 1. SUÇLU DOSYAYI SİL (Eğer hala duruyorsa)
if os.path.exists("env_sistemi_kur.py"):
    os.remove("env_sistemi_kur.py")
    print("✅ Suçlu dosya (env_sistemi_kur.py) fiziksel olarak silindi.")

# 2. .GIT KLASÖRÜNÜ SİL (Hafızayı Sıfırla)
# Bu işlem commit geçmişini siler, böylece şifrelerin olduğu eski kayıtlar yok olur.
if os.path.exists(".git"):
    # Windows bazen izin vermez, o yüzden önce salt okunur özelliğini kaldırıyoruz
    def remove_readonly(func, path, excinfo):
        os.chmod(path, 0o777)
        func(path)
        
    shutil.rmtree(".git", onerror=remove_readonly)
    print("✅ Eski Git geçmişi (.git klasörü) tamamen silindi.")
    time.sleep(1) # Dosya sistemi kendine gelsin

# 3. SIFIRDAN GIT KURULUMU
print("✨ Yeni Git yapısı kuruluyor...")
subprocess.run("git init", shell=True)
subprocess.run("git branch -M main", shell=True)
subprocess.run(f"git remote add origin {REPO_URL}", shell=True)

# 4. DOSYALARI EKLE (ARTIK TEMİZ)
# .env dosyası zaten .gitignore içinde olduğu için eklenmeyecek.
print("📦 Dosyalar paketleniyor...")
subprocess.run("git add .", shell=True)
subprocess.run('git commit -m "CLEAN START: Guvenlik Icin Gecmis Sifirlandi"', shell=True)

# 5. ZORLA GÖNDER (FORCE PUSH)
# GitHub'daki eski geçmişi de ezeceğiz.
print("🚀 GitHub'a zorla gönderiliyor (Force Push)...")
result = subprocess.run("git push -u origin main --force", shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print("\n\033[92m✅ OPERASYON BAŞARILI! Kodlar GitHub'a ulaştı.\033[0m")
    print("👉 Geçmişteki şifre hataları silindi.")
    print("👉 Vercel şimdi son haliyle kurulum yapacak.")
else:
    print("\n\033[91m❌ HATA OLUŞTU:\033[0m")
    print(result.stderr)
    print("İnternet bağlantını kontrol et veya GitHub şifreni/tokenini girmen gerekebilir.")