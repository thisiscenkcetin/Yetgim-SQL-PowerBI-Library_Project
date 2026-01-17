# KURULUM REHBERİ

## Adım 1: Veritabanı Kurulumu

### SQL Server / SQL Server Express Kullanıyorsanız:

1. **SQL Server Management Studio (SSMS)** açın
2. Sunucuya bağlanın
3. Yeni Query penceresi aç → **F5 ya da Ctrl+Shift+E**
4. Aşağıdaki SQL scriptleri sırasıyla çalıştırın:

```sql
-- 1. Veritabanını Oluştur
EXEC sp_executesql N'01_Database_Create.sql'

-- 2. Tabloları Oluştur
EXEC sp_executesql N'02_Tables_Create.sql'

-- 3. İlişkileri Kontrol Et
EXEC sp_executesql N'03_Relationships.sql'

-- 4. Örnek Veri Yükle
EXEC sp_executesql N'04_Sample_Data.sql'

-- 5. View'ları Oluştur
EXEC sp_executesql N'05_Views.sql'

-- 6. Stored Procedure'leri Oluştur
EXEC sp_executesql N'06_Stored_Procedures.sql'

-- 7. İndeksleri Oluştur
EXEC sp_executesql N'07_Indexes.sql'
```

**VEYA Daha Pratik:** Her dosyayı ayrı ayrı SSMS'te açıp **Ctrl+A** → **F5** ile çalıştırın.

---

## Adım 2: MySQL Kullanıyorsanız

```bash
# Terminal'de girin
mysql -u root -p

# MySQL komut satırında
CREATE DATABASE Kutuphane_Yonetim;
USE Kutuphane_Yonetim;
SOURCE SQL_Scripts/02_Tables_Create.sql;
SOURCE SQL_Scripts/04_Sample_Data.sql;
SOURCE SQL_Scripts/05_Views.sql;
SOURCE SQL_Scripts/06_Stored_Procedures.sql;
```

---

## Adım 3: Veri Kontrolü

Kurulum bittikten sonra, verilerin doğru yüklendiğini kontrol edin:

```sql
-- Yazarlar kontrolü
SELECT COUNT(*) AS Yazar_Sayisi FROM Yazarlar;

-- Kitaplar kontrolü
SELECT COUNT(*) AS Kitap_Sayisi FROM Kitaplar;

-- Üyeler kontrolü
SELECT COUNT(*) AS Üye_Sayisi FROM Uyeler;

-- Ödünç Hareketleri
SELECT COUNT(*) AS Hareket_Sayisi FROM Odenç_Hareketleri;
```

**Beklenen Sonuç:**
- Yazarlar: ~50
- Kitaplar: ~70 (70'in üzerinde)
- Üyeler: ~30
- Ödünç Hareketleri: Başlangıçta 0 (test için eklenecek)

---

## Adım 4: Power BI'a Bağlantı

### Power BI Desktop Açın

1. **Power BI Desktop** → **Get Data** → **SQL Server**
2. Server: `localhost` (veya `.<instance_name>` eğer Named Instance ise)
3. Database: `Kutuphane_Yonetim`
4. **Tables** sekmesinden aşağıdakileri seç:
   - Yazarlar
   - Kitaplar
   - Üyeler
   - Ödünç_Hareketleri
   - Takvim

5. **Load** ve **Close & Apply** tıkla

### Model İlişkilerini Kur (Power BI)

**Model** sekmesinde:

| From | To | Relationship |
|---|---|---|
| Kitaplar[YazarID] | Yazarlar[YazarID] | 1:N, Single |
| Ödünç_Hareketleri[KitapID] | Kitaplar[KitapID] | N:1, Single |
| Ödünç_Hareketleri[UyeID] | Üyeler[UyeID] | N:1, Single |
| Ödünç_Hareketleri[Odenç_Tarihi] | Takvim[Tarih] | N:1, Single |

---

## Adım 5: Test Sorguları

Kurulum başarılı mı diye test etmek için aşağıdaki sorguları çalıştırın:

### Test 1: Popüler Kitapları Göster
```sql
SELECT TOP 10 * FROM vw_Kitap_Popülarite;
```

### Test 2: En Aktif Üyeleri Göster
```sql
SELECT TOP 10 * FROM vw_Uye_İstatistikleri ORDER BY Toplam_Odenç_Sayisi DESC;
```

### Test 3: Yazar İstatistikleri
```sql
SELECT TOP 5 * FROM vw_Yazar_İstatistikleri;
```

---

## Adım 6: Ödünç İşlemi Yapma (Test)

### Yeni Ödünç Kaydı (Stored Procedure ile)

```sql
-- KitapID=1, UyeID=1, Bugün ödünç, 14 gün sonra iade planlanmış
EXEC sp_Yeni_Odenç_Kaydet
    @KitapID = 1,
    @UyeID = 1,
    @Odenç_Tarihi = '2025-01-17',
    @Iade_Tarihi_Planlandi = '2025-01-31',
    @Notlar = 'Test ödünç işlemi';
```

### İade İşlemini Tamamla

```sql
-- HareketID=1 olan kitabı iade et (15 gün sonra = 1 gün gecikmeli)
EXEC sp_Iade_Işlemi_Tamamla
    @HareketID = 1,
    @Iade_Tarihi_Gercek = '2025-02-01';
```

### Sonucu Kontrol Et
```sql
SELECT * FROM vw_Gecikmiş_Iadeleler;
```

---

## Sorun Giderme

### Problem: "Veritabanı zaten var" hatası
**Çözüm:** Existing veritabanını silin veya adı değiştirin
```sql
DROP DATABASE Kutuphane_Yonetim;
```

### Problem: Foreign Key hatası
**Çözüm:** Tablolar yanlış sırayla oluşturulmuş. **02_Tables_Create.sql** dosyasını silip yeniden çalıştırın.

### Problem: GETDATE() hatası
**Çözüm:** Sunucun tarih ayarı yanlış. Sistem saatini kontrol edin.

### Problem: Permission Denied
**Çözüm:** SQL'de yetkiniz yok. Admin olarak SSMS açın.

