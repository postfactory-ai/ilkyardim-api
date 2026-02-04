import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# Google Login HTTPS Hatası Çözümü için:
from werkzeug.middleware.proxy_fix import ProxyFix 
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Google OAuth için (Lokalde http izni)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

# --- KRİTİK AYAR: HTTPS YÖNLENDİRMESİ (RENDER İÇİN) ---
# Bu satır Google Login'in "Mismatch" hatasını çözer.
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gizli-anahtar')
app.config['JSON_AS_ASCII'] = False

# --- VERİTABANI AYARLARI ---
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bağlantı Kopma Koruması
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True, 
    "pool_recycle": 300
}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'giris_yap'

# --- GOOGLE OAUTH ---
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs' 
)

# ==========================================
#               VERİTABANI MODELLERİ
# ==========================================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=True)
    email = db.Column(db.String(150), unique=True, nullable=True)
    password = db.Column(db.String(250), nullable=True)
    google_id = db.Column(db.String(200), unique=True, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

class Konu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    icerik = db.Column(db.Text, nullable=True) 
    sira = db.Column(db.Integer, default=0)
    resim = db.Column(db.String(500), nullable=True)
    sorular = db.relationship('Soru', backref='konu', lazy=True)

class Soru(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    konu_id = db.Column(db.Integer, db.ForeignKey('konu.id'), nullable=False)
    soru_metni = db.Column(db.Text, nullable=False)
    a = db.Column(db.String(200), nullable=False)
    b = db.Column(db.String(200), nullable=False)
    c = db.Column(db.String(200), nullable=False)
    d = db.Column(db.String(200), nullable=False)
    dogru_cevap = db.Column(db.String(1), nullable=False)

class Duyuru(db.Model):
    __tablename__ = 'duyuru'
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100), nullable=False)
    mesaj = db.Column(db.Text, nullable=False)
    hedef = db.Column(db.String(100), default='/') 
    aktif = db.Column(db.Boolean, default=True)
    tarih = db.Column(db.DateTime, server_default=db.func.now())

class Cihaz(db.Model):
    __tablename__ = 'cihaz'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    platform = db.Column(db.String(20), default='android')
    kayit_tarihi = db.Column(db.DateTime, server_default=db.func.now())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==========================================
#          MOBİL API (JSON ÇIKIŞLARI)
# ==========================================

@app.route('/api/konular')
def api_get_konular():
    konular = Konu.query.order_by(Konu.sira).all()
    data = [{'id': k.id, 'baslik': k.baslik, 'sira': k.sira, 'resim': k.resim} for k in konular]
    return jsonify(data)

@app.route('/api/konu/<int:id>')
def api_get_konu_detay(id):
    konu = Konu.query.get_or_404(id)
    return jsonify({
        'id': konu.id,
        'baslik': konu.baslik,
        'icerik': konu.icerik,
        'resim': konu.resim,
        'sira': konu.sira
    })

@app.route('/api/duyurular')
def api_get_duyurular():
    duyurular = Duyuru.query.filter_by(aktif=True).order_by(Duyuru.id.desc()).all()
    data = [{'id': d.id, 'baslik': d.baslik, 'mesaj': d.mesaj, 'hedef': d.hedef, 'tarih': d.tarih} for d in duyurular]
    return jsonify(data)

@app.route('/api/cihaz-kayit', methods=['POST'])
def cihaz_kayit():
    data = request.json
    token = data.get('token')
    platform = data.get('platform', 'android')
    if not token: return jsonify({'error': 'Token yok'}), 400
    
    cihaz = Cihaz.query.filter_by(token=token).first()
    if not cihaz:
        yeni_cihaz = Cihaz(token=token, platform=platform)
        db.session.add(yeni_cihaz)
        db.session.commit()
    
    return jsonify({'status': 'ok', 'message': 'Cihaz kaydedildi'})

@app.route('/api/arama')
def api_arama():
    kelime = request.args.get('q', '')
    sonuclar = []
    if kelime and len(kelime) > 1:
        bulunanlar = Konu.query.filter(or_(Konu.baslik.ilike(f'%{kelime}%'), Konu.icerik.ilike(f'%{kelime}%'))).all()
        for konu in bulunanlar:
            temiz_metin = re.sub('<[^<]+?>', '', konu.icerik)
            match = re.search(re.escape(kelime), temiz_metin, re.IGNORECASE)
            ozet = ""
            if match:
                start = max(0, match.start() - 60)
                end = min(len(temiz_metin), match.end() + 60)
                ozet_parca = temiz_metin[start:end]
                ozet = re.sub(f"({re.escape(kelime)})", r"<mark>\1</mark>", ozet_parca, flags=re.IGNORECASE)
                ozet = f"...{ozet}..."
            else: ozet = temiz_metin[:150] + "..."
            sonuclar.append({'id': konu.id, 'baslik': konu.baslik, 'ozet': ozet, 'sira': konu.sira})
    return jsonify(sonuclar)


