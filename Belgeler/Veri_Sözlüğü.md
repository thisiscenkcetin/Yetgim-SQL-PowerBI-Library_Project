# VERİ SÖZLÜĞÜ - Tüm Tablolar ve Sütunlar

## 1. YAZARLAR Tablosu

| Sütun | Tür | Özellik | Açıklama |
|---|---|---|---|
| YazarID | INT | PK, AUTO_INCREMENT | Yazarın benzersiz ID'si |
| Ad_Soyad | VARCHAR(100) | NOT NULL | Yazarın adı ve soyadı |
| Dogum_Tarihi | DATE | NULLABLE | Yazarın doğum tarihi |
| Milliyet | VARCHAR(50) | NULLABLE | Yazarın ülkesi (Türk, İngiliz, vs.) |
| Biyografi | TEXT | NULLABLE | Yazarın hayatı hakkında bilgi |
| Kitap_Sayisi | INT | DEFAULT 0 | Kütüphanede bulunan kitap sayısı |
| Olusturma_Tarihi | DATETIME | DEFAULT GETDATE() | Kaydın oluşturma tarihi |
| Aktif | BIT | DEFAULT 1 | 1=Aktif, 0=Silinmiş |

**İndeksler:** Ad_Soyad

---

## 2. KITAPLAR Tablosu

| Sütun | Tür | Özellik | Açıklama |
|---|---|---|---|
| KitapID | INT | PK, AUTO_INCREMENT | Kitabın benzersiz ID'si |
| ISBN | VARCHAR(20) | UNIQUE, NOT NULL | Kitabın ISBN kodu |
| Baslik | VARCHAR(255) | NOT NULL | Kitabın başlığı |
| YazarID | INT | FK, NOT NULL | Kitabın yazarı (Yazarlar tablosu) |
| Kategori | VARCHAR(50) | NULLABLE | Kitab kategorisi (Fiksiyon, Bilim, vs.) |
| Basim_Tarihi | DATE | NULLABLE | Kitabın basılış tarihi |
| Sayfa_Sayisi | INT | NULLABLE | Kitabın sayfa sayısı |
| Stok_Miktari | INT | DEFAULT 0 | Şu anki stok adedi |
| Odenç_Sayisi | INT | DEFAULT 0 | Toplam kaç kez ödünç verilmiş |
| Olusturma_Tarihi | DATETIME | DEFAULT GETDATE() | Kaydın oluşturma tarihi |
| Aktif | BIT | DEFAULT 1 | 1=Aktif, 0=Silinmiş |

**İndeksler:** ISBN, YazarID, Kategori

**Kategoriler Örneği:** Fiksiyon, Bilim, İş, Eğitim, Şiir, Öykü, Tiyatro, Felsefe, Macera, Distopya, Bilim Kurgu, Sosyal, Çocuk

---

## 3. ÜYELER Tablosu

| Sütun | Tür | Özellik | Açıklama |
|---|---|---|---|
| UyeID | INT | PK, AUTO_INCREMENT | Üyenin benzersiz ID'si |
| Ad_Soyad | VARCHAR(100) | NOT NULL | Üyenin adı ve soyadı |
| TC_Kimlik | VARCHAR(11) | UNIQUE, NOT NULL | T.C. Kimlik numarası |
| Email | VARCHAR(100) | UNIQUE, NULLABLE | Üyenin email adresi |
| Telefon | VARCHAR(15) | NULLABLE | Üyenin telefon numarası |
| Adres | VARCHAR(255) | NULLABLE | Üyenin adresi |
| Uyelik_Tarihi | DATE | DEFAULT TODAY() | Üyelik başlama tarihi |
| Uyelik_Durumu | VARCHAR(20) | CHECK, DEFAULT 'Aktif' | Aktif / Pasif / Askıda |
| Toplam_Odenç_Sayisi | INT | DEFAULT 0 | Şu ana kadar kaç kitap ödünç aldı |
| Ceza_Miktari | DECIMAL(10,2) | DEFAULT 0 | Ödenmemiş toplam ceza (TL) |
| Son_Aktivite_Tarihi | DATE | NULLABLE | Son ödünç aldığı tarih |
| Olusturma_Tarihi | DATETIME | DEFAULT GETDATE() | Kaydın oluşturma tarihi |

**İndeksler:** TC_Kimlik, Email, Uyelik_Durumu

**Üyelik Durumları:**
- **Aktif:** Kütüphaneye aktif olarak üye
- **Pasif:** Uzun süre hiç kitap almamış
- **Askıda:** Ceza veya diğer nedenler yüzünden geçici olarak pasif

---

## 4. ÖDÜNÇ_HAREKETLERİ Tablosu

