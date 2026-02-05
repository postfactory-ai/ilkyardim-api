import sqlite3
import json
import os

def verileri_paketle():
    # 1. Doğru Veritabanı Yolunu Bulalım
    db_yolu = 'local.db'
    
    if os.path.exists('instance/local.db'):
        db_yolu = 'instance/local.db'
        print(f"✅ Veritabanı 'instance' klasöründe bulundu: {db_yolu}")
    elif os.path.exists('local.db'):
        print(f"✅ Veritabanı ana dizinde bulundu: {db_yolu}")
    else:
        print("❌ HATA: 'local.db' dosyası ne ana dizinde ne de 'instance' klasöründe bulunamadı!")
        return

    # 2. Bağlan ve Verileri Çek
    try:
        baglanti = sqlite3.connect(db_yolu)
        imlec = baglanti.cursor()
        
        # Tablo adını kontrol et (Bazen 'konu', bazen 'Konu' olabilir)
        imlec.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='konu'")
        if not imlec.fetchone():
            print("❌ HATA: Veritabanı bulundu ama içinde 'konu' tablosu yok. Yanlış DB dosyası olabilir.")
            baglanti.close()
            return

        imlec.execute("SELECT baslik, icerik, sira FROM konu ORDER BY sira")
        veriler = imlec.fetchall()
        
        if not veriler:
            print("⚠️ UYARI: Tablo bulundu ama içi BOŞ. Lokalde veri girdiğine emin misin?")
            baglanti.close()
            return

        liste = []
        for veri in veriler:
            konu = {
                "baslik": veri[0],
                "icerik": veri[1], # HTML içerik
                "sira": veri[2],
                "resim": None
            }
            liste.append(konu)

        # 3. Dosyaya Yaz
        with open('yedek_icerik.json', 'w', encoding='utf-8') as f:
            json.dump(liste, f, ensure_ascii=False, indent=4)

        print(f"\n🎉 HARİKA! {len(liste)} adet konu başarıyla 'yedek_icerik.json' dosyasına paketlendi.")
        print("Şimdi terminale şu komutları yazarak GitHub'a gönder:\n")
        print("git add yedek_icerik.json")
        print('git commit -m "Veriler paketlendi"')
        print("git push origin master")

    except Exception as e:
        print(f"❌ Beklenmedik bir hata: {e}")
    finally:
        if 'baglanti' in locals():
            baglanti.close()

if __name__ == "__main__":
    verileri_paketle()