# 📚 Streamlit Kütüphane Arayüzü

SQL Server veritabanına bağlı web tabanlı kütüphane yönetim arayüzü.

## 🚀 Başlatma

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port=8080
```

**Giriş:** `kutuphane` / `123456`

## 📋 Özellikler

- Dashboard - Özet istatistikler ve grafikler
- Kitap Yönetimi - Ekle, düzenle, sil
- Üye Yönetimi - Kayıt ve profil işlemleri
- Ödünç/İade - Kitap ödünç alma ve iade
- Raporlar - Popülarite ve trend analizleri

## ⚙️ Ayarlar

Veritabanı ayarları: `.streamlit/secrets.toml`

```toml
[database]
server = "."
database = "Kutuphane_Yonetim"
username = ""  # Windows Auth için boş
password = ""
```

## 📁 Yapı

```
├── streamlit_app.py    # Ana uygulama
├── app_pages/          # Sayfa modülleri
├── modules/            # Yardımcı modüller
├── config/             # Yapılandırma
└── assets/             # Statik dosyalar
```
