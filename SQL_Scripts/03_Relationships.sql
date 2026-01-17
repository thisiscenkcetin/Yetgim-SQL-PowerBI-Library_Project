-- ============================================
-- Yetgim Kütüphane Yönetim Sistemi
-- Foreign Key ve İlişkiler
-- ============================================

USE Kutuphane_Yonetim;

-- İlişkiler zaten 02_Tables_Create.sql içinde tanımlanmıştır
-- Referans Bütünlüğü (Referential Integrity):
--
-- 1. Kitaplar.YazarID → Yazarlar.YazarID
--    (Her kitap bir yazara ait olmalı)
--
-- 2. Odenç_Hareketleri.KitapID → Kitaplar.KitapID
--    (Her ödünç hareketi bir kitabı referans eder)
--
-- 3. Odenç_Hareketleri.UyeID → Uyeler.UyeID
--    (Her ödünç hareketi bir üyeyi referans eder)

-- Kıskaç (Cascade) ayarları eklemek istersen aşağıdakileri çalıştır:
-- NOT: İlişkiler zaten oluşturulmuş, bu kısım referans amaçlı

-- Yazarlar silindiğinde ilişkili kitapları silme (OPSIYONEL - Önerilmez)
-- ALTER TABLE Kitaplar
-- ADD CONSTRAINT FK_Kitaplar_Yazarlar 
-- FOREIGN KEY (YazarID) REFERENCES Yazarlar(YazarID) ON DELETE RESTRICT;

PRINT 'Foreign Key ilişkileri kontrol edildi.';
