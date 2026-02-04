from app import app, db
from sqlalchemy import text

print("🔧 DUYURU TABLOSU YENİLENİYOR...")

with app.app_context():
    # 1. Eski tabloyu zorla sil (İçinde veri varsa gider, sorun değil)
    # CASCADE komutu, buna bağlı her şeyi de temizler.
    with db.engine.connect() as connection:
        connection.execute(text("DROP TABLE IF EXISTS duyuru CASCADE"))
        connection.commit()
        print("🗑️  Eski, hatalı tablo silindi.")

    # 2. Yeni tabloyu (app.py'deki son haline göre) oluştur
    db.create_all()
    print("✨  Yeni 'Duyuru' tablosu (hedef sütunuyla) oluşturuldu.")
    
    print("\n✅ İŞLEM TAMAM! Şimdi 'python app.py' diyip arkanı yaslan.")