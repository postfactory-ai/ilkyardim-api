import sqlite3
import pdfplumber
import re
import os

# --- AYARLAR ---
PDF_DOSYA_ADI = "sbacil-saglik-ilk-yardim-egitimi-kitabi-mayis-2025pdf.pdf" 
base_dir = os.path.abspath(os.path.dirname(__file__))
DB_DOSYA_ADI = os.path.join(base_dir, "instance", "ilkyardim.db")
BASLANGIC_SAYFASI = 15

# Başlık Desenleri (Aynı kalıyor)
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
    """
    Düz metni Wiki tarzı zengin HTML'e çevirir.
    """
    if not text: return ""
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line or line.isdigit(): continue 
        
        # 1. Ana Başlıklar (A. B. C.)
        if re.match(r'^[A-ZĞÜŞİÖÇ]\.\s+', line):
            formatted_lines.append(f"<h3 class='text-danger mt-5 mb-3'>{line}</h3>")
        
        # 2. Alt Başlıklar (1. 2. 3.)
        elif re.match(r'^[0-9]+\.\s+', line):
            formatted_lines.append(f"<h4 class='text-primary mt-4 mb-2'>{line}</h4>")
        
        # 3. UYARI / DİKKAT KUTULARI (Botun Zekası Burada!)
        elif line.upper().startswith("DİKKAT") or line.upper().startswith("UYARI"):
            # Kırmızı Kutu
            formatted_lines.append(f"<div class='wiki-alert alert-danger-custom'><strong>⚠️ {line}</strong></div>")
        
        elif line.upper().startswith("ÖNEMLİ") or line.upper().startswith("NOT"):
            # Sarı Kutu
            formatted_lines.append(f"<div class='wiki-alert alert-warning-custom'><strong>📌 {line}</strong></div>")

        # 4. Madde İşaretleri (a) b) - veya •)
        elif re.match(r'^[a-z]\)\s+', line) or line.startswith("•") or line.startswith("-"):
            formatted_lines.append(f"<div class='ms-4 mb-2'>• {line}</div>")
            
        # 5. Normal Paragraf
        else:
            formatted_lines.append(f"<p class='mb-2'>{line}</p>")
            
    return "\n".join(formatted_lines)

def veritabanina_yukle():
    print(f"⏳ PDF okunuyor... (İlk {BASLANGIC_SAYFASI} sayfa temizleniyor)")
    
    tum_metin = ""
    with pdfplumber.open(PDF_DOSYA_ADI) as pdf:
        for i in range(BASLANGIC_SAYFASI, len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text()
            if text:
                tum_metin += "\n" + text

    print("✅ PDF hafızaya alındı. Ayrıştırma ve Zenginleştirme başlıyor...")

    conn = sqlite3.connect(DB_DOSYA_ADI)
    cursor = conn.cursor()

    for i in range(len(BASLIK_DESENLERI)):
        db_baslik, regex_pattern = BASLIK_DESENLERI[i]
        
        match_now = re.search(regex_pattern, tum_metin, re.IGNORECASE)
        
        if match_now:
            start_idx = match_now.start()
            end_idx = -1
            if i + 1 < len(BASLIK_DESENLERI):
                next_regex = BASLIK_DESENLERI[i+1][1]
                match_next = re.search(next_regex, tum_metin, re.IGNORECASE)
                if match_next and match_next.start() > start_idx:
                    end_idx = match_next.start()
            
            if end_idx != -1:
                ham_icerik = tum_metin[start_idx:end_idx]
            else:
                ham_icerik = tum_metin[start_idx:]
            
            # İlk satırı (başlığı) sil
            split_icerik = ham_icerik.split('\n', 1)
            if len(split_icerik) > 1:
                ham_icerik = split_icerik[1]

            # Zengin HTML'e çevir
            html_icerik = hiyerarsik_formatla(ham_icerik)
            
            cursor.execute("UPDATE konu SET icerik = ? WHERE baslik = ?", (html_icerik, db_baslik))
            print(f"✅ GÜNCELLENDİ (Wiki Modu): {db_baslik[:20]}... ")
        else:
            print(f"❌ BULUNAMADI: {db_baslik}")

    conn.commit()
    conn.close()
    print("\n🎉 SİTE GÜNCELLENDİ! Şimdi sayfaları gezebilirsin.")

if __name__ == "__main__":
    veritabanina_yukle()