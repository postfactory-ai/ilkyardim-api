import os
import re
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix 
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

# --- FIREBASE KÜTÜPHANESİ ---
import firebase_admin
from firebase_admin import credentials, messaging

load_dotenv()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)

# Render HTTPS Ayarı
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gizli-anahtar')
app.config['JSON_AS_ASCII'] = False

# Veritabanı Ayarları
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 👇 İSTEDİĞİN AYAR BURADA 👇
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True, "pool_recycle": 300}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'giris_yap'

# --- FIREBASE BAŞLATMA (GARANTİ YÖNTEM) ---
firebase_app = None
try:
    json_path = "serviceAccountKey.json"
    if os.path.exists(json_path):
        if not firebase_admin._apps:
            cred = credentials.Certificate(json_path)
            firebase_app = firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin Başlatıldı!")
        else:
            firebase_app = firebase_admin.get_app()
    else:
        print("⚠️ UYARI: serviceAccountKey.json bulunamadı! Push bildirimler çalışmayacak.")
except Exception as e:
    print(f"🔥 FIREBASE HATASI: {e}")

# Google OAuth
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

# --- MODELLER ---
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
    a = db.Column(db.String(200))
    b = db.Column(db.String(200))
    c = db.Column(db.String(200))
    d = db.Column(db.String(200))
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

class GeriBildirim(db.Model):
    __tablename__ = 'geri_bildirim'
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    mesaj = db.Column(db.Text, nullable=False)
    kimden = db.Column(db.String(150), nullable=True) 
    tarih = db.Column(db.DateTime, server_default=db.func.now())
    okundu = db.Column(db.Boolean, default=False)

class UserBadge(db.Model):
    __tablename__ = 'user_badge'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_code = db.Column(db.String(50), nullable=False)
    earned_at = db.Column(db.DateTime, server_default=db.func.now())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- YARDIMCI FONKSİYON: PUSH GÖNDER ---
def push_gonder(baslik, mesaj, hedef='/', user_ids=None):
    if not firebase_admin._apps: return False
    try:
        tokens = []
        if user_ids:
            cihazlar = Cihaz.query.filter(Cihaz.user_id.in_(user_ids)).all()
            tokens = [c.token for c in cihazlar if c.token]
        else:
            cihazlar = Cihaz.query.all()
            tokens = [c.token for c in cihazlar if c.token]

        if not tokens: return False

        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=baslik, body=mesaj),
            data={'hedef': hedef},
            android=messaging.AndroidConfig(priority='high', notification=messaging.AndroidNotification(sound='default', channel_id='high_importance_channel', click_action='FLUTTER_NOTIFICATION_CLICK')),
            tokens=tokens,
        )
        messaging.send_each_for_multicast(message)
        return True
    except Exception as e:
        print(f"Push Hatası: {e}")
        return False

# --- API ENDPOINTS ---

@app.route('/api/konular')
def api_get_konular():
    konular = Konu.query.order_by(Konu.sira).all()
    data = [{'id': k.id, 'baslik': k.baslik, 'sira': k.sira, 'resim': None} for k in konular]
    return jsonify(data)

@app.route('/api/konu/<int:id>')
def api_get_konu_detay(id):
    konu = Konu.query.get_or_404(id)
    return jsonify({'id': konu.id, 'baslik': konu.baslik, 'icerik': konu.icerik, 'sira': konu.sira, 'resim': None})

@app.route('/api/quiz/<int:konu_id>')
def api_get_quiz(konu_id):
    sorular = Soru.query.filter_by(konu_id=konu_id).all()
    return jsonify([{'id': s.id, 'soru': s.soru_metni, 'secenekler': { 'A': s.a, 'B': s.b, 'C': s.c, 'D': s.d }, 'dogru_cevap': s.dogru_cevap} for s in sorular])

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
    email = data.get('email')
    if not token: return jsonify({'error': 'Token yok'}), 400
    
    user_id = None
    if email:
        user = User.query.filter_by(email=email).first()
        if user: user_id = user.id

    cihaz = Cihaz.query.filter_by(token=token).first()
    if not cihaz:
        db.session.add(Cihaz(token=token, platform=platform, user_id=user_id))
    else:
        if user_id and not cihaz.user_id: cihaz.user_id = user_id
    db.session.commit()
    return jsonify({'status': 'ok', 'message': 'Cihaz kaydedildi'})

