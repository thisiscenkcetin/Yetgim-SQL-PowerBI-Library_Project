-- ============================================
-- Yetgim Kütüphane Yönetim Sistemi
-- SQL VIEW'ları (Analiz için)
-- ============================================

USE Kutuphane_Yonetim;

-- VIEW 1: Aktif Ödünç Hareketleri (Gecikmiş ve Zamanında)
CREATE OR ALTER VIEW vw_Aktif_Odenç AS
SELECT 
    o.HareketID,
    k.Baslik,
    k.ISBN,
    y.Ad_Soyad AS Yazar,
    u.Ad_Soyad AS Üye,
    u.Email,
    u.Telefon,
    o.Odenç_Tarihi,
    o.Iade_Tarihi_Planlandi,
    DATEDIFF(DAY, o.Iade_Tarihi_Planlandi, CAST(GETDATE() AS DATE)) AS Gecen_Gun_Sayisi,
    CASE 
        WHEN CAST(GETDATE() AS DATE) > o.Iade_Tarihi_Planlandi THEN 'GECİKMİŞ'
        ELSE 'ZAMANINDA'
    END AS Durum,
    o.Ceza_Tutari
FROM Odenç_Hareketleri o
INNER JOIN Kitaplar k ON o.KitapID = k.KitapID
INNER JOIN Yazarlar y ON k.YazarID = y.YazarID
INNER JOIN Uyeler u ON o.UyeID = u.UyeID
WHERE o.Iade_Tarihi_Gercek IS NULL;

-- VIEW 2: Üye İstatistikleri (Ödünç Sayısı, Aktif Ödünç, Son Aktivite)
CREATE OR ALTER VIEW vw_Uye_İstatistikleri AS
SELECT 
    u.UyeID,
    u.Ad_Soyad,
    u.Email,
    u.Uyelik_Tarihi,
    u.Uyelik_Durumu,
    COUNT(o.HareketID) AS Toplam_Odenç_Sayisi,
    SUM(CASE WHEN o.Iade_Tarihi_Gercek IS NULL THEN 1 ELSE 0 END) AS Aktif_Odenç_Sayisi,
    MAX(o.Odenç_Tarihi) AS Son_Odenç_Tarihi,
    SUM(o.Ceza_Tutari) AS Toplam_Ceza_Miktari,
    CASE 
        WHEN COUNT(o.HareketID) > 20 THEN 'Çok Aktif'
        WHEN COUNT(o.HareketID) > 5 THEN 'Orta'
        WHEN COUNT(o.HareketID) > 0 THEN 'Az Aktif'
        ELSE 'Pasif'
    END AS Aktivite_Düzeyi
FROM Uyeler u
LEFT JOIN Odenç_Hareketleri o ON u.UyeID = o.UyeID
GROUP BY u.UyeID, u.Ad_Soyad, u.Email, u.Uyelik_Tarihi, u.Uyelik_Durumu;

-- VIEW 3: Kitap Popülarite Sıralaması (En Çok Ödünç Verilen)
CREATE OR ALTER VIEW vw_Kitap_Popülarite AS
SELECT 
    k.KitapID,
    k.Baslik,
    k.ISBN,
    y.Ad_Soyad AS Yazar,
    k.Kategori,
    k.Stok_Miktari,
    COUNT(o.HareketID) AS Odenç_Sayisi,
    ROUND(CAST(COUNT(o.HareketID) AS FLOAT) * 100.0 / 
        (SELECT CAST(COUNT(*) AS FLOAT) FROM Odenç_Hareketleri), 2) AS Odenç_Yüzdesi,
    CASE 
        WHEN k.Stok_Miktari <= 0 THEN 'Stok Bitti'
        WHEN k.Stok_Miktari <= 5 THEN 'Az Stok'
        ELSE 'Yeterli Stok'
    END AS Stok_Durumu
FROM Kitaplar k
LEFT JOIN Odenç_Hareketleri o ON k.KitapID = o.KitapID
LEFT JOIN Yazarlar y ON k.YazarID = y.YazarID
GROUP BY k.KitapID, k.Baslik, k.ISBN, y.Ad_Soyad, k.Kategori, k.Stok_Miktari
ORDER BY Odenç_Sayisi DESC;

-- VIEW 4: Gecikmiş İadeler ve Cezalar
CREATE OR ALTER VIEW vw_Gecikmiş_Iadeleler AS
SELECT 
    o.HareketID,
    u.Ad_Soyad AS Üye_Adi,
    u.Email,
    u.Telefon,
    u.Ceza_Miktari AS Toplam_Ceza_Miktari,
    k.Baslik AS Kitap_Adi,
    y.Ad_Soyad AS Yazar_Adi,
    o.Odenç_Tarihi,
    o.Iade_Tarihi_Planlandi,
    DATEDIFF(DAY, o.Iade_Tarihi_Planlandi, CAST(GETDATE() AS DATE)) AS Gecikmiş_Gun,
    DATEDIFF(DAY, o.Iade_Tarihi_Planlandi, CAST(GETDATE() AS DATE)) * 5 AS Tahmini_Ceza_Tutari
