# POWER BI RAPOR TASARIMI

## Genel Yapı

**Dosya Adı:** `Yetgim_Kutuphane_Yonetim.pbix`

**Sayfa Sayısı:** 5 (Ana Dashboard + 4 Detay Raporu)

**Filtre Yapısı:** Global (Takvim, Kategori) + Sayfa Bazında (Durum, Dönem)

---

## SAYFA 1: DASHBOARD (Özet Kontrol Paneli)

### Layout
```
┌─────────────────────────────────────────────────────────┐
│           YETGIM KUTUPHANE YÖNETİM SISTEMI             │
│              Dashboard - Güncel Durum                   │
└─────────────────────────────────────────────────────────┘

┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Toplam      │ │  Aktif       │ │  Aktif       │ │  Gecikmiş    │
│  Kitaplar    │ │  Üyeler      │ │  Ödünçler    │ │  İadeler     │
│  [Toplam_Kitap] │ [Aktif_Üye] │ [Aktif_Odenç] │ [Gecikmiş_Odenç]
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

┌─────────────────────────────────┐  ┌───────────────────────────────┐
│ Aylık Ödünç Trendi (Çizgi)      │  │ Kategorilere Göre (Donut)     │
│ Son 12 Ay                        │  │ Kitap Dağılımı                │
│                                  │  │ Fiksiyon, Bilim, İş, vs.      │
│ [Alan Grafik]                    │  │ [Alan Grafik]                 │
│                                  │  │                               │
│                                  │  │                               │
└─────────────────────────────────┘  └───────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│ Slicer (Filtreler)                                               │
│ [Yıl ▼]  [Ay ▼]  [Kategori ▼]  [Durum ▼]                        │
└──────────────────────────────────────────────────────────────────┘
```

### Görseller Detayı

**KPI Kartlar (4 adet)** - Sağ üst köşede
- Renk Şeması: Yeşil (Toplam), Mavi (Aktif), Sarı (Ödünç), Kırmızı (Gecikmiş)
- Font: Büyük sayılar (36pt), Açıklama (12pt)
- Format: `#,##0` (Türkçe ayraç)

**Aylık Ödünç Trendi (Çizgi Grafik)** - Sol alt
- X Ekseni: Ay (Ocak, Şubat, ..., Aralık)
- Y Ekseni: Ödünç Sayısı
- Seri: Mavi çizgi, işaretçiler
- Efsane: Sağ üst

**Kategori Dağılımı (Donut Chart)** - Sağ alt
- Dilimler: Her kategori farklı renk
- İç Yazı: Kategori adı + %
- Açılmış Görünüm: Seçilen dilim vurgulanır
- İnteraktif: Kategoriye tıklanınca diğer sayfalar filtreler

---

## SAYFA 2: POPÜLER KITAPLAR & YAZARLAR

### Layout
```
┌──────────────────────────────────────────────────────────┐
│ TOP 10 KITAPLAR (Tablo)      │ TOP 5 YAZARLAR (Bar)     │
│ Sıra | Başlık | Yazar | Ödünç│ 1. [Yazar] - Ödünç Sayısı│
│ 1.   | Kar    | ...   | 45   │ 2. ...                  │
│ ...                          │ ...                      │
│                              │                         │
│                              │ [Alan Grafik]           │
│                              │                         │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────┐  ┌──────────────────────────┐
│ KATEGORİLERE GÖRE        │  │ ARANAN KİTAPLAR          │
│ (Yatay Bar Chart)        │  │ (Tablo - Stok Bitti)    │
│ Fiksiyon: 156            │  │ Kitap | Ödünç Sayısı    │
│ Bilim: 98                │  │ ...                     │
│ İş: 67                   │  │                         │
│ ...                      │  │                         │
│ [Alan Grafik]            │  │ [Alan Grafik]           │
│                          │  │                         │
└──────────────────────────┘  └──────────────────────────┘
```

### Görseller Detayı

**Top 10 Kitaplar (Tablo)**
- Sütunlar: Sıra, Kitap Başlığı, Yazar, Ödünç Sayısı, Stok Durumu
- Koşullu Biçimlendirme: Stok durumuna göre renk (Kırmızı=Bitti, Sarı=Az, Yeşil=Normal)
- Sıralama: Ödünç Sayısı DESC