@app.route('/api/feedback', methods=['POST'])
def api_feedback():
    try:
        data = request.json
        baslik = data.get('baslik')
        mesaj = data.get('mesaj')
        kimden = data.get('kimden', 'Misafir')

        if not baslik or not mesaj: return jsonify({'durum': 'hata'}), 400

        # Kaydet
        db.session.add(GeriBildirim(baslik=baslik, mesaj=mesaj, kimden=kimden))
        db.session.commit()
        
        # Adminlere Bildir (Hata olsa da devam et)
        try:
            adminler = User.query.filter_by(is_admin=True).all()
            admin_ids = [u.id for u in adminler]
            if admin_ids:
                push_gonder(f"📩 Yeni Mesaj: {kimden}", f"{baslik}", hedef='/yonetim/mesajlar', user_ids=admin_ids)
        except: pass

        return jsonify({'durum': 'basarili'})
    except Exception as e:
        return jsonify({'durum': 'hata', 'mesaj': str(e)}), 500

@app.route('/api/arama')
def api_arama():
    kelime = request.args.get('q', '')
    sonuclar = []
    if kelime and len(kelime) > 1:
        bulunanlar = Konu.query.filter(or_(Konu.baslik.ilike(f'%{kelime}%'), Konu.icerik.ilike(f'%{kelime}%'))).all()
        for konu in bulunanlar:
            temiz_metin = re.sub('<[^<]+?>', '', konu.icerik)
            match = re.search(re.escape(kelime), temiz_metin, re.IGNORECASE)
            ozet = match.string[max(0, match.start()-60):min(len(temiz_metin), match.end()+60)] if match else temiz_metin[:100]
            if match: ozet = f"...{ozet}..."
            sonuclar.append({'id': konu.id, 'baslik': konu.baslik, 'ozet': ozet, 'sira': konu.sira})
    return jsonify(sonuclar)

@app.route('/api/quiz-sonuc', methods=['POST'])
def api_quiz_sonuc():
    data = request.json
    email, puan = data.get('email'), data.get('puan')
    if not email: return jsonify({'durum': 'ok', 'yeni_rozetler': []})
    user = User.query.filter_by(email=email).first()
    if not user: return jsonify({'durum': 'hata'})
    
    yeni = []
    if not UserBadge.query.filter_by(user_id=user.id, badge_code='cirak').first():
        db.session.add(UserBadge(user_id=user.id, badge_code='cirak'))
        yeni.append('cirak')
    if puan == 100 and not UserBadge.query.filter_by(user_id=user.id, badge_code='usta').first():
        db.session.add(UserBadge(user_id=user.id, badge_code='usta'))
        yeni.append('usta')
    if puan >= 80 and not UserBadge.query.filter_by(user_id=user.id, badge_code='basarili').first():
        db.session.add(UserBadge(user_id=user.id, badge_code='basarili'))
        yeni.append('basarili')
        
    db.session.commit()
    return jsonify({'durum': 'basarili', 'yeni_rozetler': yeni})

@app.route('/api/rozetlerim', methods=['POST'])
def api_rozetlerim():
    data = request.json
    email = data.get('email')
    if not email: return jsonify([])
    user = User.query.filter_by(email=email).first()
    if not user: return jsonify([])
    badges = UserBadge.query.filter_by(user_id=user.id).all()
    return jsonify([b.badge_code for b in badges])

@app.route('/api/kullanici-bilgi', methods=['POST'])
def api_kullanici_bilgi():
    data = request.json
    user = None
    if data.get('google_id'): user = User.query.filter_by(google_id=data.get('google_id')).first()
    elif data.get('email'): user = User.query.filter_by(email=data.get('email')).first()
    if user: return jsonify({'durum': 'tamam', 'ad': user.username, 'email': user.email, 'admin_mi': user.is_admin})
    return jsonify({'durum': 'hata'}), 404

@app.route('/api/mobil-login', methods=['POST'])
def api_mobil_login():
    data = request.json
    email, ad, google_id = data.get('email'), data.get('ad'), data.get('google_id')
    if not email: return jsonify({'hata': 'Email yok'}), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        db.session.add(User(username=ad, email=email, google_id=google_id))
        db.session.commit()
        return jsonify({'durum': 'basarili', 'islem': 'yeni_kayit'})
    return jsonify({'durum': 'basarili', 'islem': 'giris'})

