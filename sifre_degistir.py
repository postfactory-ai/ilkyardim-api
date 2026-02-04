from app import app, db, User
from werkzeug.security import generate_password_hash
import getpass

print("\n🔐 ADMIN ŞİFRE GÜNCELLEME ARACI 🔐")
print("-" * 40)

def sifre_guncelle():
    with app.app_context():
        # Admin kullanıcısını bul
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ HATA: 'admin' kullanıcısı bulunamadı!")
            print("   Önce 'python tamir_ve_yukle.py' çalıştırıp sistemi kurmalısın.")
            return

        print(f"✅ Kullanıcı bulundu: {admin.username} ({admin.email})")
        
        # Yeni şifreyi iste (Yazarken görünmez)
        yeni_sifre = getpass.getpass("👉 Yeni Şifrenizi Girin: ")
        tekrar_sifre = getpass.getpass("👉 Şifreyi Tekrar Girin: ")
        
        if yeni_sifre != tekrar_sifre:
            print("\n❌ HATA: Şifreler eşleşmedi! Tekrar dene.")
            return
            
        if len(yeni_sifre) < 6:
            print("\n❌ UYARI: Şifre en az 6 karakter olsa daha iyi olur.")
            
        # Şifreyi hashle ve kaydet
        hashed_pw = generate_password_hash(yeni_sifre, method='pbkdf2:sha256')
        admin.password = hashed_pw
        db.session.commit()
        
        print("\n" + "="*40)
        print("🎉 BAŞARILI! Admin şifresi değiştirildi.")
        print(f"👉 Artık '{yeni_sifre}' ile giriş yapabilirsin.")
        print("="*40)

if __name__ == "__main__":
    sifre_guncelle()