-- ============================================
-- Yetgim Kütüphane Yönetim Sistemi
-- İndeks Oluşturma (Performans Optimizasyonu)
-- ============================================

USE Kutuphane_Yonetim;

-- KITAPLAR Tablosu İndeksleri
CREATE NONCLUSTERED INDEX idx_Kitaplar_ISBN
ON Kitaplar(ISBN);

CREATE NONCLUSTERED INDEX idx_Kitaplar_YazarID
ON Kitaplar(YazarID);

CREATE NONCLUSTERED INDEX idx_Kitaplar_Kategori
ON Kitaplar(Kategori);

-- ÜYELER Tablosu İndeksleri
CREATE NONCLUSTERED INDEX idx_Uyeler_TC_Kimlik
ON Uyeler(TC_Kimlik);

CREATE NONCLUSTERED INDEX idx_Uyeler_Email
ON Uyeler(Email);

CREATE NONCLUSTERED INDEX idx_Uyeler_Uyelik_Durumu
ON Uyeler(Uyelik_Durumu);

-- ÖDÜNÇ_HAREKETLERİ Tablosu İndeksleri (Kritik)
CREATE NONCLUSTERED INDEX idx_Odenç_KitapID
ON Odenç_Hareketleri(KitapID);

CREATE NONCLUSTERED INDEX idx_Odenç_UyeID
ON Odenç_Hareketleri(UyeID);

-- Compound Index: Ödünç sorgularında tarih aralığı (Most Important)
CREATE NONCLUSTERED INDEX idx_Odenç_Tarihi_Composite
ON Odenç_Hareketleri(Odenç_Tarihi, UyeID, KitapID)
INCLUDE (Iade_Tarihi_Gercek, Ceza_Tutari);

-- İade tarihine göre sorgular için
CREATE NONCLUSTERED INDEX idx_Odenç_Iade_Planlandi
ON Odenç_Hareketleri(Iade_Tarihi_Planlandi)
WHERE Iade_Tarihi_Gercek IS NULL;

-- YAZARLAR Tablosu İndeksleri
CREATE NONCLUSTERED INDEX idx_Yazarlar_Ad_Soyad
ON Yazarlar(Ad_Soyad);

-- TAKVİM Tablosu İndeksleri
CREATE NONCLUSTERED INDEX idx_Takvim_Tarih
ON Takvim(Tarih);

CREATE NONCLUSTERED INDEX idx_Takvim_Yil_Ay
ON Takvim(Yil, Ay);

PRINT 'İndeksler başarıyla oluşturuldu.';
PRINT 'Sistem şu an en iyi performans için optimize edilmiştir.';