**Top 5 Yazarlar (Bar Chart - Yatay)**
- X Ekseni: Ödünç Sayısı
- Y Ekseni: Yazar Adı
- Veri Etiketleri: Açık (Sayı gösterilsin)

**Kategorilere Göre (Bar Chart - Yatay)**
- Renk Gradyent: Açık mavi → Koyu mavi (Ödünç sayısına göre)

**Aranan Kitaplar (Tablo)**
- Sadece Stok_Kategorisi = "Stok Bitti" olan kitaplar
- Sütunlar: Başlık, Yazar, Ödünç Sayısı, Son İade
- Sıralama: Ödünç Sayısı DESC (En çok talep görenleri yukarı)

---

## SAYFA 3: GECİKMİŞ İADELER & CEZALAR

### Layout
```
┌──────────────────────┐ ┌──────────────────────────────┐
│ Toplam Ceza (KPI)    │ │ Ödenmemiş Ceza (KPI)         │
│ 15.500 TL            │ │ 8.750 TL                     │
└──────────────────────┘ └──────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ GECİKMİŞ ÖDÜNÇLER (Tablo)                             │
│ Üye | Kitap | Gün | Ceza | İletişim | Hareket Tarihi  │
│ ... | ...   | ..  | ...  │ ...      │ ...             │
└────────────────────────────────────────────────────────┘

┌────────────────────────────┐  ┌───────────────────────┐
│ HAFTALIK GECİKMİŞ TREND    │  │ EN FAZLA CEZALI 5     │
│ (Çizgi Grafik)             │  │ ÜYE (Bar)             │
│                            │  │ Üye Adı | Ceza        │
│ [Alan Grafik]              │  │ 1. ... | 2.500 TL     │
│                            │  │ ...                   │
│                            │  │ [Alan Grafik]         │
│                            │  │                       │
└────────────────────────────┘  └───────────────────────┘
```

### Görseller Detayı

**Gecikmiş Ödünçler (Tablo)**
- Sütunlar: Üye Adı, Email, Telefon, Kitap Başlığı, Gecikmiş Gün, Tahmini Ceza
- Koşullu Biçimlendirme: Gün sayısına göre renk (Kırmızı = 30+ gün)
- Sıralama: Gecikmiş Gün DESC
- Sayfa Boyutu: 15-20 satır (kaydırılabilir)

**Haftalık Trend (Çizgi Grafik)**
- X Ekseni: Hafta numarası
- Y Ekseni: Gecikmiş Ödünç Sayısı
- Filtreleme: Sadece Gecikmeli = 1 ve İade_Tarihi_Gercek = NULL

**En Fazla Cezalı Üyeler (Bar - Yatay)**
- Top 5 Üye
- Renk: Kırmızı tonları (Ceza miktarına göre yoğunluk)
- Veri Etiketi: TL cinsinden

---

## SAYFA 4: AYLIK TREND ANALİZİ

### Layout
```
┌────────────────────────────────────────────────────────┐
│ AYLIK ÖDÜNÇ KARŞILAŞTIRMASI (Sütun + Çizgi Combo)     │
│ Sütun: Toplam Ödünç, Çizgi: İade Oranı (%)            │
│ [Alan Grafik - Büyük]                                 │
│                                                        │
│                                                        │
│                                                        │
│                                                        │
└────────────────────────────────────────────────────────┘

┌──────────────────────────┐  ┌──────────────────────────┐
│ AYLIK İSTATİSTİK (Tablo)│  │ AYLIK CEZA TOPLAMI (Bar) │
│ Ay | Ödünç | İade | Pnd │  │ [Alan Grafik]            │
│ ... | ... | ... | ... │  │                         │
│                          │  │                         │
└──────────────────────────┘  └──────────────────────────┘
```

### Görseller Detayı

**Aylık Ödünç Kombinasyon (Sütun + Çizgi)**
- Sütun: Ödünç Sayısı (Mavi)
- Çizgi: İade Oranı (%) (Kırmızı)
- İkinci Y Ekseni: 0-100%
- X Ekseni: Ay (Ocak, ..., Aralık)
- Trend: Mevsimsel alışkanlıkları gösterir

**Aylık İstatistik (Tablo)**
- Sütunlar: Ay, Toplam Ödünç, İade Edilen, Penderler, Ort. Gün
- Formül: Penderler = Ödünç - İade
- Sıralama: Ay DESC (Son aylar üstte)