@app.route('/api/giris', methods=['POST'])
def api_giris():
    data = request.json
    user = User.query.filter((User.username == data.get('username')) | (User.email == data.get('username'))).first()
    if user and user.password and check_password_hash(user.password, data.get('password')):
        return jsonify({'durum': 'basarili', 'user': {'id': user.id, 'username': user.username, 'email': user.email, 'is_admin': user.is_admin}})
    return jsonify({'durum': 'hata'}), 401

@app.route('/api/kayit', methods=['POST'])
def api_kayit():
    data = request.json
    if User.query.filter((User.username == data.get('username')) | (User.email == data.get('email'))).first():
        return jsonify({'durum': 'hata', 'mesaj': 'Kullanıcı zaten var'}), 409
    try:
        hashed = generate_password_hash(data.get('password'), method='pbkdf2:sha256')
        new_user = User(username=data.get('username'), email=data.get('email'), password=hashed)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'durum': 'basarili', 'user': {'id': new_user.id, 'username': new_user.username, 'email': new_user.email}})
    except Exception as e: return jsonify({'durum': 'hata', 'mesaj': str(e)}), 500

# --- YÖNETİM PANELİ (HATA KORUMALI) ---
@app.route('/yonetim')
@login_required
def yonetim_index():
    if not current_user.is_admin: return "Yetkisiz"
    try: konular = Konu.query.order_by(Konu.sira).all()
    except: konular = []
    try: duyuru_sayisi = Duyuru.query.count()
    except: duyuru_sayisi = 0
    try: mesaj_sayisi = GeriBildirim.query.filter_by(okundu=False).count()
    except: mesaj_sayisi = -1
    return render_template('admin/index.html', konular=konular, duyuru_sayisi=duyuru_sayisi, mesaj_sayisi=mesaj_sayisi)

@app.route('/yonetim/mesajlar')
@login_required
def yonetim_mesajlar():
    if not current_user.is_admin: return "Yetkisiz"
    try: mesajlar = GeriBildirim.query.order_by(GeriBildirim.tarih.desc()).all()
    except: mesajlar = []
    return render_template('admin/mesajlar.html', mesajlar=mesajlar)

@app.route('/yonetim/hesap', methods=['GET', 'POST'])
@login_required
def yonetim_hesap():
    if not current_user.is_admin: return "Yetkisiz"
    if request.method == 'POST':
        islem = request.form.get('islem_turu')
        if islem == 'sifre_degistir':
            current_user.password = generate_password_hash(request.form.get('yeni_sifre'), method='pbkdf2:sha256')
            db.session.commit()
            flash('✅ Şifre güncellendi.', 'success')
        elif islem == 'admin_ekle':
            if not User.query.filter_by(email=request.form.get('email')).first():
                db.session.add(User(username=request.form.get('kadi'), email=request.form.get('email'), password=generate_password_hash(request.form.get('sifre'), method='pbkdf2:sha256'), is_admin=True))
                db.session.commit()
                flash('✅ Admin eklendi.', 'success')
        return redirect(url_for('yonetim_hesap'))
    adminler = User.query.filter_by(is_admin=True).all()
    return render_template('admin/hesap.html', adminler=adminler)

@app.route('/yonetim/duyurular', methods=['GET', 'POST'])
@login_required
def yonetim_duyurular():
    if not current_user.is_admin: return "Yetkisiz"
    if request.method == 'POST':
        baslik, mesaj = request.form.get('baslik'), request.form.get('mesaj')
        db.session.add(Duyuru(baslik=baslik, mesaj=mesaj, hedef=request.form.get('hedef')))
        db.session.commit()
        push_gonder(baslik, mesaj, hedef=request.form.get('hedef'))
        return redirect(url_for('yonetim_duyurular'))
    try: duyurular = Duyuru.query.order_by(Duyuru.id.desc()).all()
    except: duyurular = []
    return render_template('admin/duyurular.html', duyurular=duyurular)

@app.route('/yonetim/duyuru-sil/<int:id>')
@login_required
def duyuru_sil(id):
    if not current_user.is_admin: return "Yetkisiz"
    db.session.delete(Duyuru.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('yonetim_duyurular'))

