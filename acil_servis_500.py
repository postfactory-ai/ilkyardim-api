import pdfplumber
import re
import os
from app import app, db, Konu, User
from werkzeug.security import generate_password_hash

# --- AYARLAR ---
PDF_DOSYA_ADI = "sbacil-saglik-ilk-yardim-egitimi-kitabi-mayis-2025pdf.pdf" 
BASLANGIC_SAYFASI = 15

print("\033[92m🤖 VERİ YÜKLEME ROBOTU ÇALIŞIYOR...\033[0m")

# Başlık Desenleri
BASLIK_DESENLERI = [
    ("GENEL BİLGİLER", r"I\.\s*GENEL\s+İLK\s+YARDIM"),
    ("VÜCUT SİSTEMLERİ", r"II\.\s*VÜCUT\s+SİSTEMLERİ"),
    ("HASTA TAŞIMA", r"III\.\s*ACİL\s+TAŞIMA"),
    ("OED (ŞOK CİHAZI)", r"IV\.\s*OTOMATİK\s+EKSTERNAL"),
    ("TEMEL YAŞAM DESTEĞİ", r"V\.\s*TEMEL\s+YAŞAM"),
    ("HAVA YOLU TIKANIKLIĞI", r"VI\.\s*HAVA\s+YOLU"),
    ("BİLİNÇ BOZUKLUKLARI", r"VII\.\s*BİLİNÇ"),
    ("KANAMALAR", r"VIII\.\s*KANAMA"),
    ("ŞOK DURUMU", r"IX\.\s*ŞOK\s+VE"),
    ("YARALANMALAR", r"X\.\s*YARALANMALARDA"),
    ("BOĞULMALAR", r"XI\.\s*BOĞULMALARDA"),
    ("KIRIK, ÇIKIK VE BURKULMA", r"XII\.\s*KIRIK,\s*ÇIKIK"), 
    ("HAYVAN ISIRIKLARI", r"X(II|III)\.\s*HAYVAN\s+ISIRIKLARI"),
    ("ZEHİRLENMELER", r"XIV\.\s*ZEHİRLENMELERDE"),
    ("YANIK VE DONMALAR", r"XV\.\s*YANIK,\s*SOĞUK"),
    ("GÖZ, KULAK, BURUN", r"XVI\.\s*(GÖZ|GÖZE).+YABANCI")
]

def hiyerarsik_formatla(text):
    if not text: return ""
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if not line or line.isdigit(): continue 
        if re.match(r'^[A-ZĞÜŞİÖÇ]\.\s+', line):
            formatted_lines.append(f"<h4 class='text-danger mt-4 mb-2 fw-bold'>{line}</h4>")
        elif re.match(r'^[0-9]+\.\s+', line):
            formatted_lines.append(f"<h5 class='text-primary mt-3 mb-1 fw-bold'>{line}</h5>")
        elif line.upper().startswith("DİKKAT") or line.upper().startswith("UYARI"):
            formatted_lines.append(f"<div class='alert alert-danger d-flex align-items-center mt-2'><i class='ph-bold ph-warning me-2 fs-4'></i> <strong>{line}</strong></div>")
        elif line.upper().startswith("ÖNEMLİ") or line.upper().startswith("NOT"):
            formatted_lines.append(f"<div class='alert alert-warning d-flex align-items-center mt-2'><i class='ph-bold ph-info me-2 fs-4'></i> <strong>{line}</strong></div>")
        elif re.match(r'^[a-z]\)\s+', line) or line.startswith("•") or line.startswith("-"):
            formatted_lines.append(f"<div class='ms-3 mb-1 text-secondary'><i class='ph-duotone ph-check-circle me-1'></i> {line}</div>")
        else:
            formatted_lines.append(f"<p class='mb-2'>{line}</p>")
    return "\n".join(formatted_lines)

def yukle():
    if not os.path.exists(PDF_DOSYA_ADI):
        print(f"❌ '{PDF_DOSYA_ADI}' BULUNAMADI! Lütfen proje klasörüne at.")
        return

    print("⏳ PDF okunuyor...")
    tum_metin = ""
    try:
        with pdfplumber.open(PDF_DOSYA_ADI) as pdf:
            for i in range(BASLANGIC_SAYFASI, len(pdf.pages)):
                text = pdf.pages[i].extract_text()
                if text: tum_metin += "\n" + text
    except Exception as e:
        print(f"❌ PDF Hatası: {e}")
        return

    with app.app_context():
        # Hangi veritabanına bağlıyız?
        print(f"📡 Hedef Veritabanı: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # 1. Tabloları Kur
        db.create_all()
        
        # 2. Admin Ekle
        if not User.query.filter_by(username='admin').first():
            print("👤 Admin oluşturuluyor...")
            admin = User(username='admin', email='admin@sistem.com', password=generate_password_hash('1234', method='pbkdf2:sha256'), is_admin=True)
            db.session.add(admin)
        
        # 3. İçerikleri Ekle
        print("📚 İçerikler işleniyor...")
        for i, (db_baslik_adi, regex_pattern) in enumerate(BASLIK_DESENLERI):
            sira_no = i + 1
            match_now = re.search(regex_pattern, tum_metin, re.IGNORECASE)
            
            if match_now:
                start = match_now.start()
                end = -1
                if i + 1 < len(BASLIK_DESENLERI):
                    next_reg = BASLIK_DESENLERI[i+1][1]
                    match_next = re.search(next_reg, tum_metin, re.IGNORECASE)
                    if match_next and match_next.start() > start: end = match_next.start()
                
                ham = tum_metin[start:end] if end != -1 else tum_metin[start:]
                split_ic = ham.split('\n', 1)
                ham = split_ic[1] if len(split_ic) > 1 else ham
                
                html = hiyerarsik_formatla(ham)
                
                konu = Konu.query.filter_by(sira=sira_no).first()
                if konu:
                    konu.icerik = html
                    konu.baslik = db_baslik_adi
                else:
                    yeni_konu = Konu(sira=sira_no, baslik=db_baslik_adi, icerik=html, resim="")
                    db.session.add(yeni_konu)
                print(f"✅ Modül {sira_no}: {db_baslik_adi} Yüklendi.")
            else:
                # PDF'te bulamazsa boş oluştur ki anasayfada kutu çıksın
                if not Konu.query.filter_by(sira=sira_no).first():
                    bos_konu = Konu(sira=sira_no, baslik=db_baslik_adi, icerik="İçerik hazırlanıyor...", resim="")
                    db.session.add(bos_konu)
                    print(f"⚠️ Modül {sira_no} PDF'te bulunamadı, boş eklendi.")

        db.session.commit()
        print("\n🎉 İŞLEM TAMAMLANDI!")

if __name__ == "__main__":
    yukle()