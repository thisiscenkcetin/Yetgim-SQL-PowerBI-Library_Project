# Sistem Sabit Değerleri

# Ödünç Ayarları
DEFAULT_ODENÇ_SURESI = 14  # gün
ODENÇ_CEZASI_GUNLUK = 5.0  # TL
MAKSIMUM_ODENÇ_SAYISI = 5
MAKSIMUM_CEZA_LIMITI = 100.0  # TL

# Üyelik Durumları
UYELIK_DURUMLARI = ["Aktif", "Pasif", "Askıda"]
DEFAULT_UYELIK_DURUMU = "Aktif"

# Kitap Kategorileri
KITAP_KATEGORILERI = [
    "Fiksiyon",
    "Bilim",
    "İş",
    "Eğitim",
    "Şiir",
    "Öykü",
    "Tiyatro",
    "Felsefe",
    "Macera",
    "Distopya",
    "Bilim Kurgu",
    "Sosyal",
    "Çocuk",
    "Tarih"
]

# Kullanıcı Rolleri (tek yetkili kütüphaneci hesabı)
ROLES = {
    "kutuphane": {
        "password": "123456",
        "role": "Kütüphaneci",
        # Tek hesap, tüm izinler
        "permissions": ["read", "write", "write_odenç", "write_iade", "admin"]
    }
}

# Mesajlar
MESSAGES = {
    "odenç_basarili": "✅ Ödünç hareketi başarıyla kaydedildi!",
    "iade_basarili": "✅ İade işlemi tamamlandı.",
    "uye_kayit_basarili": "✅ Üyeyi başarıyla kaydettik.",
    "kitap_eklendi": "✅ Kitap başarıyla eklendi.",
    "hata_veritabani": "❌ Veritabanı hatası oluştu. Lütfen daha sonra tekrar deneyin.",
    "hata_gecersiz": "❌ Geçersiz veriler girdiniz.",
    "uyari_ceza": "⚠️ Bu üyenin X TL cezası var!",
}