# ==========================================
#             YÖNETİM PANELİ (ADMİN)
# ==========================================

@app.route('/yonetim')
@login_required
def yonetim_index():
    if not current_user.is_admin: return "Yetkisiz"
    konular = Konu.query.order_by(Konu.sira).all()
    duyuru_sayisi = Duyuru.query.count()
    return render_template('admin/index.html', konular=konular, duyuru_sayisi=duyuru_sayisi)

@app.route('/yonetim/hesap', methods=['GET', 'POST'])
@login_required
def yonetim_hesap():
    if not current_user.is_admin: return "Yetkisiz"
    
    if request.method == 'POST':
        islem = request.form.get('islem_turu')
        
        # 1. ŞİFRE DEĞİŞTİRME
        if islem == 'sifre_degistir':
            eski_sifre = request.form.get('eski_sifre')
            yeni_sifre = request.form.get('yeni_sifre')
            
            if not check_password_hash(current_user.password, eski_sifre):
                flash('❌ Mevcut şifre hatalı.', 'danger')
            elif len(yeni_sifre) < 4:
                flash('⚠️ Yeni şifre çok kısa!', 'warning')
            else:
                current_user.password = generate_password_hash(yeni_sifre, method='pbkdf2:sha256')
                db.session.commit()
                flash('✅ Şifre güncellendi.', 'success')
        
        # 2. YENİ ADMİN EKLEME
        elif islem == 'admin_ekle':
            kadi = request.form.get('kadi')
            email = request.form.get('email')
            sifre = request.form.get('sifre')
            
            if User.query.filter((User.username==kadi) | (User.email==email)).first():
                flash('⚠️ Kullanıcı zaten var.', 'warning')
            else:
                yeni_admin = User(
                    username=kadi, email=email, 
                    password=generate_password_hash(sifre, method='pbkdf2:sha256'),
                    is_admin=True
                )
                db.session.add(yeni_admin)
                db.session.commit()
                flash(f'🎉 {kadi} admin olarak eklendi!', 'success')
                
        return redirect(url_for('yonetim_hesap'))

    adminler = User.query.filter_by(is_admin=True).all()
    return render_template('admin/hesap.html', adminler=adminler)

@app.route('/yonetim/duyurular', methods=['GET', 'POST'])
@login_required
def yonetim_duyurular():
    if not current_user.is_admin: return "Yetkisiz"
    
    if request.method == 'POST':
        baslik = request.form.get('baslik')
        mesaj = request.form.get('mesaj')
        hedef = request.form.get('hedef')
        
        yeni_duyuru = Duyuru(baslik=baslik, mesaj=mesaj, hedef=hedef)
        db.session.add(yeni_duyuru)
        db.session.commit()
        
        kayitli = Cihaz.query.count()
        print(f"PUSH SENT: {baslik} -> {kayitli} cihaz (Link: {hedef})")
        
        flash(f'✅ Bildirim {kayitli} cihaza gönderildi!', 'success')
        return redirect(url_for('yonetim_duyurular'))
        
    duyurular = Duyuru.query.order_by(Duyuru.id.desc()).all()
    return render_template('admin/duyurular.html', duyurular=duyurular)

@app.route('/yonetim/duyuru-sil/<int:id>')
@login_required
def duyuru_sil(id):
    if not current_user.is_admin: return "Yetkisiz"
    duyuru = Duyuru.query.get_or_404(id)
    db.session.delete(duyuru)
    db.session.commit()
    flash('🗑️ Duyuru silindi.', 'warning')
    return redirect(url_for('yonetim_duyurular'))

@app.route('/yonetim/soru-ekle', methods=['GET', 'POST'])
@login_required
def soru_ekle():
    if not current_user.is_admin: return "Yetkisiz Alan"
    if request.method == 'POST':
        konu_id = request.form.get('konu_id')
        soru_metni = request.form.get('soru')
        a, b, c, d = request.form.get('a'), request.form.get('b'), request.form.get('c'), request.form.get('d')
        dogru = request.form.get('dogru')
        yeni_soru = Soru(konu_id=konu_id, soru_metni=soru_metni, a=a, b=b, c=c, d=d, dogru_cevap=dogru)
        db.session.add(yeni_soru)
        db.session.commit()
        flash('✅ Soru eklendi!', 'success')
        return redirect(url_for('soru_ekle'))
    konular = Konu.query.order_by(Konu.sira).all()
    return render_template('admin/soru_ekle.html', konular=konular)

