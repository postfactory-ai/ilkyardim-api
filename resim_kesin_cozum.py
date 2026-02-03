import psycopg2

# ==========================================================
# BURAYA NEON DB KODUNU YAPIŞTIR
DATABASE_URL = "postgresql://neondb_owner:npg_OAFxzgdw76ta@ep-long-brook-agzcx4dh-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" 
# ==========================================================

# Anahtar Kelimeye Göre Resim Eşleştirme
RESIM_MAP = [
    ("GENEL", "https://images.unsplash.com/photo-1516574187841-693083f05b12?w=600&q=80"),
    ("VÜCUT", "https://images.unsplash.com/photo-1530210124550-912dc1381cb8?w=600&q=80"),
    ("TAŞIMA", "https://images.unsplash.com/photo-1588611842858-2947df332309?w=600&q=80"),
    ("OED", "https://images.unsplash.com/photo-1576091160550-2187d80aeff2?w=600&q=80"),
    ("YAŞAM", "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600&q=80"),
    ("HAVA", "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=600&q=80"),
    ("BİLİNÇ", "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=600&q=80"),
    ("KANAMA", "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=600&q=80"),
    ("ŞOK", "https://images.unsplash.com/photo-1584362917165-526a968579e8?w=600&q=80"),
    ("YARALANMA", "https://images.unsplash.com/photo-1624727828489-a1e03b79bba8?w=600&q=80"),
    ("BOĞULMA", "https://images.unsplash.com/photo-1542614471-001ddf2b7219?w=600&q=80"),
    ("KIRIK", "https://images.unsplash.com/photo-1583912268297-3c58cc84a0b3?w=600&q=80"),
    ("HAYVAN", "https://images.unsplash.com/photo-1562957138-16dc5c2d3340?w=600&q=80"),
    ("ZEHİRLENME", "https://images.unsplash.com/photo-1607569707101-1e247b973523?w=600&q=80"),
    ("YANIK", "https://images.unsplash.com/photo-1626292723326-62025f0e9b25?w=600&q=80"),
    ("GÖZ", "https://images.unsplash.com/photo-1625515234909-54b1f4870f44?w=600&q=80")
]

def guncelle():
    print("⏳ Veritabanına bağlanılıyor...")
    url = DATABASE_URL.replace("postgres://", "postgresql://") if "postgres://" in DATABASE_URL else DATABASE_URL
    
    try:
        conn = psycopg2.connect(url)
        cursor = conn.cursor()

        # Önce tüm resimleri temizle (Karışıklık kalmasın)
        # cursor.execute("UPDATE konu SET resim = NULL")
        # print("🧹 Eski resimler temizlendi.")

        print("📸 Yeni resimler yükleniyor...")
        
        for kelime, link in RESIM_MAP:
            # Başlığın içinde o kelime geçiyorsa (LIKE %KELIME%) güncelle
            cursor.execute("UPDATE konu SET resim = %s WHERE baslik LIKE %s", (link, f"%{kelime}%"))
            if cursor.rowcount > 0:
                print(f"✅ Eşleşti: '{kelime}' -> Resim Güncellendi.")
            else:
                print(f"⚠️ Eşleşmedi: '{kelime}' (Veritabanında bu kelimeyle başlık yok mu?)")

        conn.commit()
        conn.close()
        print("\n🎉 İŞLEM BİTTİ! Siteyi kontrol et.")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    guncelle()