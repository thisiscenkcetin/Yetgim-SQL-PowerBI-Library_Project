# DAX FORMÜLLERI - Power BI Measures ve Calculations

## Measures (Ölçüler) - Power BI'da Tanımlanacak

### Temel KPI'lar

```dax
-- 1. Toplam Kitap Sayısı
Toplam_Kitap = COUNTA(Kitaplar[KitapID])

-- 2. Toplam Üye Sayısı
Toplam_Üye = COUNTA(Uyeler[UyeID])

-- 3. Aktif Üye Sayısı
Aktif_Üye = CALCULATE(
    COUNTA(Uyeler[UyeID]),
    Uyeler[Uyelik_Durumu] = "Aktif"
)

-- 4. Toplam Ödünç Sayısı
Toplam_Odenç = COUNTA(Odenç_Hareketleri[HareketID])

-- 5. Aktif Ödünç Sayısı (İadesi Beklenen)
Aktif_Odenç = CALCULATE(
    COUNTA(Odenç_Hareketleri[HareketID]),
    Odenç_Hareketleri[Iade_Tarihi_Gercek] = BLANK()
)

-- 6. Gecikmiş Ödünç Sayısı
Gecikmiş_Odenç = CALCULATE(
    COUNTA(Odenç_Hareketleri[HareketID]),
    Odenç_Hareketleri[Gecikmeli] = 1,
    Odenç_Hareketleri[Iade_Tarihi_Gercek] = BLANK()
)

-- 7. Toplam Ceza Miktarı
Toplam_Ceza = SUM(Odenç_Hareketleri[Ceza_Tutari])

-- 8. Ödenmemiş Ceza
Odenmemis_Ceza = CALCULATE(
    SUM(Uyeler[Ceza_Miktari]),
    Uyeler[Ceza_Miktari] > 0
)
```

### Kategori ve Kitap Analizleri

```dax
-- 9. Kategoriye Göre Ödünç Sayısı
Kategori_Odenç = CALCULATE(
    COUNTA(Odenç_Hareketleri[HareketID]),
    ALLEXCEPT(Kitaplar, Kitaplar[Kategori])
)

-- 10. Kitap Ödünç Yüzdesi
Odenç_Yüzdesi = DIVIDE(
    COUNTA(Odenç_Hareketleri[HareketID]),
    [Toplam_Odenç]
) * 100

-- 11. Kategori Başına Ortalama Ödünç
Kategori_Ort_Odenç = AVERAGEX(
    VALUES(Kitaplar[Kategori]),
    CALCULATE(COUNTA(Odenç_Hareketleri[HareketID]))
)

-- 12. En Popüler Kitap (Bu Dönemde)
En_Popüler_Kitap = TOPN(
    1,
    SUMMARIZE(Kitaplar, Kitaplar[Baslik], Kitaplar[KitapID]),
    CALCULATE(COUNTA(Odenç_Hareketleri[HareketID])),
    DESC
)
```

### Üye Analizleri

```dax
-- 13. Üye Aktivite Durumu (Segment)
Aktivite_Durumu = IF(
    CALCULATE(COUNTA(Odenç_Hareketleri[HareketID])) > 20,
    "Çok Aktif",
    IF(
        CALCULATE(COUNTA(Odenç_Hareketleri[HareketID])) > 5,
        "Orta Aktif",
        IF(
            CALCULATE(COUNTA(Odenç_Hareketleri[HareketID])) > 0,
            "Az Aktif",
            "Pasif"
        )
    )
)

-- 14. Üye Başına Ödünç Oranı
Uye_Odenç_Orani = DIVIDE(
    [Toplam_Odenç],
    [Toplam_Üye]
)

-- 15. Pasif Üye Sayısı (6+ ay hiç ödünç almamış)
Pasif_Üye_Sayisi = CALCULATE(
    COUNTA(Uyeler[UyeID]),
    Uyeler[Son_Aktivite_Tarihi] < TODAY() - 180
)
```

### Gecikme ve Ceza Analizleri

