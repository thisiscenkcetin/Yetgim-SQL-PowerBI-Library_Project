# 📚 Kütüphane Yönetim Sistemi

SQL Server + Power BI + Streamlit ile geliştirilmiş kapsamlı kütüphane yönetim sistemi.

## 🎯 Proje Özeti

| Bileşen | Açıklama |
|---------|----------|
| **SQL Server** | Veritabanı tasarımı, tablolar, ilişkiler, stored procedures |
| **Power BI** | İnteraktif dashboard ve raporlar |
| **Streamlit** | Web tabanlı yönetim arayüzü |


## Demo 

![Demo 0](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/0.png?raw=true)

![Demo 1](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/1.png?raw=true)

![Demo 2](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/2.png?raw=true)

![Demo 3](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/3.png?raw=true)

![Demo 4](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/4.png?raw=true)

![Demo 5](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/5.png?raw=true)

![Demo 6](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/7.png?raw=true)

![Demo 7](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/7.png?raw=true)

![Demo 8](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/8.png?raw=true)

![Demo 9](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/9.png?raw=true)

![Demo 10](https://github.com/thisiscenkcetin/Yetgim-SQL-PowerBI-Library_Project/blob/main/Demo/10.png?raw=true)


## 📁 Klasör Yapısı

```
├── SQL_Scripts/     # Veritabanı scriptleri (01-07)
├── PowerBI/         # Power BI rapor dosyaları
├── Streamlit/       # Web arayüzü
├── Belgeler/        # Proje dokümantasyonu
└── Veriler/         # Örnek veri dosyaları
```

## 🚀 Hızlı Başlangıç

### 1. Veritabanı Kurulumu
```sql
-- SQL_Scripts klasöründeki scriptleri sırayla çalıştırın:
-- 01_Create_Database.sql
-- 02_Create_Tables.sql
-- 03_Relationships.sql
-- 04_Sample_Data.sql
-- 05_Stored_Procedures.sql
-- 06_Views.sql
-- 07_Advanced_Queries.sql
```

### 2. Streamlit Arayüzü
```bash
cd Streamlit
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port=8080
```

**Giriş Bilgileri:** `kutuphane` / `123456`

### 3. Power BI
`PowerBI/` klasöründeki `.pbix` dosyasını açın.

## ✅ Tamamlanan Gereksinimler

### SQL Server
- [x] Veritabanı oluşturma (Kutuphane_Yonetim)
- [x] 5 ana tablo (Yazarlar, Kitaplar, Uyeler, Odunc_Hareketleri, Takvim)
- [x] Primary/Foreign key ilişkileri
- [x] Stored Procedures ve Views
- [x] Örnek veriler (49 yazar, 50 kitap, 70 üye)

### Power BI
- [x] SQL Server bağlantısı
- [x] Veri modeli ve ilişkiler
- [x] İnteraktif dashboard
- [x] Filtreleme ve drill-down

### Streamlit
- [x] SQL Server canlı bağlantı (pyodbc)
- [x] Dashboard özet istatistikleri
- [x] Kitap/Üye/Yazar CRUD işlemleri
- [x] Ödünç alma/iade sistemi
- [x] Raporlar ve grafikler

## 🔧 Teknik Detaylar

- **Python:** 3.13
- **Veritabanı:** SQL Server (Windows Authentication)
- **Bağlantı:** pyodbc (SQLAlchemy Python 3.13 uyumsuzluğu nedeniyle)

## İletişim

Cenk ÇETİN 
dev.cenkcetin@gmail.com
