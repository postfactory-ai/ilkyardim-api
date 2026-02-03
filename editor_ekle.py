import os
import subprocess

# AYARLAR
BASE_DIR = os.getcwd()
ADMIN_DIR = os.path.join(BASE_DIR, 'templates', 'admin')

print("\033[92m🛠️ YÖNETİM PANELİ GÜÇLENDİRİLİYOR (RICH TEXT EDITOR)...\033[0m")

# Summernote Entegreli Düzenleme Sayfası
duzenle_html = """
{% extends "layout.html" %}

{% block content %}
<link href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">

<div class="container mt-5 mb-5">
    <div class="card shadow-lg border-0">
        <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
            <h4 class="mb-0"><i class="fa-solid fa-pen-to-square"></i> İçerik Düzenle</h4>
            <a href="/yonetim" class="btn btn-outline-light btn-sm">Geri Dön</a>
        </div>
        <div class="card-body p-4">
            <form method="POST">
                
                <div class="mb-4">
                    <label class="form-label fw-bold">Konu Başlığı</label>
                    <input type="text" name="baslik" class="form-control form-control-lg" value="{{ konu.baslik }}" required>
                </div>

                <div class="mb-4">
                    <label class="form-label fw-bold">Kapak Resmi (URL)</label>
                    <div class="input-group">
                        <span class="input-group-text"><i class="fa-solid fa-image"></i></span>
                        <input type="text" name="resim" class="form-control" value="{{ konu.resim if konu.resim else '' }}" placeholder="https://...">
                    </div>
                    <small class="text-muted">Unsplash veya Google Görsellerden resim adresi yapıştır.</small>
                </div>

                <div class="mb-4">
                    <label class="form-label fw-bold">İçerik</label>
                    <textarea id="summernote" name="icerik">{{ konu.icerik }}</textarea>
                </div>

                <div class="d-grid gap-2">
                    <button type="submit" class="btn btn-success btn-lg"><i class="fa-solid fa-save"></i> DEĞİŞİKLİKLERİ KAYDET</button>
                </div>
            </form>
        </div>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>
<script>
    $(document).ready(function() {
        $('#summernote').summernote({
            placeholder: 'İçeriği buraya yazın...',
            tabsize: 2,
            height: 400,
            toolbar: [
                ['style', ['style']],
                ['font', ['bold', 'underline', 'clear']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['table', ['table']],
                ['insert', ['link', 'picture', 'video']],
                ['view', ['fullscreen', 'codeview', 'help']]
            ]
        });
    });
</script>
{% endblock %}
"""

with open(os.path.join(ADMIN_DIR, 'duzenle.html'), 'w', encoding='utf-8') as f:
    f.write(duzenle_html)

print("✅ Editör eklendi. GitHub'a gönderiliyor...")

# Git Komutları
subprocess.run("git add -A", shell=True)
subprocess.run('git commit -m "Admin Paneline Summernote Editor Eklendi"', shell=True)
subprocess.run("git push", shell=True)

print("🚀 GÖNDERİLDİ! Vercel güncellenince panelde Word gibi editör çıkacak.")