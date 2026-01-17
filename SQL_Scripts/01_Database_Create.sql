-- ============================================
-- Yetgim Kütüphane Yönetim Sistemi
-- Veritabanı Oluşturma Script
-- ============================================

-- Veritabanı oluşturma
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'Kutuphane_Yonetim')
BEGIN
    CREATE DATABASE Kutuphane_Yonetim;
    PRINT 'Veritabanı Kutuphane_Yonetim başarıyla oluşturuldu.';
END
ELSE
BEGIN
    PRINT 'Veritabanı Kutuphane_Yonetim zaten var.';
END
GO

USE Kutuphane_Yonetim;
GO

-- Varsayılan SQL Server ayarları
SET ANSI_NULLS ON;
SET QUOTED_IDENTIFIER ON;

PRINT 'Veritabanı Kutuphane_Yonetim başarıyla oluşturuldu.';
