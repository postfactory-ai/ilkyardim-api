import psycopg2

# ==========================================================
# BURAYA NEON DB KODUNU YAPIŞTIR
DATABASE_URL = "postgresql://neondb_owner:npg_OAFxzgdw76ta@ep-long-brook-agzcx4dh-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" 
# ==========================================================

# ID'ye Göre Kesin Resim Listesi (1-16 Arası)
RESIM_LISTESI = {
    1: "https://images.unsplash.com/photo-1516574187841-693083f05b12?w=600&q=80",  # I. Genel
    2: "https://images.unsplash.com/photo-1530210124550-912dc1381cb8?w=600&q=80",  # II. Vücut
    3: "https://images.unsplash.com/photo-1588611842858-2947df332309?w=600&q=80",  # III. Taşıma
    4: "https://images.unsplash.com/photo-1576091160550-2187d80aeff2?w=600&q=80",  # IV. OED
    5: "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=600&q=80",  # V. Yaşam Desteği
    6: "https://images.unsplash.com/photo-1631815588090-d4bfec5b1ccb?w=600&q=80",  # VI. Hava Yolu
    7: "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=600&q=80",  # VII. Bilinç
    8: "https://images.unsplash.com/photo-1628771065518-0d82f1938462?w=600&q=80",  # VIII. Kanama
    9: "https://images.unsplash.com/photo-1584362917165-526a968579e8?w=600&q=80",  # IX. Şok
    10: "https://images.unsplash.com/photo-1624727828489-a1e03b79bba8?w=600&q=80", # X. Yaralanma
    11: "https://images.unsplash.com/photo-1542614471-001ddf2b7219?w=600&q=80",  # XI. Boğulma
    12: "https://images.unsplash.com/photo-1583912268297-3c58cc84a0b3?w=600&q=80", # XII. Kırık
    13: "https://images.unsplash.com/photo-1562957138-16dc5c2d3340?w=600&q=80",  # XIII. Hayvan
    14: "https://images.unsplash.com/photo-1607569707101-1e247b973523?w=600&q=80", # XIV. Zehirlenme
    15: "https://images.unsplash.com/photo-1626292723326-62025f0e9b25?w=600&q=80", # XV. Yanık
    16: "https://images.unsplash.com/photo-1625515234909-54b1f4870f44?w=600&q=80", # XVI. Göz/KBB
}

def id_ile_resim_guncelle():
    print("⏳ Veritabanına bağlanılıyor...")
    url = DATABASE_URL.replace("postgres://", "postgresql://") if "postgres://" in DATABASE_URL else DATABASE_URL
    
    try:
        conn = psycopg2.connect(url)
        cursor = conn.cursor()

        print("📸 Resimler ID bazlı güncelleniyor...")
        
        for sira_id, resim_url in RESIM_LISTESI.items():
            # Sıra numarasına (sira) göre güncelleme yapıyoruz
            cursor.execute("UPDATE konu SET resim = %s WHERE sira = %s", (resim_url, sira_id))
            print(f"✅ Modül {sira_id} resmi güncellendi.")

        conn.commit()
        conn.close()
        print("\n🎉 RESİMLER KESİN OLARAK DÜZELDİ! Siteyi kontrol et.")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    id_ile_resim_guncelle()