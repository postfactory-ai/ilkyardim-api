from app import app, db

# 1. Mobil Cihaz Tokenları İçin Tablo
class Cihaz(db.Model):
    __tablename__ = 'cihaz'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Hangi kullanıcı?
    token = db.Column(db.String(500), unique=True, nullable=False) # Firebase Token'ı
    platform = db.Column(db.String(20), default='android') # android/ios
    kayit_tarihi = db.Column(db.DateTime, server_default=db.func.now())

# 2. Duyuru Tablosunu Güncelliyoruz (Hedef Link Eklendi)
# SQLAlchemy'de tabloyu değiştirmek zordur, o yüzden Duyuru tablosunu silip yeniden oluşturuyoruz.
# (Eski duyurular silinecek, sorun değil)

print("🏗️ VERİTABANI GÜNCELLENİYOR (Push Bildirim Sistemi)...")

with app.app_context():
    # Önce Duyuru tablosunu düşür (sütun eklemek için)
    db.session.execute(db.text('DROP TABLE IF EXISTS duyuru'))
    db.session.commit()
    
    # Tabloları baştan oluştur
    db.create_all()
    print("✅ 'Cihaz' tablosu eklendi.")
    print("✅ 'Duyuru' tablosu (Hedef Link özelliğiyle) yenilendi.")