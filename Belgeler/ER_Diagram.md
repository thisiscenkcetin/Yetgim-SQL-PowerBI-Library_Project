# ER DİYAGRAMI - Varlık İlişki Modeli

## Tablo Yapıları ve İlişkileri

```
┌─────────────────────────────────────────────────────────────────┐
│                     YETGİM KUTUPHANE SISTEMИ                    │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │   YAZARLAR   │
                    ├──────────────┤
                    │ YazarID (PK) │
                    │ Ad_Soyad     │
                    │ Dogum_Tarihi │
                    │ Milliyet     │
                    │ Biyografi    │
                    │ Kitap_Sayisi │
                    └──────────────┘
                           ▲
                           │ 1:N
                           │
                    ┌──────────────┐
                    │   KITAPLAR   │
                    ├──────────────┤
                    │ KitapID (PK) │
                    │ ISBN (UNIQUE)│
                    │ Baslik       │
                    │ YazarID (FK) │─────► Yazarlar
                    │ Kategori     │
                    │ Basim_Tarihi │
                    │ Sayfa_Sayisi │
                    │ Stok_Miktari │
                    │ Odenç_Sayisi │
                    └──────────────┘
                           ▲
                           │ N:1
                           │
           ┌────────────────────────────────────────┐
           │    ÖDÜNÇ_HAREKETLERİ (JOIN TABLE)      │
           ├────────────────────────────────────────┤
           │ HareketID (PK)                         │
           │ KitapID (FK) ────────► Kitaplar        │
           │ UyeID (FK) ──────────┐                 │
           │ Odenç_Tarihi         │                 │
           │ Iade_Tarihi_Planlandi│                 │
           │ Iade_Tarihi_Gercek   │                 │
           │ Gun_Sayisi           │                 │
           │ Gecikmeli            │                 │
           │ Ceza_Tutari          │                 │
           │ Notlar               │                 │
           └────────────────────────────────────────┘
                                    │
                                    │ N:1
                                    ▼
                           ┌──────────────┐
                           │   ÜYELER     │
                           ├──────────────┤
                           │ UyeID (PK)   │
                           │ Ad_Soyad     │
                           │ TC_Kimlik    │
                           │ Email        │
                           │ Telefon      │
                           │ Adres        │
                           │ Uyelik_Tarihi│
                           │ Uyelik_Durus │
                           │ Ceza_Miktari │
                           └──────────────┘

                    ┌──────────────────┐
                    │   TAKVİM (Dim)   │
                    ├──────────────────┤
                    │ TarihID (PK)     │
                    │ Tarih (UNIQUE)   │
                    │ Yil              │
                    │ Ay / Ay_Adi      │
                    │ Gun              │
                    │ Haftanin_Gunu    │
                    │ Hafta_Numarasi   │
                    │ Ceyrek           │
                    └──────────────────┘
                           ▲
                           │ 1:N
                           │
         Ödünç_Tarihi ile bağlantı (Power BI'da)
```

## İlişki Özeti

| Kaynak Tablo | FK Sütun | Hedef Tablo | Tip | Açıklama |
|---|---|---|---|---|
| Kitaplar | YazarID | Yazarlar | N:1 | Her kitap bir yazara ait |
| Ödünç_Hareketleri | KitapID | Kitaplar | N:1 | Her ödünç işlemi bir kitab referans eder |
| Ödünç_Hareketleri | UyeID | Üyeler | N:1 | Her ödünç işlemi bir üyeyi referans eder |
| Ödünç_Hareketleri | Odenç_Tarihi | Takvim | N:1 | (Power BI) Tarih boyutu |

## İlişki Kısıtlamaları

- **Referential Integrity:** FK tabloları orijinal tablo silinmiş verileri tutamaz
- **Cascading Rules:** Yazarlar silinince (OPTIONAL) ilişkili kitapları nasıl işleyelim?
- **Null Values:** Üyeler.Telefon nullable, ama Kitaplar.Baslik NOT NULL

## Veri Akışı

```
1. Yazarlar sisteme kaydolur
2. Kitaplar yazarlarla eşleştirilir
3. Üyeler kütüphaneye kaydolur
4. Ödünç_Hareketleri: Üye + Kitap kombinasyonu
5. İade işlemi: Ödünç_Hareketleri güncellenir, Ceza hesaplanır
```
