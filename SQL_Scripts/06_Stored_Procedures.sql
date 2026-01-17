-- ============================================
-- Yetgim Kütüphane Yönetim Sistemi
-- Stored Procedures (İşletim Prosedürleri)
-- ============================================

USE Kutuphane_Yonetim;

-- PROCEDURE 1: Yeni Ödünç Hareketini Kaydetme
CREATE OR ALTER PROCEDURE sp_Yeni_Odenç_Kaydet
    @KitapID INT,
    @UyeID INT,
    @Odenç_Tarihi DATE,
    @Iade_Tarihi_Planlandi DATE,
    @Notlar NVARCHAR(MAX) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    
    BEGIN TRY
        -- Ödünç Hareketi Ekleme
        INSERT INTO Odenç_Hareketleri (KitapID, UyeID, Odenç_Tarihi, Iade_Tarihi_Planlandi, Notlar)
        VALUES (@KitapID, @UyeID, @Odenç_Tarihi, @Iade_Tarihi_Planlandi, @Notlar);
        
        -- Üyenin Son Aktivite Tarihini Güncelleme
        UPDATE Uyeler
        SET Son_Aktivite_Tarihi = @Odenç_Tarihi,
            Toplam_Odenç_Sayisi = Toplam_Odenç_Sayisi + 1
        WHERE UyeID = @UyeID;
        
        -- Kitabın Ödünç Sayısını Artırma
        UPDATE Kitaplar
        SET Odenç_Sayisi = Odenç_Sayisi + 1
        WHERE KitapID = @KitapID;
        
        COMMIT TRANSACTION;
        PRINT 'Ödünç hareketi başarıyla kaydedildi.';
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        PRINT 'Hata: ' + ERROR_MESSAGE();
    END CATCH;
END;

-- PROCEDURE 2: İade Işlemi Tamamlama
CREATE OR ALTER PROCEDURE sp_Iade_Işlemi_Tamamla
    @HareketID INT,
    @Iade_Tarihi_Gercek DATE
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    
    BEGIN TRY
        DECLARE @UyeID INT;
        DECLARE @Iade_Tarihi_Planlandi DATE;
        DECLARE @Gecikmiş_Gün INT;
        DECLARE @Ceza_Tutari DECIMAL(10,2);
        
        -- Hareket Bilgisini Çek
        SELECT @UyeID = UyeID, @Iade_Tarihi_Planlandi = Iade_Tarihi_Planlandi
        FROM Odenç_Hareketleri
        WHERE HareketID = @HareketID;
        
        -- Gecikmiş Gün Sayısını Hesapla
        SET @Gecikmiş_Gün = DATEDIFF(DAY, @Iade_Tarihi_Planlandi, @Iade_Tarihi_Gercek);
        
        -- Ceza Tutarını Hesapla (Günde 5 TL)
        IF @Gecikmiş_Gün > 0
            SET @Ceza_Tutari = @Gecikmiş_Gün * 5
        ELSE
            SET @Ceza_Tutari = 0;
        
        -- Hareket Tablosunu Güncelle
        UPDATE Odenç_Hareketleri
        SET Iade_Tarihi_Gercek = @Iade_Tarihi_Gercek,
            Gun_Sayisi = DATEDIFF(DAY, Odenç_Tarihi, @Iade_Tarihi_Gercek),
            Gecikmeli = CASE WHEN @Gecikmiş_Gün > 0 THEN 1 ELSE 0 END,
            Ceza_Tutari = @Ceza_Tutari
        WHERE HareketID = @HareketID;
        
        -- Üyenin Ceza Miktarını Güncelle
        UPDATE Uyeler
        SET Ceza_Miktari = Ceza_Miktari + @Ceza_Tutari
        WHERE UyeID = @UyeID;
        
        COMMIT TRANSACTION;
        PRINT 'İade işlemi tamamlanmıştır. Ceza: ' + CAST(@Ceza_Tutari AS VARCHAR(10)) + ' TL';
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        PRINT 'Hata: ' + ERROR_MESSAGE();
    END CATCH;
END;

-- PROCEDURE 3: Gecikmiş Ödünçleri Listeleme
CREATE OR ALTER PROCEDURE sp_Gecikmiş_Odenç_Listesi
AS
BEGIN
    SET NOCOUNT ON;
    SELECT TOP 100 *
    FROM vw_Gecikmiş_Iadeleler
    ORDER BY Gecikmiş_Gun DESC;
END;

-- PROCEDURE 4: Üye Ödünç Geçmişini Görüntüleme
CREATE OR ALTER PROCEDURE sp_Uye_Odenç_Gecmisi
    @UyeID INT
AS
BEGIN
    SET NOCOUNT ON;
    SELECT 
        o.HareketID,
        k.Baslik,
        k.ISBN,
        y.Ad_Soyad AS Yazar,
        o.Odenç_Tarihi,
        o.Iade_Tarihi_Planlandi,
        o.Iade_Tarihi_Gercek,
        o.Gun_Sayisi,
        CASE WHEN o.Gecikmeli = 1 THEN 'Evet' ELSE 'Hayır' END AS Gecikmeli,
        o.Ceza_Tutari
    FROM Odenç_Hareketleri o
    INNER JOIN Kitaplar k ON o.KitapID = k.KitapID
    INNER JOIN Yazarlar y ON k.YazarID = y.YazarID
    WHERE o.UyeID = @UyeID
    ORDER BY o.Odenç_Tarihi DESC;
END;

-- PROCEDURE 5: Kitap Ekle
CREATE OR ALTER PROCEDURE sp_Kitap_Ekle
    @ISBN VARCHAR(20),
    @Baslik VARCHAR(255),
    @YazarID INT,
    @Kategori VARCHAR(50),
    @Basim_Tarihi DATE,
    @Sayfa_Sayisi INT,
    @Stok_Miktari INT = 0
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRANSACTION;
    
    BEGIN TRY
        INSERT INTO Kitaplar (ISBN, Baslik, YazarID, Kategori, Basim_Tarihi, Sayfa_Sayisi, Stok_Miktari)
        VALUES (@ISBN, @Baslik, @YazarID, @Kategori, @Basim_Tarihi, @Sayfa_Sayisi, @Stok_Miktari);
        
        UPDATE Yazarlar
        SET Kitap_Sayisi = Kitap_Sayisi + 1
        WHERE YazarID = @YazarID;
        
        COMMIT TRANSACTION;
        PRINT 'Kitap başarıyla eklendi.';
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        PRINT 'Hata: ' + ERROR_MESSAGE();
    END CATCH;
END;

-- PROCEDURE 6: Üye Kayıt
CREATE OR ALTER PROCEDURE sp_Uye_Kayit
    @Ad_Soyad VARCHAR(100),
    @TC_Kimlik VARCHAR(11),
    @Email VARCHAR(100),
    @Telefon VARCHAR(15),
    @Adres VARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        INSERT INTO Uyeler (Ad_Soyad, TC_Kimlik, Email, Telefon, Adres, Uyelik_Tarihi, Uyelik_Durumu)
        VALUES (@Ad_Soyad, @TC_Kimlik, @Email, @Telefon, @Adres, CAST(GETDATE() AS DATE), 'Aktif');
        
        PRINT 'Üye başarıyla kaydedildi.';
    END TRY
    BEGIN CATCH
        PRINT 'Hata: ' + ERROR_MESSAGE();
    END CATCH;
END;

PRINT 'Tüm Stored Procedure''ler başarıyla oluşturuldu.';