@app.route('/yonetim/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def yonetim_duzenle(id):
    if not current_user.is_admin: return "Yetkisiz"
    konu = Konu.query.get_or_404(id)
    if request.method == 'POST':
        konu.baslik = request.form['baslik']
        konu.icerik = request.form['icerik']
        db.session.commit()
        return redirect(url_for('yonetim_index'))
    return render_template('admin/duzenle.html', konu=konu)


# ==========================================
#              GENEL ROTALAR
# ==========================================

@app.route('/')
def index():
    konular = Konu.query.order_by(Konu.sira).all()
    duyurular = Duyuru.query.filter_by(aktif=True).order_by(Duyuru.id.desc()).limit(3).all()
    return render_template('index.html', konular=konular, duyurular=duyurular)

@app.route('/konu/<int:id>')
def konu_detay(id):
    konu = Konu.query.get_or_404(id)
    return render_template('detay.html', konu=konu)

@app.route('/arama')
def arama():
    kelime = request.args.get('q', '')
    return render_template('arama.html', kelime=kelime)

@app.route('/quiz')
def quiz_genel():
    konular = Konu.query.order_by(Konu.sira).all()
    return render_template('quiz_secim.html', konular=konular)

@app.route('/quiz/<int:konu_id>')
def quiz_coz(konu_id):
    konu = Konu.query.get_or_404(konu_id)
    sorular = Soru.query.filter_by(konu_id=konu_id).all()
    return render_template('quiz.html', konu=konu, sorular=sorular)

# --- ÜYELİK VE GİRİŞ ---

@app.route('/giris', methods=['GET', 'POST'])
def giris_yap():
    if request.method == 'POST':
        girdi = request.form.get('username')
        sifre = request.form.get('password')
        user = User.query.filter((User.username == girdi) | (User.email == girdi)).first()
        if user and user.password and check_password_hash(user.password, sifre):
            login_user(user)
            return redirect(url_for('index'))
        else: flash('Hatalı bilgiler.', 'danger')
    return render_template('login.html')

@app.route('/kayit', methods=['GET', 'POST'])
def kayit_ol():
    if request.method == 'POST':
        kadi = request.form.get('username')
        email = request.form.get('email')
        sifre = request.form.get('password')
        if User.query.filter((User.username==kadi) | (User.email==email)).first():
            flash('Kullanıcı zaten var.', 'warning')
            return redirect(url_for('kayit_ol'))
        hashed_pw = generate_password_hash(sifre, method='pbkdf2:sha256')
        yeni_user = User(username=kadi, email=email, password=hashed_pw)
        db.session.add(yeni_user)
        db.session.commit()
        login_user(yeni_user)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize/google')
def google_authorize():
    try:
        token = google.authorize_access_token()
        resp = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
        user_info = resp.json()
        user = User.query.filter_by(google_id=user_info['id']).first()
        if not user:
            user = User.query.filter_by(email=user_info['email']).first()
            if user:
                user.google_id = user_info['id']
                db.session.commit()
            else:
                user = User(username=user_info['name'], email=user_info['email'], google_id=user_info['id'], password=None)
                db.session.add(user)
                db.session.commit()
        login_user(user)
        flash('Başarıyla giriş yapıldı!', 'success')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Google Hata: {str(e)}", 'danger')
        return redirect(url_for('giris_yap'))

@app.route('/cikis')
@login_required
def cikis_yap():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profil')
@login_required
def profil():
    return render_template('profile.html', user=current_user)

@app.route('/kurulum-yap')
def kurulum():
    db.create_all()
    return "Kurulum/Veritabani Onarimi Tamam."

# ==========================================
#     İÇERİK KURTARMA VE DÜZELTME
# ==========================================

@app.route('/icerik-yukle')
def icerik_yukle():
    # 1. ÖNCE TEMİZLİK
    eski_konular = Konu.query.all()
    for k in eski_konular:
        db.session.delete(k)
    db.session.commit()
    
    # 2. DOLU VE INDEX UYUMLU İÇERİK
    konu_listesi = [
        {
            "sira": 1, 
            "baslik": "Genel İlkyardım Bilgileri", 
            "resim": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&q=80&w=800", 
            "icerik": """
                <h4>İlkyardım Nedir?</h4>
                <p>Herhangi bir kaza veya yaşamı tehlikeye düşüren bir durumda, sağlık görevlileri yardıma gelinceye kadar hayatın kurtarılması ya da durumun kötüye gitmesini önleyebilmek amacı ile olay yerinde, tıbbi araç gereç aranmaksızın, mevcut araç ve gereçlerle yapılan ilaçsız uygulamalardır.</p>
                <h4>İlkyardımcının Özellikleri</h4>
                <ul>
                    <li>İnsan vücudu ile ilgili temel bilgilere sahip olmalı,</li>
                    <li>Sakin, kendine güvenen ve pratik olmalı,</li>
                    <li>Eldeki olanakları değerlendirebilmeli,</li>
                    <li>Olayı anında ve doğru olarak haber vermeli (112),</li>
                    <li>Çevredeki kişileri organize edebilmelidir.</li>
                </ul>
                <h5>Hayat Kurtarma Zinciri</h5>
                <p>1. Halka: Sağlık kuruluşuna haber verme (112).</p>
                <p>2. Halka: Olay yerinde temel yaşam desteği yapılması.</p>
                <p>3. Halka: Ambulans ekiplerince müdahaleler yapılması.</p>
                <p>4. Halka: Hastane acil servislerinde müdahale yapılması.</p>
            """
        },
        {
            "sira": 2, 
            "baslik": "Olay Yerinin Değerlendirilmesi", 
            "resim": "https://images.unsplash.com/photo-1588776813186-643d3999da05?auto=format&fit=crop&q=80&w=800", 
            "icerik": """
                <h4>Olay Yerini Değerlendirme</h4>
                <p>Tekrar kaza olma riskinin ortadan kaldırılması ve hasta/yaralı sayısının belirlenmesidir.</p>
                <h4>Olay Yerinde Yapılacaklar</h4>
                <ul>
                    <li>Kaza yeri işaretlenmelidir (Reflektör vb).</li>
                    <li>Meraklı kişiler uzaklaştırılmalıdır.</li>
                    <li>Patlama/yangın riskine karşı önlemler alınmalıdır.</li>
                    <li>Hasta/yaralı yerinden oynatılmamalıdır.</li>
                </ul>
                <h5>112 Aranırken Nelere Dikkat Edilmeli?</h5>
                <p>Sakin olunmalı, adres net verilmeli, hasta sayısı ve durumları bildirilmelidir.</p>
            """
        },
        {
            "sira": 3,
            "baslik": "Temel Yaşam Desteği (TYD)",
            "resim": "https://images.unsplash.com/photo-1533090161767-e6ffed986c88?auto=format&fit=crop&q=80&w=800",
            "icerik": """
                <h4>Temel Yaşam Desteği Nedir?</h4>
                <p>Solunumu ve/veya kalbi durmuş kişiye hayati fonksiyonlarını geri kazandırmak için yapılan uygulamalardır.</p>
                <h4>Hava Yolu Açıklığı</h4>
                <p>Baş-Çene pozisyonu verilerek hava yolu açılır.</p>
                <h4>Dış Kalp Masajı ve Suni Solunum</h4>
                <p>Yetişkinlerde <strong>30 Kalp Masajı - 2 Suni Solunum</strong> döngüsüyle uygulanır.</p>
                <h5>Çocuklarda ve Bebeklerde</h5>
                <p>Çocuklarda tek elle, bebeklerde iki parmakla kalp masajı yapılır.</p>
            """
        },
        {
            "sira": 4, "baslik": "Kanamalarda İlkyardım", 
            "resim": "https://images.unsplash.com/photo-1628102491629-778571d893a3?auto=format&fit=crop&q=80&w=800", 
            "icerik": "<h4>Kanama Nedir?</h4><p>Damar bütünlüğünün bozulmasıdır.</p><h4>Dış Kanamalarda İlkyardım</h4><p>Yara üzerine temiz bezle baskı uygulanır. Kanama durmazsa ikinci bez konur. Uzuv kopması varsa turnike uygulanır.</p>"
        },
        {
            "sira": 5, "baslik": "Yanıklarda İlkyardım", 
            "resim": "https://images.unsplash.com/photo-1624727828489-a1e03b79bba8?auto=format&fit=crop&q=80&w=800", 
            "icerik": "<h4>Yanık Nedir?</h4><p>Isı, elektrik, kimyasal madde vb. etkisiyle doku bozulmasıdır.</p><h4>İlkyardım</h4><p>Yanık bölge en az 20 dakika tazyiksiz su altına tutulur. Asla diş macunu, yoğurt vb. sürülmez.</p>"
        },
         {
            "sira": 6, "baslik": "Kırık, Çıkık ve Burkulma", 
            "resim": "https://images.unsplash.com/photo-1584515933487-9bfa0024220b?auto=format&fit=crop&q=80&w=800", 
            "icerik": "<h4>Kırık Belirtileri</h4><p>Ağrı, şişlik, şekil bozukluğu.</p><h4>İlkyardım</h4><p>Hareket ettirilmez, tespit edilir (sabitlenir). Açık kırık varsa yara temiz bezle kapatılır.</p>"
        },
         {
            "sira": 7, "baslik": "Bilinç Bozuklukları", 
            "resim": "https://images.unsplash.com/photo-1516574187841-693019951ac4?auto=format&fit=crop&q=80&w=800", 
            "icerik": "<h4>Bayılma</h4><p>Kısa süreli bilinç kaybı.</p><h4>Koma</h4><p>Uzun süreli bilinç kaybı. Koma pozisyonu (yarı yüzükoyun yan yatış) verilir.</p>"
        },
         {
            "sira": 8, "baslik": "Zehirlenmeler", 
            "resim": "https://images.unsplash.com/photo-1607619056574-7b8d3ee536b2?auto=format&fit=crop&q=80&w=800", 
            "icerik": "<h4>Sindirim Yoluyla</h4><p>Kusturulmaz (yakıcı maddeyse), 114 aranır.</p><h4>Solunum Yoluyla</h4><p>Temiz havaya çıkarılır.</p>"
        },
         {
            "sira": 9, "baslik": "Hayvan Isırmaları", 
            "resim": "https://images.unsplash.com/photo-1535930749574-1399327ce78f?auto=format&fit=crop&q=80&w=800", 
            "icerik": "<h4>Kedi-Köpek Isırması</h4><p>Yara 5 dakika sabunlu suyla yıkanır. Kuduz aşısı için sağlık kuruluşuna gidilir.</p>"
        },
        {
            "sira": 10, "baslik": "Göze Yabancı Cisim", 
            "resim": "https://images.unsplash.com/photo-1506477331477-33d5d8b3dc85?auto=format&fit=crop&q=80&w=800", 
            "icerik": "<h4>Toz Kaçması</h4><p>Göz ovuşturulmaz, bol su ile yıkanır veya nemli bezle alınır.</p><h4>Batan Cisim</h4><p>Asla çıkarılmaya çalışılmaz, her iki göz kapatılarak hastaneye sevk edilir.</p>"
        },
        {
            "sira": 11, "baslik": "Boğulmalar", 
            "resim": "https://images.unsplash.com/photo-1531168556467-80aace0d0144?auto=format&fit=crop&q=80&w=800", 
            "icerik": "<h4>Suda Boğulma</h4><p>Sudan çıkarılır, solunum kontrol edilir. Gerekirse Temel Yaşam Desteği başlanır.</p>"
        },
        {
            "sira": 12, "baslik": "Taşıma Teknikleri", 
            "resim": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?auto=format&fit=crop&q=80&w=800", 
            "icerik": "<h4>Genel Kural</h4><p>Mümkünse hasta taşınmaz. Taşınacaksa baş-boyun-gövde ekseni korunur.</p><h4>Sürükleme Yöntemi</h4><p>Dar alanlarda veya hasta çok kiloluysa kullanılır.</p>"
        }
    ]

    for data in konu_listesi:
        yeni_konu = Konu(
            sira=data["sira"],
            baslik=data["baslik"],
            icerik=data["icerik"],
            resim=data["resim"]
        )
        db.session.add(yeni_konu)

    # Admin Kontrolü
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        yeni_admin = User(
            username='admin', 
            email='admin@sistem.com', 
            password=generate_password_hash('1234', method='pbkdf2:sha256'), 
            is_admin=True
        )
        db.session.add(yeni_admin)
        print("Admin oluşturuldu.")

    db.session.commit()
    
    return """
    <div style='text-align:center; padding:50px; font-family:sans-serif;'>
        <h1 style='color:#2ecc71; font-size:3em;'>✅ TAMİR EDİLDİ!</h1>
        <p style='font-size:1.5em;'>Eski, bozuk veriler silindi.</p>
        <p style='font-size:1.5em;'>Yeni, HTML formatlı ve Index uyumlu veriler yüklendi.</p>
        <br>
        <a href='/' style='background:#3498db; color:white; padding:15px 30px; text-decoration:none; border-radius:5px;'>SİTEYE DÖN</a>
    </div>
    """

if __name__ == '__main__':
    app.run(debug=True)