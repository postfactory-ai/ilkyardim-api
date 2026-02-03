import os
import subprocess
import psycopg2
import json
from datetime import datetime

# ==========================================================
# BURAYA NEON DB KODUNU YAPIŞTIR (Vercel'deki ile aynı)
DATABASE_URL = "postgresql://neondb_owner:npg_OAFxzgdw76ta@ep-long-brook-agzcx4dh-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" 
# ==========================================================

# Renkler
GREEN = '\033[92m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

print(f"{CYAN}🔄 OTOMATİK SENKRONİZASYON BAŞLATILIYOR...{RESET}")
print("-" * 50)

# --- ADIM 1: VERİ GÜVENLİĞİ (CLOUD -> LOCAL YEDEKLEME) ---
def veri_yedekle():
    print(f"{YELLOW}1. Bulut Veritabanı (NeonDB) Yedekleniyor...{RESET}")
    url = DATABASE_URL.replace("postgres://", "postgresql://") if "postgres://" in DATABASE_URL else DATABASE_URL
    
    try:
        conn = psycopg2.connect(url)
        cursor = conn.cursor()
        cursor.execute("SELECT id, baslik, icerik, resim, sira FROM konu ORDER BY sira ASC")
        veriler = cursor.fetchall()
        
        liste = []
        for veri in veriler:
            liste.append({
                "id": veri[0], "baslik": veri[1], "icerik": veri[2], "resim": veri[3], "sira": veri[4]
            })

        # Dosyayı 'son_yedek.json' olarak kaydet (Her seferinde üzerine yazar, en günceli tutar)
        with open("son_yedek.json", 'w', encoding='utf-8') as f:
            json.dump(liste, f, ensure_ascii=False, indent=4)
            
        print(f"{GREEN}✅ Veri Yedeği Alındı! (son_yedek.json){RESET}")
        conn.close()
    except Exception as e:
        print(f"❌ Yedekleme Hatası (Önemli değil, kod devam eder): {e}")

# --- ADIM 2: KOD GÜVENLİĞİ (LOCAL -> CLOUD GÜNCELLEME) ---
def kod_gonder():
    print(f"\n{YELLOW}2. Kod Değişiklikleri Buluta Gönderiliyor (Git & Vercel)...{RESET}")
    
    # Git durumunu kontrol et
    status = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True).stdout
    
    if not status:
        print(f"{GREEN}✅ Değişiklik yok, her şey güncel!{RESET}")
        return

    try:
        # Tarihli mesaj oluştur
        zaman = datetime.now().strftime("%d.%m.%Y %H:%M")
        mesaj = f"AUTO-SYNC: {zaman} Guncellemesi"
        
        subprocess.run("git add -A", shell=True, check=True)
        print("   - Dosyalar paketlendi.")
        
        subprocess.run(f'git commit -m "{mesaj}"', shell=True, check=True)
        print("   - Mühürlendi.")
        
        print("   - Uzaya fırlatılıyor... 🚀")
        subprocess.run("git push", shell=True, check=True)
        
        print(f"\n{GREEN}🎉 SENKRONİZASYON TAMAMLANDI!{RESET}")
        print("   - Veriler: Güvende (Localde yedekli)")
        print("   - Kodlar: Güncel (Vercel'de yayında)")
        
    except Exception as e:
        print(f"❌ Git Hatası: {e}")

if __name__ == "__main__":
    veri_yedekle()
    kod_gonder()
    input("\nÇıkmak için Enter'a bas...")