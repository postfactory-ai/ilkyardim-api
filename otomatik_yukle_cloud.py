import pdfplumber
import re
import psycopg2 
import os

# ==========================================================
# BURAYA NEON DB ADRESİNİ YAPIŞTIR (Vercel'e koyduğun kodun aynısı)
# Örnek: "postgresql://neondb_owner:npg_OAFxzgdw76ta@ep-long-brook-agzcx4dh-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
# ==========================================================
DATABASE_URL = "postgresql://neondb_owner:npg_OAFxzgdw76ta@ep-long-brook-agzcx4dh-pooler.c-2.eu-central-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" 

PDF_DOSYA_ADI = "sbacil-saglik-ilk-yardim-egitimi-kitabi-mayis-2025pdf.pdf" 
BASLANGIC_SAYFASI = 15

# Başlık Desenleri
BASLIK_DESENLERI = [
    ("I. GENEL İLK YARDIM BİLGİLERİ", r"I\.\s*GENEL\s+İLK\s+YARDIM"),
    ("II. VÜCUT SİSTEMLERİ", r"II\.\s*VÜCUT\s+SİSTEMLERİ"),
    ("III. ACİL TAŞIMA TEKNİKLERİ", r"III\.\s*ACİL\s+TAŞIMA"),
    ("IV. OTOMATİK EKSTERNAL DEFİBRİLATÖR (OED) KULLANIMI", r"IV\.\s*OTOMATİK\s+EKSTERNAL"),
    ("V. TEMEL YAŞAM DESTEĞİ", r"V\.\s*TEMEL\s+YAŞAM"),
    ("VI. HAVA YOLU TIKANIKLIĞINDA İLK YARDIM", r"VI\.\s*HAVA\s+YOLU"),
    ("VII. BİLİNÇ BOZUKLUKLARINDA VE CİDDİ HASTALIK DURUMLARINDA İLK YARDIM", r"VII\.\s*BİLİNÇ"),
    ("VIII. KANAMALARDA İLK YARDIM", r"VIII\.\s*KANAMA"),
    ("IX. ŞOK VE GÖĞÜS AĞRISINDA İLK YARDIM", r"IX\.\s*ŞOK\s+VE"),
    ("X. YARALANMALARDA İLK YARDIM", r"X\.\s*YARALANMALARDA"),
    ("XI. BOĞULMALARDA İLK YARDIM", r"XI\.\s*BOĞULMALARDA"),
    ("XII. KIRIK, ÇIKIK VE BURKULMALARDA İLK YARDIM", r"XII\.\s*KIRIK,\s*ÇIKIK"), 
    ("XIII. HAYVAN ISIRIKLARI ve BÖCEK SOKMALARINDA İLK YARDIM", r"X(II|III)\.\s*HAYVAN\s+ISIRIKLARI"),
    ("XIV. ZEHİRLENMELERDE İLK YARDIM", r"XIV\.\s*ZEHİRLENMELERDE"),
    ("XV. YANIK, SOĞUK VE SICAK ACİLLERİNDE İLK YARDIM", r"XV\.\s*YANIK,\s*SOĞUK"),
    ("XVI. GÖZE, KULAĞA, BURUNA YABANCI CİSİM KAÇMASI VE YUTULAN YABANCI CİSİMLERDE İLK YARDIM", r"XVI\.\s*(GÖZ|GÖZE).+YABANCI")
]

def hiyerarsik_formatla(text):
    if not text: return ""
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.isdigit(): continue 
        if re.match(r'^[A-ZĞÜŞİÖÇ]\.\s+', line):
            formatted_lines.append(f"<h3 class='text-danger mt-5 mb-3'>{line}</h3>")
        elif re.match(r'^[0-9]+\.\s+', line):
            formatted_lines.append(f"<h4 class='text-primary mt-4 mb-2'>{line}</h4>")
        elif any(x in line.upper() for x in ["DİKKAT", "UYARI"]):
            formatted_lines.append(f"<div class='wiki-alert alert-danger-custom'><strong>⚠️ {line}</strong></div>")
        elif any(x in line.upper() for x in ["ÖNEMLİ", "NOT"]):
            formatted_lines.append(f"<div class='wiki-alert alert-warning-custom'><strong>📌 {line}</strong></div>")
        elif re.match(r'^[a-z]\)\s+', line) or line.startswith("•") or line.startswith("-"):
            formatted_lines.append(f"<div class='ms-4 mb-2'>• {line}</div>")
        else:
            formatted_lines.append(f"<p class='mb-2'>{line}</p>")
    return "\n".join(formatted_lines)

def veritabanina_yukle():
    print("⏳ PDF okunuyor...")
    tum_metin = ""
    with pdfplumber.open(PDF_DOSYA_ADI) as pdf:
        for i in range(BASLANGIC_SAYFASI, len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text()
            if text: tum_metin += "\n" + text

    print("✅ PDF hafızada. NeonDB'ye bağlanılıyor...")
    
    # URL Düzeltmesi (Postgresql formatı için)
    final_db_url = DATABASE_URL.replace("postgres://", "postgresql://") if "postgres://" in DATABASE_URL else DATABASE_URL
    
    try:
        conn = psycopg2.connect(final_db_url)
        cursor = conn.cursor()
        
        # Önce Tablonun var olduğundan emin olalım
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS konu (
                id SERIAL PRIMARY KEY,
                baslik VARCHAR(200) NOT NULL,
                icerik TEXT,
                sira INTEGER DEFAULT 0,
                eklenme_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()

        # Konuları İşle
        for i in range(len(BASLIK_DESENLERI)):
            db_baslik, regex_pattern = BASLIK_DESENLERI[i]
            
            # Başlık veritabanında var mı? Yoksa ekle (INSERT), Varsa güncelle (UPDATE)
            # Bu sayede boş tabloyu da doldururuz.
            match_now = re.search(regex_pattern, tum_metin, re.IGNORECASE)
            
            html_icerik = "İçerik Bulunamadı"
            if match_now:
                start_idx = match_now.start()
                end_idx = -1
                if i + 1 < len(BASLIK_DESENLERI):
                    next_regex = BASLIK_DESENLERI[i+1][1]
                    match_next = re.search(next_regex, tum_metin, re.IGNORECASE)
                    if match_next and match_next.start() > start_idx:
                        end_idx = match_next.start()
                
                ham_icerik = tum_metin[start_idx:end_idx] if end_idx != -1 else tum_metin[start_idx:]
                split_icerik = ham_icerik.split('\n', 1)
                if len(split_icerik) > 1: ham_icerik = split_icerik[1]
                html_icerik = hiyerarsik_formatla(ham_icerik)

            # Önce konuyu bulmaya çalış
            cursor.execute("SELECT id FROM konu WHERE baslik = %s", (db_baslik,))
            result = cursor.fetchone()

            if result:
                # Varsa Güncelle
                cursor.execute("UPDATE konu SET icerik = %s WHERE baslik = %s", (html_icerik, db_baslik))
                print(f"🔄 GÜNCELLENDİ: {db_baslik[:20]}...")
            else:
                # Yoksa Sıfırdan Ekle
                cursor.execute("INSERT INTO konu (baslik, icerik, sira) VALUES (%s, %s, %s)", (db_baslik, html_icerik, i+1))
                print(f"➕ EKLENDİ: {db_baslik[:20]}...")

        conn.commit()
        conn.close()
        print("\n🎉 BULUT VERİTABANI FULLENDİ! Siteyi yenileyebilirsin.")
        
    except Exception as e:
        print(f"❌ Bağlantı Hatası: {e}")

if __name__ == "__main__":
    veritabanina_yukle()