**Aylık Ceza (Bar Chart)**
- Kategoriler: Aylar
- Değerler: Ceza Tutarı (TL)
- Renk Gradyent: Kırmızı (Yüksek ceza) → Sarı (Düşük ceza)

---

## SAYFA 5A: STOK DURUMU

### Layout
```
┌──────────────────────────┐  ┌──────────────────────────┐
│ TOPLAM STOK MİKTARI      │  │ YETERSİZ STOK SAYISI    │
│ KPI Kartı: 2.450         │  │ KPI Kartı: 12 Kitap    │
└──────────────────────────┘  └──────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ KATEGORİYE GÖRE STOK (Donut)   │ STOK DURUMU (Tablo)   │
│ [Alan]                         │ Kategori | Stok | Dur │
│                                │ ...      | ...  | ... │
│                                │          │      │     │
│                                │ [Alan]   │      │     │
└────────────────────────────────────────────────────────┘
```

---

## SAYFA 5B: ÜYE AKTİVİTESİ

### Layout
```
┌──────────────────────────┐  ┌──────────────────────────┐
│ EN AKTİF 10 ÜYE (Bar)    │  │ ÜYELİK DURUMU (Pie)      │
│                          │  │ Aktif: 55                │
│ [Alan Grafik]            │  │ Pasif: 12                │
│                          │  │ Askıda: 3                │
│                          │  │ [Alan Grafik]            │
│                          │  │                         │
└──────────────────────────┘  └──────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ ÜYELERE GÖRE CEZA (Top 10 - Tablo)                    │
│ Üye Adı | Email | Ceza | Durum | İletişim             │
│ ...                                                    │
└────────────────────────────────────────────────────────┘

┌──────────────────────────┐  ┌──────────────────────────┐
│ AYLIK YENİ ÜYE TRENDI    │  │ AKTİVİTE SEGMENTASYONU  │
│ (Çizgi)                  │  │ (Donut)                  │
│ [Alan Grafik]            │  │ Çok Aktif: 20            │
│                          │  │ Orta: 30                 │
│                          │  │ Az Aktif: 10             │
│                          │  │ Pasif: 10                │
│                          │  │ [Alan Grafik]            │
└──────────────────────────┘  └──────────────────────────┘
```

---

## RENK ŞEMASI (Tema - Türkçe & Profesyonel)

| Kullanım | Renk | HEX |
|---|---|---|
| Ana Veri (Mavi) | Açık Mavi | #4472C4 |
| Başarı/Pozitif (Yeşil) | Koyu Yeşil | #70AD47 |
| Uyarı/İkincil | Turuncu | #FFC000 |
| Hata/Gecikme (Kırmızı) | Koyu Kırmızı | #C55A11 |
| Pasif/Arka Plan | Açık Gri | #E8E8E8 |
| Metin | Koyu Gri | #3F3F3F |

---

## İlişkiler (Filtering)

```
Takvim[Tarih] ←────────► Odenç_Hareketleri[Odenç_Tarihi]
                           │
                           ├──► Kitaplar[KitapID]
                           │      │
                           │      └──► Yazarlar[YazarID]
                           │
                           └──► Uyeler[UyeID]
```

**Filtre Yönü:** ÇİFT YÖNLÜ (Slicers ve görseller birbirini filtreleyebilsin)

---

## İnteraktif Özellikler

1. **Tarih Slicer:** Raporun tüm sayfalarını belirli dönem için filtrele
2. **Kategori Slicer:** Kitap kategorisine göre filtrele
3. **Drill-Through:** Gecikmiş İadeleler → Üye Geçmişi
4. **Vurgulama:** Tablolardaki satıra tıklanınca ilişkili görseller güncellensin
5. **Sürükle-Bırak:** Süzgeç ikonları için sağ klik filtresi

---

## Power BI Best Practices

✅ Tüm sayfa başlıkları kalın (18pt)
✅ KPI kartlar benzer boyutta hizalı
✅ Görsellerin arası 15-20px boşluk
✅ Tablo başlıkları koyu gri arka plan
✅ Veri etiketleri tam sayılar (virgülsüz)
✅ Türkçe tam adlar (kısaltma yok)
✅ Format: Para = 0.00 TL, Yüzde = 0.0%, Tarih = GG.AA.YYYY