@app.route('/yonetim/soru-ekle', methods=['GET', 'POST'])
@login_required
def soru_ekle():
    if not current_user.is_admin: return "Yetkisiz Alan"
    if request.method == 'POST':
        db.session.add(Soru(
            konu_id=request.form.get('konu_id'),
            soru_metni=request.form.get('soru'),
            a=request.form.get('a'), b=request.form.get('b'), c=request.form.get('c'), d=request.form.get('d'),
            dogru_cevap=request.form.get('dogru')
        ))
        db.session.commit()
        flash('✅ Soru eklendi.', 'success')
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

@app.route('/')
def index():
    konular = Konu.query.order_by(Konu.sira).all()
    try: duyurular = Duyuru.query.filter_by(aktif=True).order_by(Duyuru.id.desc()).limit(3).all()
    except: duyurular = []
    return render_template('index.html', konular=konular, duyurular=duyurular)

@app.route('/konu/<int:id>')
def konu_detay(id):
    konu = Konu.query.get_or_404(id)
    return render_template('detay.html', konu=konu)

@app.route('/arama')
def arama():
    return render_template('arama.html', kelime=request.args.get('q', ''))

@app.route('/quiz')
def quiz_genel():
    konular = Konu.query.order_by(Konu.sira).all()
    return render_template('quiz_secim.html', konular=konular)

@app.route('/quiz/<int:konu_id>')
def quiz_coz(konu_id):
    konu = Konu.query.get_or_404(konu_id)
    sorular = Soru.query.filter_by(konu_id=konu_id).all()
    return render_template('quiz.html', konu=konu, sorular=sorular)

@app.route('/giris', methods=['GET', 'POST'])
def giris_yap():
    if request.method == 'POST':
        user = User.query.filter((User.username == request.form.get('username')) | (User.email == request.form.get('username'))).first()
        if user and user.password and check_password_hash(user.password, request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
        else: flash('Hatalı bilgiler.', 'danger')
    return render_template('login.html')

@app.route('/kayit', methods=['GET', 'POST'])
def kayit_ol():
    if request.method == 'POST':
        if User.query.filter((User.username==request.form.get('username')) | (User.email==request.form.get('email'))).first():
            flash('Kullanıcı mevcut.', 'warning')
            return redirect(url_for('kayit_ol'))
        db.session.add(User(username=request.form.get('username'), email=request.form.get('email'), password=generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')))
        db.session.commit()
        return redirect(url_for('giris_yap'))
    return render_template('register.html')

@app.route('/login/google')
def google_login():
    return google.authorize_redirect(url_for('google_authorize', _external=True))

@app.route('/authorize/google')
def google_authorize():
    try:
        token = google.authorize_access_token()
        user_info = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
        user = User.query.filter_by(google_id=user_info['id']).first()
        if not user:
            user = User.query.filter_by(email=user_info['email']).first()
            if user:
                user.google_id = user_info['id']
            else:
                user = User(username=user_info['name'], email=user_info['email'], google_id=user_info['id'])
                db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    except Exception as e:
        flash(f"Hata: {str(e)}", 'danger')
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

@app.route('/icerik-yukle')
def icerik_yukle():
    if not os.path.exists('yedek_icerik.json'): return "Dosya yok"
    try:
        Konu.query.delete()
        with open('yedek_icerik.json', 'r', encoding='utf-8') as f:
            for data in json.load(f):
                db.session.add(Konu(sira=data.get("sira", 0), baslik=data.get("baslik"), icerik=data.get("icerik")))
        if not User.query.filter_by(username='admin').first():
             db.session.add(User(username='admin', email='admin@sistem.com', password=generate_password_hash('1234', method='pbkdf2:sha256'), is_admin=True))
        db.session.commit()
        return "İçerik Yüklendi"
    except Exception as e: return f"Hata: {str(e)}"

# --- KURULUM / ONARIM (ZORLA SIFIRLAMA) ---
@app.route('/kurulum-yap')
def kurulum():
    try:
        with app.app_context():
            # Sorunlu tabloları kaldırıp yeniden oluşturur (Veri kaybını göze alarak)
            GeriBildirim.__table__.drop(db.engine, checkfirst=True)
            UserBadge.__table__.drop(db.engine, checkfirst=True)
            db.create_all()
        return "✅ KURULUM BAŞARILI! Tablolar sıfırlandı ve onarıldı."
    except Exception as e:
        return f"HATA OLUŞTU: {e}"

if __name__ == '__main__':
    app.run(debug=True)