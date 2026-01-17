-- ============================================
-- Yetgim Kütüphane Yönetim Sistemi
-- Tablo Oluşturma Script
-- ============================================

USE Kutuphane_Yonetim;

-- 1. YAZARLAR TABLOSU
CREATE TABLE Yazarlar (
    YazarID INT PRIMARY KEY IDENTITY(1,1),
    Ad_Soyad VARCHAR(100) NOT NULL,
    Dogum_Tarihi DATE NULL,
    Milliyet VARCHAR(50) NULL,
    Biyografi TEXT NULL,
    Kitap_Sayisi INT DEFAULT 0,
    Olusturma_Tarihi DATETIME DEFAULT GETDATE(),
    Aktif BIT DEFAULT 1
);

-- 2. KITAPLAR TABLOSU
CREATE TABLE Kitaplar (
    KitapID INT PRIMARY KEY IDENTITY(1,1),
    ISBN VARCHAR(20) UNIQUE NOT NULL,
    Baslik VARCHAR(255) NOT NULL,
    YazarID INT NOT NULL,
    Kategori VARCHAR(50) NULL,
    Basim_Tarihi DATE NULL,
    Sayfa_Sayisi INT NULL,
    Stok_Miktari INT DEFAULT 0,
    Odenç_Sayisi INT DEFAULT 0,
    Olusturma_Tarihi DATETIME DEFAULT GETDATE(),
    Aktif BIT DEFAULT 1,
    FOREIGN KEY (YazarID) REFERENCES Yazarlar(YazarID)
);

-- 3. ÜYELER TABLOSU
CREATE TABLE Uyeler (
    UyeID INT PRIMARY KEY IDENTITY(1,1),
    Ad_Soyad VARCHAR(100) NOT NULL,
    TC_Kimlik VARCHAR(11) UNIQUE NOT NULL,
    Email VARCHAR(100) UNIQUE NULL,
    Telefon VARCHAR(15) NULL,
    Adres VARCHAR(255) NULL,
    Uyelik_Tarihi DATE DEFAULT CAST(GETDATE() AS DATE),
    Uyelik_Durumu VARCHAR(20) DEFAULT 'Aktif' CHECK (Uyelik_Durumu IN ('Aktif', 'Pasif', 'Askida')),
    Toplam_Odenç_Sayisi INT DEFAULT 0,
    Ceza_Miktari DECIMAL(10,2) DEFAULT 0,
    Son_Aktivite_Tarihi DATE NULL,
    Olusturma_Tarihi DATETIME DEFAULT GETDATE()
);

-- 4. ÖDÜNÇ_HAREKETLERİ TABLOSU
CREATE TABLE Odenç_Hareketleri (
    HareketID INT PRIMARY KEY IDENTITY(1,1),
    KitapID INT NOT NULL,
    UyeID INT NOT NULL,
    Odenç_Tarihi DATE NOT NULL,
    Iade_Tarihi_Planlandi DATE NOT NULL,
    Iade_Tarihi_Gercek DATE NULL,
    Gun_Sayisi INT NULL,
    Gecikmeli BIT DEFAULT 0,
    Ceza_Tutari DECIMAL(10,2) DEFAULT 0,
    Notlar TEXT NULL,
    Olusturma_Tarihi DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (KitapID) REFERENCES Kitaplar(KitapID),
    FOREIGN KEY (UyeID) REFERENCES Uyeler(UyeID)
);

-- 5. TAKVİM TABLOSU (Power BI için)
CREATE TABLE Takvim (
    TarihID INT PRIMARY KEY,
    Tarih DATE UNIQUE NOT NULL,
    Yil INT NOT NULL,
    Ay INT NOT NULL,
    Ay_Adi VARCHAR(20) NOT NULL,
    Gun INT NOT NULL,
    Haftanin_Gunu VARCHAR(20) NOT NULL,
    Hafta_Numarasi INT NULL,
    Ceyrek INT NULL,
    Ayin_Ilk_Gunu DATE NULL,
    Ayin_Son_Gunu DATE NULL
);

PRINT 'Tüm tablolar başarıyla oluşturuldu.';