```dax
-- 16. Ortalama Gecikme Günü
Ort_Gecikme_Gunu = AVERAGEX(
    FILTER(
        Odenç_Hareketleri,
        Odenç_Hareketleri[Gecikmeli] = 1
    ),
    DATEDIFF(
        Odenç_Hareketleri[Iade_Tarihi_Planlandi],
        Odenç_Hareketleri[Iade_Tarihi_Gercek],
        DAY
    )
)

-- 17. Gecikme Oranı (%)
Gecikme_Orani = DIVIDE(
    [Gecikmiş_Odenç],
    [Toplam_Odenç]
) * 100

-- 18. En Fazla Gecikmiş Üye
En_Fazla_Gecikmiş_Üye = CALCULATE(
    MAX(Uyeler[Ceza_Miktari]),
    ALLEXCEPT(Uyeler, Uyeler[Ad_Soyad])
)

-- 19. Ceza Toplamı (Bu Ay)
Bu_Ay_Ceza = CALCULATE(
    [Toplam_Ceza],
    MONTH(Odenç_Hareketleri[Odenç_Tarihi]) = MONTH(TODAY()),
    YEAR(Odenç_Hareketleri[Odenç_Tarihi]) = YEAR(TODAY())
)
```

### Stok Analizleri

```dax
-- 20. Toplam Stok Miktarı
Toplam_Stok = SUM(Kitaplar[Stok_Miktari])

-- 21. Yetersiz Stok Sayısı (≤5)
Yetersiz_Stok_Sayisi = CALCULATE(
    COUNTA(Kitaplar[KitapID]),
    Kitaplar[Stok_Miktari] <= 5
)

-- 22. Stok Bitmiş Kitap Sayısı
Stok_Bitmis_Sayisi = CALCULATE(
    COUNTA(Kitaplar[KitapID]),
    Kitaplar[Stok_Miktari] = 0
)

-- 23. Stok Turnaover Oranı (Ödünç/Stok)
Stok_Turnover = DIVIDE(
    COUNTA(Odenç_Hareketleri[HareketID]),
    [Toplam_Stok]
)

-- 24. Kategoriye Göre Stok Durumu
Kategori_Stok = SUM(Kitaplar[Stok_Miktari])
```

### Tarih Tabanlı Analizler

```dax
-- 25. Aylık Ödünç Sayısı
Aylik_Odenç = CALCULATE(
    COUNTA(Odenç_Hareketleri[HareketID]),
    Takvim[Ay] = MONTH(TODAY()),
    Takvim[Yil] = YEAR(TODAY())
)

-- 26. Yıllık Ödünç Sayısı
Yillik_Odenç = CALCULATE(
    COUNTA(Odenç_Hareketleri[HareketID]),
    YEAR(Odenç_Hareketleri[Odenç_Tarihi]) = YEAR(TODAY())
)

-- 27. Geçen Aydan Karşılaştırma (%)
Onceki_Ay_Degisim = DIVIDE(
    [Aylik_Odenç],
    CALCULATE(
        [Aylik_Odenç],
        DATEADD(Takvim[Tarih], -1, MONTH)
    )
) - 1

-- 28. Yeni Üye Sayısı (Bu Ay)
Bu_Ay_Yeni_Uye = CALCULATE(
    COUNTA(Uyeler[UyeID]),
    MONTH(Uyeler[Uyelik_Tarihi]) = MONTH(TODAY()),
    YEAR(Uyeler[Uyelik_Tarihi]) = YEAR(TODAY())
)
```

---

## Calculated Columns (Hesaplanmış Sütunlar)

Bu sütunlar **tablo görsellerinde** önemlidir:

```dax
-- Ödünç_Hareketleri tablosuna:
Gecikmiş_Gün = DATEDIFF(
    [Iade_Tarihi_Planlandi],
    [Iade_Tarihi_Gercek],
    DAY
)

Ceza_TL = MAX(0, [Gecikmiş_Gün] * 5)

Durum = IF([Iade_Tarihi_Gercek] = BLANK(), "Bekleniyor", "İade Edildi")

-- Kitaplar tablosuna:
Stok_Kategorisi = IF(
    [Stok_Miktari] = 0,
    "Stok Bitti",
    IF([Stok_Miktari] <= 5, "Az Stok", "Yeterli")
)

-- Üyeler tablosuna:
Ceza_Durumu = IF([Ceza_Miktari] > 0, "Vardır", "Yok")
```

---

## DAX Best Practices

1. **Süzme önceliği:** `CALCULATE(measure, filter1, filter2)` format
2. **Boş kontrol:** `BLANK()` yerine `= ""` kullanmayın
3. **Performans:** `SUMX` yerine `SUM(Calculated Column)` tercih et
4. **Türkçe:** Tüm measure adlarını Türkçe yaz
5. **Yorum:** Karmaşık formülün üstüne `// Açıklama` ekle

---

## Formülleri Power BI'da Kullanmak

1. **Model** → **Manage Roles** → **New Measure**
2. Formülü yapıştır
3. **Enter**
4. Rapor sayfalarında "Fields" panelinden measure'ı sürükle

