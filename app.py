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

# Veritabanı
db_url = os.environ.get("DATABASE_URL")
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///local.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True, "pool_recycle": 300}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'giris_yap'

# --- FIREBASE BAŞLATMA ---
try:
    if not firebase_admin._apps:
        if os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
            firebase_admin.initialize_app(cred)
            print("✅ Firebase Admin Başlatıldı!")
        else:
            print("⚠️ serviceAccountKey.json bulunamadı! Push bildirim çalışmayacak.")
except Exception as e:
    print(f"⚠️ Firebase Admin Hatası: {e}")

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

# YENİ EKLENEN TABLO: Feedback
class GeriBildirim(db.Model):
    __tablename__ = 'geri_bildirim'
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=False)
    mesaj = db.Column(db.Text, nullable=False)
    tarih = db.Column(db.DateTime, server_default=db.func.now())
    okundu = db.Column(db.Boolean, default=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- API ENDPOINTS ---

@app.route('/api/konular')
def api_get_konular():
    konular = Konu.query.order_by(Konu.sira).all()
    data = [{'id': k.id, 'baslik': k.baslik, 'sira': k.sira, 'resim': None} for k in konular]
    return jsonify(data)

@app.route('/api/konu/<int:id>')
def api_get_konu_detay(id):
    konu = Konu.query.get_or_404(id)
    return jsonify({
        'id': konu.id,
        'baslik': konu.baslik,
        'icerik': konu.icerik,
        'sira': konu.sira,
        'resim': None
    })

@app.route('/api/quiz/<int:konu_id>')
def api_get_quiz(konu_id):
    sorular = Soru.query.filter_by(konu_id=konu_id).all()
    return jsonify([{
        'id': s.id,
        'soru': s.soru_metni,
        'secenekler': { 'A': s.a, 'B': s.b, 'C': s.c, 'D': s.d },
        'dogru_cevap': s.dogru_cevap
    } for s in sorular])

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
        return jsonify({'status': 'ok', 'message': 'Yeni cihaz kaydedildi'})
    
    return jsonify({'status': 'ok', 'message': 'Cihaz zaten kayitli'})

# YENİ API: Feedback Kaydet
@app.route('/api/feedback', methods=['POST'])
def api_feedback():
    data = request.json
    baslik = data.get('baslik')
    mesaj = data.get('mesaj')

    if not baslik or not mesaj:
        return jsonify({'durum': 'hata', 'mesaj': 'Başlık ve mesaj zorunludur.'}), 400

    yeni_bildirim = GeriBildirim(baslik=baslik, mesaj=mesaj)
    db.session.add(yeni_bildirim)
    db.session.commit()
    
    return jsonify({'durum': 'basarili', 'mesaj': 'Geri bildiriminiz alındı!'})

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

# --- MOBİL GİRİŞ & KAYIT ---
@app.route('/api/kullanici-bilgi', methods=['POST'])
def api_kullanici_bilgi():
    data = request.json
    google_id = data.get('google_id')
    email = data.get('email')
    user = None
    if google_id:
        user = User.query.filter_by(google_id=google_id).first()
    elif email:
        user = User.query.filter_by(email=email).first()
        
    if user:
        return jsonify({
            'durum': 'tamam',
            'ad': user.username,
            'email': user.email,
            'admin_mi': user.is_admin
        })
    else:
        return jsonify({'durum': 'hata', 'mesaj': 'Kullanıcı bulunamadı'}), 404

@app.route('/api/mobil-login', methods=['POST'])
def api_mobil_login():
    data = request.json
    email = data.get('email')
    ad = data.get('ad')
    google_id = data.get('google_id')
    
    if not email: return jsonify({'hata': 'Email yok'}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        yeni_user = User(username=ad, email=email, google_id=google_id, password=None)
        db.session.add(yeni_user)
        db.session.commit()
        islem = "yeni_kayit"
    else:
        if not user.google_id:
            user.google_id = google_id
            db.session.commit()
        islem = "giris"
        
    return jsonify({'durum': 'basarili', 'islem': islem})

@app.route('/api/giris', methods=['POST'])
def api_giris():
    data = request.json
    girdi = data.get('username')
    sifre = data.get('password')

    if not girdi or not sifre:
        return jsonify({'durum': 'hata', 'mesaj': 'Eksik bilgi!'}), 400

    user = User.query.filter((User.username == girdi) | (User.email == girdi)).first()
    
    if user and user.password and check_password_hash(user.password, sifre):
        return jsonify({
            'durum': 'basarili',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin
            }
        })
    else:
        return jsonify({'durum': 'hata', 'mesaj': 'Hatalı kullanıcı adı veya şifre!'}), 401

@app.route('/api/kayit', methods=['POST'])
def api_kayit():
    data = request.json
    kadi = data.get('username')
    email = data.get('email')
    sifre = data.get('password')

    if not kadi or not email or not sifre:
        return jsonify({'durum': 'hata', 'mesaj': 'Tüm alanları doldurun!'}), 400

    if User.query.filter((User.username == kadi) | (User.email == email)).first():
        return jsonify({'durum': 'hata', 'mesaj': 'Bu kullanıcı zaten kayıtlı!'}), 409

    try:
        hashed_pw = generate_password_hash(sifre, method='pbkdf2:sha256')
        yeni_user = User(username=kadi, email=email, password=hashed_pw)
        db.session.add(yeni_user)
        db.session.commit()
        
        return jsonify({
            'durum': 'basarili',
            'user': {
                'id': yeni_user.id,
                'username': yeni_user.username,
                'email': yeni_user.email,
                'is_admin': yeni_user.is_admin
            }
        })
    except Exception as e:
        return jsonify({'durum': 'hata', 'mesaj': str(e)}), 500

# --- PANEL & YÖNETİM ---
@app.route('/yonetim')
@login_required
def yonetim_index():
    if not current_user.is_admin: return "Yetkisiz"
    konular = Konu.query.order_by(Konu.sira).all()
    duyuru_sayisi = Duyuru.query.count()
    mesaj_sayisi = GeriBildirim.query.filter_by(okundu=False).count() # Okunmamış mesajlar
    return render_template('admin/index.html', konular=konular, duyuru_sayisi=duyuru_sayisi, mesaj_sayisi=mesaj_sayisi)

# YENİ PANEL SAYFASI: MESAJLAR
@app.route('/yonetim/mesajlar')
@login_required
def yonetim_mesajlar():
    if not current_user.is_admin: return "Yetkisiz"
    mesajlar = GeriBildirim.query.order_by(GeriBildirim.tarih.desc()).all()
    return render_template('admin/mesajlar.html', mesajlar=mesajlar)

@app.route('/yonetim/hesap', methods=['GET', 'POST'])
@login_required
def yonetim_hesap():
    if not current_user.is_admin: return "Yetkisiz"
    if request.method == 'POST':
        islem = request.form.get('islem_turu')
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
        elif islem == 'admin_ekle':
            kadi = request.form.get('kadi')
            email = request.form.get('email')
            sifre = request.form.get('sifre')
            if User.query.filter((User.username==kadi) | (User.email==email)).first():
                flash('⚠️ Kullanıcı zaten var.', 'warning')
            else:
                yeni_admin = User(username=kadi, email=email, password=generate_password_hash(sifre, method='pbkdf2:sha256'), is_admin=True)
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
        
        # --- PUSH BİLDİRİM ---
        try:
            tum_cihazlar = Cihaz.query.all()
            tokens = [c.token for c in tum_cihazlar if c.token]
            
            if tokens:
                message = messaging.MulticastMessage(
                    notification=messaging.Notification(
                        title=baslik,
                        body=mesaj,
                    ),
                    data={'hedef': hedef},
                    android=messaging.AndroidConfig(
                        priority='high',
                        notification=messaging.AndroidNotification(
                            sound='default',
                            channel_id='high_importance_channel',
                            click_action='FLUTTER_NOTIFICATION_CLICK'
                        )
                    ),
                    tokens=tokens,
                )
                response = messaging.send_each_for_multicast(message)
                flash(f'✅ Bildirim {response.success_count} cihaza ulaştı!', 'success')
            else:
                flash('⚠️ Kayıtlı cihaz yok, sadece veritabanına eklendi.', 'warning')
        except Exception as e:
            print(f"PUSH HATASI: {e}")
            flash(f'⚠️ Push Hatası: {e}', 'warning')

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

# --- WEB YOLLARI ---
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

# --- AUTH ---
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
            flash('Kullanıcı mevcut.', 'warning')
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
        flash('Başarılı giriş.', 'success')
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
    return "Kurulum/Onarim Tamam."

@app.route('/icerik-yukle')
def icerik_yukle():
    dosya_adi = 'yedek_icerik.json'
    if not os.path.exists(dosya_adi): return "HATA: Dosya yok"
    try:
        with open(dosya_adi, 'r', encoding='utf-8') as f:
            konu_listesi = json.load(f)
        Konu.query.delete()
        for data in konu_listesi:
            db.session.add(Konu(sira=data.get("sira", 0), baslik=data.get("baslik"), icerik=data.get("icerik"), resim=None))
        if not User.query.filter_by(username='admin').first():
             db.session.add(User(username='admin', email='admin@sistem.com', password=generate_password_hash('1234', method='pbkdf2:sha256'), is_admin=True))
        db.session.commit()
        return "İçerik Yüklendi"
    except Exception as e:
        return f"HATA: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)