FROM Odenç_Hareketleri o
INNER JOIN Uyeler u ON o.UyeID = u.UyeID
INNER JOIN Kitaplar k ON o.KitapID = k.KitapID
INNER JOIN Yazarlar y ON k.YazarID = y.YazarID
WHERE o.Iade_Tarihi_Gercek IS NULL 
  AND CAST(GETDATE() AS DATE) > o.Iade_Tarihi_Planlandi
ORDER BY DATEDIFF(DAY, o.Iade_Tarihi_Planlandi, CAST(GETDATE() AS DATE)) DESC;

-- VIEW 5: Aylık Ödünç Trendi
CREATE OR ALTER VIEW vw_Aylik_Odenç_Trendi AS
SELECT 
    YEAR(o.Odenç_Tarihi) AS Yil,
    MONTH(o.Odenç_Tarihi) AS Ay,
    CASE MONTH(o.Odenç_Tarihi)
        WHEN 1 THEN 'Ocak' WHEN 2 THEN 'Şubat' WHEN 3 THEN 'Mart'
        WHEN 4 THEN 'Nisan' WHEN 5 THEN 'Mayıs' WHEN 6 THEN 'Haziran'
        WHEN 7 THEN 'Temmuz' WHEN 8 THEN 'Ağustos' WHEN 9 THEN 'Eylül'
        WHEN 10 THEN 'Ekim' WHEN 11 THEN 'Kasım' WHEN 12 THEN 'Aralık'
    END AS Ay_Adi,
    COUNT(o.HareketID) AS Toplam_Odenç,
    SUM(CASE WHEN o.Iade_Tarihi_Gercek IS NOT NULL THEN 1 ELSE 0 END) AS Iade_Edilen,
    SUM(CASE WHEN o.Iade_Tarihi_Gercek IS NULL THEN 1 ELSE 0 END) AS Penderler,
    AVG(DATEDIFF(DAY, o.Odenç_Tarihi, ISNULL(o.Iade_Tarihi_Gercek, CAST(GETDATE() AS DATE)))) AS Ort_Odenç_Gunu
FROM Odenç_Hareketleri o
GROUP BY YEAR(o.Odenç_Tarihi), MONTH(o.Odenç_Tarihi)
ORDER BY Yil DESC, Ay DESC;

-- VIEW 6: Kategoriye Göre Ödünç Dağılımı
CREATE OR ALTER VIEW vw_Kategori_Odenç_Dagilimi AS
SELECT 
    k.Kategori,
    COUNT(o.HareketID) AS Odenç_Sayisi,
    COUNT(DISTINCT k.KitapID) AS Kitap_Sayisi,
    ROUND(CAST(COUNT(o.HareketID) AS FLOAT) * 100.0 / 
        (SELECT CAST(COUNT(*) AS FLOAT) FROM Odenç_Hareketleri), 2) AS Yuzde
FROM Kitaplar k
LEFT JOIN Odenç_Hareketleri o ON k.KitapID = o.KitapID
WHERE k.Kategori IS NOT NULL
GROUP BY k.Kategori
ORDER BY Odenç_Sayisi DESC;

-- VIEW 7: Yazar Istatistikleri
CREATE OR ALTER VIEW vw_Yazar_İstatistikleri AS
SELECT 
    y.YazarID,
    y.Ad_Soyad,
    y.Milliyet,
    COUNT(DISTINCT k.KitapID) AS Kitap_Sayisi,
    COUNT(o.HareketID) AS Toplam_Odenç_Sayisi,
    ROUND(CAST(COUNT(o.HareketID) AS FLOAT) * 100.0 / 
        (SELECT CAST(COUNT(*) AS FLOAT) FROM Odenç_Hareketleri), 2) AS Toplam_Odenç_Yüzdesi
FROM Yazarlar y
LEFT JOIN Kitaplar k ON y.YazarID = k.YazarID
LEFT JOIN Odenç_Hareketleri o ON k.KitapID = o.KitapID
GROUP BY y.YazarID, y.Ad_Soyad, y.Milliyet
ORDER BY Toplam_Odenç_Sayisi DESC;

-- VIEW 8: Stok Durumu Özeti
CREATE OR ALTER VIEW vw_Stok_Durumu_Ozeti AS
SELECT 
    k.KitapID,
    k.Baslik,
    y.Ad_Soyad AS Yazar,
    k.Kategori,
    k.Stok_Miktari,
    CASE 
        WHEN k.Stok_Miktari <= 0 THEN 'Stok Bitti'
        WHEN k.Stok_Miktari <= 5 THEN 'Yetersiz Stok'
        WHEN k.Stok_Miktari <= 20 THEN 'Normal Stok'
        ELSE 'Yüksek Stok'
    END AS Stok_Kategorisi,
    COUNT(o.HareketID) AS Toplam_Odenç_Sayisi
FROM Kitaplar k
LEFT JOIN Yazarlar y ON k.YazarID = y.YazarID
LEFT JOIN Odenç_Hareketleri o ON k.KitapID = o.KitapID
GROUP BY k.KitapID, k.Baslik, y.Ad_Soyad, k.Kategori, k.Stok_Miktari
ORDER BY k.Stok_Miktari ASC;

PRINT 'Tüm VIEW''lar başarıyla oluşturuldu.';
