import os
import subprocess

print("\033[93m🛠️ VERCEL YAPILANDIRMASI MODERNİZE EDİLİYOR...\033[0m")

# YENİ VE MODERN VERCEL.JSON
# "builds" dizisi KALDIRILDI (Hatanın sebebi buydu).
# Sadece "rewrites" kullanıyoruz. Bu sayede Vercel otomatik olarak Python ortamını tanıyacak.
vercel_config = """{
    "version": 2,
    "rewrites": [
        { "source": "/(.*)", "destination": "/app.py" }
    ]
}"""

# Dosyayı Yaz
with open("vercel.json", "w", encoding="utf-8") as f:
    f.write(vercel_config)

print("✅ vercel.json dosyası temizlendi ve güncellendi.")

# Git Push
print("\n🚀 GITHUB'A GÖNDERİLİYOR...")
subprocess.run("git add vercel.json", shell=True)
subprocess.run('git commit -m "FIX: Vercel Legacy Builds Config Kaldirildi"', shell=True)
subprocess.run("git push", shell=True)

print("\n✅ İŞLEM TAMAM!")
print("1. Vercel şimdi projeyi 'Python' olarak otomatik algılayacak.")
print("2. Paneldeki ayarların artık geçerli olacak.")
print("3. Bu işlem Google Login 401 hatasını da çözebilir çünkü Env değişkenleri artık düzgün yüklenecek.")