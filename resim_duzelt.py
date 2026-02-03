import psycopg2

# ==========================================================
# BURAYA NEON DB CONNECTION STRING'İ YAPIŞTIR
DATABASE_URL = "postgresql://neondb_owner:npg_OAFxzgdw76ta@ep-long-brook-agzcx4dh-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" 
# ==========================================================

# Konulara Özel, Kontrol Edilmiş Görseller
RESIMLER = {
    "GENEL İLK YARDIM": "https://images.unsplash.com/photo-1516574187841-693083f05b12?w=600&q=80",
    "VÜCUT SİSTEMLERİ": "https://images.unsplash.com/photo-1530210124550-912dc1381cb8?w=600&q=80",
    "TAŞIMA": "https://images.unsplash.com/photo-1516549655169-df83a0774514?w=600&q=80", # Sedye
    "OED": "https://images.unsplash.com/photo-1584036561566-b93a50208c3c?w=600&q=80", # Defibrilatör
    "YAŞAM DESTEĞİ": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600&q=80", # CPR
    "HAVA YOLU": "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=600&q=80",
    "BİLİNÇ": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=600&q=80",
    "KANAMA": "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=600&q=80", # Bandaj
    "ŞOK": "https://images.unsplash.com/photo-1579154204601-01588f351e67?w=600&q=80",
    "YARALANMA": "https://images.unsplash.com/photo-1624727828489-a1e03b79bba8?w=600&q=80",
    "BOĞULMA": "https://images.unsplash.com/photo-1682687218982-6d5081035a8a?w=600&q=80", # Su
    "KIRIK": "https://images.unsplash.com/photo-1583912268297-3c58cc84a0b3?w=600&q=80", # Röntgen
    "HAYVAN": "https://images.unsplash.com/photo-1555685812-4b943f3e99a0?w=600&q=80", # Böcek
    "ZEHİRLENME": "https://images.unsplash.com/photo-1515569067071-ec3b51335dd0?w=600&q=80",
    "YANIK": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&q=80", # Ateş
    "GÖZ": "https://images.unsplash.com/photo-1569617084133-26942bb441f2?w=600&q=80"
}

def resimleri_duzelt():
    print("⏳ Veritabanına bağlanılıyor...")
    
    url = DATABASE_URL.replace("postgres://", "postgresql://") if "postgres://" in DATABASE_URL else DATABASE_URL
    
    try:
        conn = psycopg2.connect(url)
        cursor = conn.cursor()

        print("📸 Resimler güncelleniyor...")
        for anahtar, link in RESIMLER.items():
            # Başlığın içinde anahtar kelime geçiyorsa (örn: 'KANAMA' geçiyorsa) resmi güncelle
            cursor.execute("UPDATE konu SET resim = %s WHERE baslik LIKE %s", (link, f"%{anahtar}%"))
            print(f"✅ Güncellendi: {anahtar}")

        conn.commit()
        conn.close()
        print("\n🎉 RESİMLER BAŞARIYLA YÜKLENDİ! Siteyi kontrol et.")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    resimleri_duzelt()