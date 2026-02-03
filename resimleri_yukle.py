import psycopg2

# ==========================================================
# BURAYA NEON DB ADRESİNİ YAPIŞTIR
DATABASE_URL = "postgresql://neondb_owner:npg_OAFxzgdw76ta@ep-long-brook-agzcx4dh-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" 
# ==========================================================

# Konulara Özel Resim Linkleri (Unsplash)
RESIMLER = {
    "I. GENEL İLK YARDIM BİLGİLERİ": "https://images.unsplash.com/photo-1516574187841-693083f05b12?auto=format&fit=crop&w=500&q=80",
    "II. VÜCUT SİSTEMLERİ": "https://images.unsplash.com/photo-1530210124550-912dc1381cb8?auto=format&fit=crop&w=500&q=80", # Anatomi
    "III. ACİL TAŞIMA TEKNİKLERİ": "https://images.unsplash.com/photo-1588611842858-2947df332309?auto=format&fit=crop&w=500&q=80", # Sedye/Ambulans
    "IV. OTOMATİK EKSTERNAL DEFİBRİLATÖR (OED) KULLANIMI": "https://images.unsplash.com/photo-1576091160550-2187d80aeff2?auto=format&fit=crop&w=500&q=80", # OED Cihazı
    "V. TEMEL YAŞAM DESTEĞİ": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=500&q=80", # CPR / Kalp Masajı
    "VI. HAVA YOLU TIKANIKLIĞINDA İLK YARDIM": "https://plus.unsplash.com/premium_photo-1661766572565-515d914b14d3?auto=format&fit=crop&w=500&q=80", # Boğaz/Nefes
    "VII. BİLİNÇ BOZUKLUKLARINDA VE CİDDİ HASTALIK DURUMLARINDA İLK YARDIM": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&w=500&q=80", # Hasta yatak
    "VIII. KANAMALARDA İLK YARDIM": "https://images.unsplash.com/photo-1616117326884-3c467a783786?auto=format&fit=crop&w=500&q=80", # Kan/Bandaj
    "IX. ŞOK VE GÖĞÜS AĞRISINDA İLK YARDIM": "https://images.unsplash.com/photo-1584362917165-526a968579e8?auto=format&fit=crop&w=500&q=80", # Kalp ağrısı
    "X. YARALANMALARDA İLK YARDIM": "https://images.unsplash.com/photo-1579165466741-7f35a4755657?auto=format&fit=crop&w=500&q=80", # Yara bandı
    "XI. BOĞULMALARDA İLK YARDIM": "https://images.unsplash.com/photo-1542614471-001ddf2b7219?auto=format&fit=crop&w=500&q=80", # Su/Deniz
    "XII. KIRIK, ÇIKIK VE BURKULMALARDA İLK YARDIM": "https://images.unsplash.com/photo-1563214436-b63e806798a7?auto=format&fit=crop&w=500&q=80", # Röntgen/Kemik
    "XIII. HAYVAN ISIRIKLARI ve BÖCEK SOKMALARINDA İLK YARDIM": "https://images.unsplash.com/photo-1562957138-16dc5c2d3340?auto=format&fit=crop&w=500&q=80", # Arı/Böcek
    "XIV. ZEHİRLENMELERDE İLK YARDIM": "https://images.unsplash.com/photo-1607569707101-1e247b973523?auto=format&fit=crop&w=500&q=80", # İlaç/Zehir
    "XV. YANIK, SOĞUK VE SICAK ACİLLERİNDE İLK YARDIM": "https://images.unsplash.com/photo-1626292723326-62025f0e9b25?auto=format&fit=crop&w=500&q=80", # Ateş/Yanık
    "XVI. GÖZE, KULAĞA, BURUNA YABANCI CİSİM KAÇMASI VE YUTULAN YABANCI CİSİMLERDE İLK YARDIM": "https://images.unsplash.com/photo-1625515234909-54b1f4870f44?auto=format&fit=crop&w=500&q=80" # Göz/Muayene
}

def resimleri_yukle():
    print("⏳ NeonDB'ye bağlanılıyor...")
    
    final_db_url = DATABASE_URL.replace("postgres://", "postgresql://") if "postgres://" in DATABASE_URL else DATABASE_URL
    
    try:
        conn = psycopg2.connect(final_db_url)
        cursor = conn.cursor()
        
        # Sütun yoksa oluştur (Garanti olsun)
        try:
            cursor.execute("ALTER TABLE konu ADD COLUMN resim VARCHAR(500)")
            conn.commit()
            print("✅ 'resim' sütunu tabloya eklendi.")
        except:
            conn.rollback() # Zaten varsa hata verir, devam et
            print("ℹ️ 'resim' sütunu zaten var.")

        print("📸 Resimler güncelleniyor...")

        for baslik, url in RESIMLER.items():
            # Başlığın bir kısmını aratarak güncelle (Tam eşleşme bazen boşluktan kaçabilir)
            cursor.execute("UPDATE konu SET resim = %s WHERE baslik LIKE %s", (url, f"%{baslik[:10]}%"))
            print(f"🖼️ Resim eklendi: {baslik[:20]}...")

        conn.commit()
        conn.close()
        print("\n🎉 İŞLEM TAMAM! Siteye resimler yüklendi.")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    resimleri_yukle()