| Sütun | Tür | Özellik | Açıklama |
|---|---|---|---|
| HareketID | INT | PK, AUTO_INCREMENT | Hareketin benzersiz ID'si |
| KitapID | INT | FK, NOT NULL | Ödünç alınan kitap |
| UyeID | INT | FK, NOT NULL | Kitabı ödünç alan üye |
| Odenç_Tarihi | DATE | NOT NULL | Kitabın ödünç alındığı tarih |
| Iade_Tarihi_Planlandi | DATE | NOT NULL | Kitabın iade edileceği planlanmış tarih (14 gün sonrası) |
| Iade_Tarihi_Gercek | DATE | NULLABLE | Kitabın gerçek iade tarihı (NULL = henüz iadesiz) |
| Gun_Sayisi | INT | NULLABLE | Kitap ne kadar gün ödünç tutuldu |
| Gecikmeli | BIT | DEFAULT 0 | 1=Gecikmeli, 0=Zamanında |
| Ceza_Tutari | DECIMAL(10,2) | DEFAULT 0 | Gecikme cezası (Gün × 5 TL) |
| Notlar | TEXT | NULLABLE | İşlemle ilgili notlar |
| Olusturma_Tarihi | DATETIME | DEFAULT GETDATE() | Kaydın oluşturma tarihi |

**İndeksler:** KitapID, UyeID, Odenç_Tarihi (Composite), Iade_Tarihi_Planlandi

**Önemli Notlar:**
- Iade_Tarihi_Planlandi otomatik olarak Odenç_Tarihi + 14 gün
- Gun_Sayisi = Iade_Tarihi_Gercek - Odenç_Tarihi
- Ceza = MAX(0, (Iade_Tarihi_Gercek - Iade_Tarihi_Planlandi) × 5)

---

## 5. TAKVİM Tablosu (Power BI Boyut Tablosu)

| Sütun | Tür | Özellik | Açıklama |
|---|---|---|---|
| TarihID | INT | PK | Tarih ID (YYYYMMDD formatında) |
| Tarih | DATE | UNIQUE, NOT NULL | Takvim tarihi |
| Yil | INT | NOT NULL | Yıl (2023, 2024, 2025, 2026) |
| Ay | INT | NOT NULL | Ay numarası (1-12) |
| Ay_Adi | VARCHAR(20) | NOT NULL | Ayın adı (Ocak, Şubat, ... Aralık) |
| Gun | INT | NOT NULL | Günü (1-31) |
| Haftanin_Gunu | VARCHAR(20) | NOT NULL | Haftanın günü (Pazartesi, ... Pazar) |
| Hafta_Numarasi | INT | NULLABLE | ISO Hafta numarası (1-52) |
| Ceyrek | INT | NULLABLE | Çeyrek (1, 2, 3, 4) |
| Ayin_Ilk_Gunu | DATE | NULLABLE | Ayın ilk günü |
| Ayin_Son_Gunu | DATE | NULLABLE | Ayın son günü |

**İndeksler:** Tarih, Yil_Ay

**Veri Aralığı:** 2023-01-01 to 2026-12-31 (4 yıl, ~1500 satır)

---

## Veri Tipleri Referansı

| Tip | Kullanım | Örnek |
|---|---|---|
| INT | Tam sayılar, ID'ler | YazarID, Sayfa_Sayisi |
| VARCHAR(n) | Değişken uzunlukta metin | Ad_Soyad, Email |
| DATE | Tarih (TT.AA.YYYY) | Dogum_Tarihi, Odenç_Tarihi |
| DATETIME | Tarih + Saat | Olusturma_Tarihi |
| DECIMAL(10,2) | Para birimleri | Ceza_Tutari (10 digit, 2 decimal) |
| TEXT | Uzun metin | Biyografi, Notlar |
| BIT | Boole (0 veya 1) | Aktif, Gecikmeli |

---

## Kısıtlamalar (Constraints)

| Tablo | Kısıtlama | Açıklama |
|---|---|---|
| Kitaplar | UNIQUE(ISBN) | Her kitabın benzersiz ISBN'si olmalı |
| Uyeler | UNIQUE(TC_Kimlik) | Her üyenin benzersiz TC'si olmalı |
| Uyeler | UNIQUE(Email) | Her üyenin farklı email'i |
| Uyeler | CHECK(Uyelik_Durumu) | Sadece belirtilen durumlar geçerli |
| Kitaplar | FK(YazarID) | Kitabın yazarı Yazarlar tablosunda olmalı |
| Ödünç | FK(KitapID, UyeID) | Ödünç edilen kitap ve üye geçerli olmalı |

