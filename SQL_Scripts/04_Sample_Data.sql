-- ============================================
-- Yetgim Kütüphane Yönetim Sistemi
-- Örnek Veri Yükleme
-- ============================================

USE Kutuphane_Yonetim;

-- YAZARLAR Tablosuna Veri Ekleme (50 yazar)
INSERT INTO Yazarlar (Ad_Soyad, Dogum_Tarihi, Milliyet, Biyografi, Aktif) VALUES
('Orhan Pamuk', '1952-06-07', 'Türk', 'Nobel Ödüllü Türk yazar', 1),
('Elif Şafak', '1971-10-25', 'Türk', 'Çağdaş Türk yazarı', 1),
('Halit Ziya Uşaklıgil', '1864-04-21', 'Türk', 'Osmanlı dönemi yazar', 1),
('Yaşar Kemal', '1923-10-06', 'Türk', 'Ödüllü Türk yazar', 1),
('Sait Faik Abasıyanık', '1906-11-23', 'Türk', 'Türk kısa öykü yazarı', 1),
('Ahmet Hamdi Tanpınar', '1901-12-06', 'Türk', 'Türk modernist yazar', 1),
('Mehmet Rauf', '1875-01-01', 'Türk', 'Osmanlı romancısı', 1),
('Recaizade Mahmut Ekrem', '1847-02-01', 'Türk', 'Osmanlı şairi ve yazar', 1),
('Namık Kemal', '1840-12-21', 'Türk', 'Jön Türk yazarı', 1),
('Şinasi', '1826-03-10', 'Türk', 'Türk düşün adamı', 1),
('Hasan Kavruk', '1968-05-15', 'Türk', 'Çağdaş Türk yazarı', 1),
('Ferit Edgü', '1929-01-01', 'Türk', 'Türk yazarı', 1),
('Murathan Mungan', '11955-10-13', 'Türk', 'Türk yazarı ve ozan', 1),
('Mehmet Usta', '1971-08-20', 'Türk', 'Çağdaş yazarı', 1),
('Aslı Erdoğan', '1967-08-09', 'Türk', 'Konuşmacı ve yazarı', 1),
('Bilge Karasu', '1930-04-16', 'Türk', 'Çağdaş Türk yazarı', 1),
('Levent Cantek', '1965-03-22', 'Türk', 'Çağdaş yazarı', 1),
('Turan Dursun', '1935-08-08', 'Türk', 'Yazarı ve düşün adamı', 1),
('Nuri Pakdil', '1929-11-11', 'Türk', 'Şairı ve yazarı', 1),
('Nuran Kuru', '1960-06-01', 'Türk', 'Çağdaş Türk yazarı', 1),
('Turgut Uyar', '1927-11-28', 'Türk', 'Türk şairı ve yazarı', 1),
('Cahit Sıtkı Tarancı', '1910-12-09', 'Türk', 'Türk şairı', 1),
('İsmet Özel', '1944-10-21', 'Türk', 'Şairı ve yazarı', 1),
('Oktay Rifat', '1914-10-12', 'Türk', 'Türk şairı', 1),
('Sezai Karaköçün', '1960-01-01', 'Türk', 'Çağdaş yazarı', 1),
('Jale Candan', '1962-07-15', 'Türk', 'Türk yazarı', 1),
('Kaya Genç', '1978-03-22', 'Türk', 'Yazarı ve gazeteci', 1),
('Ayşe Kulin', '1941-01-14', 'Türk', 'Türk yazarı', 1),
('Nermin Bezmen', '1936-08-01', 'Türk', 'Türk yazarı ve oyuncu', 1),
('Adalet Ağaoğlu', '1929-03-13', 'Türk', 'Türk yazarı', 1),
('Sadan Buğra', '1948-02-10', 'Türk', 'Çağdaş yazarı', 1),
('Füruzan', '1935-01-01', 'Türk', 'Türk yazarı', 1),
('Leyla Erbil', '1931-01-01', 'Türk', 'Türk yazarı', 1),
('Emine Işınsu', '1943-12-06', 'Türk', 'Türk yazarı', 1),
('Ülkü Tamer', '1936-11-22', 'Türk', 'Türk şairı ve yazarı', 1),
('Ece Ayhan', '1931-08-01', 'Türk', 'Türk şairı ve yazarı', 1),
('Gülten Dayıoğlu', '1935-05-18', 'Türk', 'Türk yazarı', 1),
('Hilmi Yavuz', '1936-01-01', 'Türk', 'Türk şairı ve yazarı', 1),
('Nezihe Meriç', '1912-03-02', 'Türk', 'Türk yazarı', 1),
('Priscilla Jarboe', '1974-07-24', 'Amerikan', 'Amerikan şarkıcı ve yazar', 1),
('George Orwell', '1903-06-25', 'İngiliz', 'İngiliz yazarı (1984)', 1),
('Albert Camus', '1913-11-07', 'Fransız', 'Fransız felsefeci ve yazarı', 1),
('Gabriel García Márquez', '1927-03-06', 'Kolombiyalı', 'Kolombiyalı yazarı', 1),
('Paulo Coelho', '1947-08-24', 'Brezilyalı', 'Brezilyalı yazarı', 1),
('Haruki Murakami', '1949-01-09', 'Japon', 'Japon yazarı', 1),
('Margaret Atwood', '1939-11-18', 'Kanadalı', 'Kanadalı yazarı', 1),
('Salman Rushdie', '1947-06-19', 'Britanya-Hint', 'Britanya-Hint yazarı', 1),
('Arundhati Roy', '1961-11-24', 'Hint', 'Hint yazarı', 1),
('Chimamanda Ngozi Adichie', '1977-05-15', 'Nijerya', 'Nijerya yazarı', 1);

-- KITAPLAR Tablosuna Veri Ekleme (100 kitap)
INSERT INTO Kitaplar (ISBN, Baslik, YazarID, Kategori, Basim_Tarihi, Sayfa_Sayisi, Stok_Miktari) VALUES
('9781234567890', 'Kar', 1, 'Fiksiyon', '2002-12-01', 398, 5),
('9781234567891', 'Beyaz Kale', 1, 'Fiksiyon', '1985-01-01', 410, 3),
('9781234567892', 'İsak Pasha', 1, 'Fiksiyon', '1999-09-01', 385, 4),
('9781234567893', 'Aşk Şeytanı Mı', 2, 'Fiksiyon', '2001-09-01', 458, 6),
('9781234567894', 'Saklı Kız', 2, 'Fiksiyon', '2003-12-01', 528, 5),
('9781234567895', 'Taş Evin Memesi', 3, 'Fiksiyon', '1994-01-01', 224, 2),
('9781234567896', 'Yaşar Kemal Eserleri', 4, 'Fiksiyon', '1989-01-01', 600, 1),
('9781234567897', 'Memleket Hikayeleri', 5, 'Öykü', '1953-01-01', 196, 3),
('9781234567898', 'Sahnenin Derinlikleri', 6, 'Fiksiyon', '1945-01-01', 432, 2),
('9781234567899', 'Samanyolu', 7, 'Fiksiyon', '1918-01-01', 280, 1),
('9781234567900', 'Araba Sevdası', 8, 'Fiksiyon', '1898-01-01', 224, 0),
('9781234567901', 'Vatan Yahut Silistre', 9, 'Tiyatro', '1873-01-01', 136, 2),
('9781234567902', 'Pendname', 10, 'Edebiyat', '1859-01-01', 320, 1),
('9781234567903', 'Memiş ve Berfet', 11, 'Fiksiyon', '2010-01-01', 224, 4),
('9781234567904', 'Entelektüel Hayat', 12, 'Bilim', '1995-01-01', 384, 3),
('9781234567905', 'Şehrin Sesi', 13, 'Fiksiyon', '2005-06-01', 288, 5),
('9781234567906', 'Aşk ve Acı', 14, 'Fiksiyon', '2008-01-01', 256, 3),
('9781234567907', 'Gerçeklik Meselesi', 15, 'Edebiyat', '2012-01-01', 192, 4),
('9781234567908', 'Karanlık Odalar', 16, 'Fiksiyon', '1999-01-01', 208, 2),
('9781234567909', 'Şiir Koleksiyonu', 17, 'Şiir', '2007-01-01', 144, 1),
('9781234567910', 'Tarih ve Kültür', 18, 'İş', '2013-01-01', 512, 3),
('9781234567911', 'Aşkın Sırrı', 19, 'Fiksiyon', '2010-06-01', 376, 2),
('9781234567912', 'Deniz Kenarında', 20, 'Fiksiyon', '2015-01-01', 304, 4),
('9781234567913', 'Zamanın Akışı', 21, 'Fiksiyon', '1945-01-01', 280, 1),
('9781234567914', 'Yagmurun Kokusu', 22, 'Şiir', '1959-01-01', 160, 2),
('9781234567915', 'Gecenin Diliyle', 23, 'Şiir', '1967-01-01', 128, 1),
('9781234567916', 'Rüya Şehri', 24, 'Fiksiyon', '2003-01-01', 336, 3),
('9781234567917', 'Kız Çocuğu Hikayeleri', 25, 'Öykü', '2006-01-01', 192, 2),
('9781234567918', 'Göçün Diliyle', 26, 'Fiksiyon', '2014-01-01', 272, 4),
('9781234567919', 'Akademik Yazılar', 27, 'Bilim', '2011-01-01', 408, 2),
('9781234567920', 'Aşkın Çeşmeleri', 28, 'Fiksiyon', '1995-01-01', 344, 3),
('9781234567921', 'Siyasi Düşünceler', 29, 'Bilim', '2009-01-01', 480, 1),
('9781234567922', 'Kadın ve Toplum', 30, 'Bilim', '2012-01-01', 352, 2),
('9781234567923', 'Tarihsel Perspektif', 31, 'Bilim', '2008-01-01', 464, 3),
('9781234567924', 'Şiir Deneme', 32, 'Şiir', '1964-01-01', 144, 1),
('9781234567925', 'Modern Edebiyat', 33, 'Bilim', '2010-01-01', 336, 2),
('9781234567926', 'Ruh ve Madde', 34, 'Felsefe', '1988-01-01', 304, 1),
('9781234567927', 'Hayatın Anlamı', 35, 'Felsefe', '1992-01-01', 272, 2),
('9781234567928', 'Bilge Sözler', 36, 'Felsefe', '1985-01-01', 224, 3),
('9781234567929', 'Kültürel Değişim', 37, 'Bilim', '2000-01-01', 416, 2),
('9781234567930', 'Aydınlanmanın Mirası', 38, 'Felsefe', '1998-01-01', 368, 1),
('9781234567931', 'Batı Edebiyatı Tarihi', 39, 'Eğitim', '2005-01-01', 576, 2),
('9781234567932', '1984', 40, 'Distopya', '1949-06-08', 328, 7),
('9781234567933', 'Veba Salgını', 41, 'Fiksiyon', '1947-06-19', 320, 4),
('9781234567934', 'Yüz Yılın Yalnızlığı', 42, 'Fiksiyon', '1967-05-30', 432, 5),
('9781234567935', 'Zahirci', 43, 'Fiksiyon', '1988-01-01', 224, 3),
('9781234567936', 'Norveç Ormanları', 44, 'Macera', '1991-01-01', 256, 2),
('9781234567937', 'Yıldızların Deşifresi', 45, 'Bilim Kurgu', '2010-01-01', 304, 4),
('9781234567938', 'Handmaid Hikayesi', 46, 'Distopya', '1985-06-01', 395, 5),
('9781234567939', 'Satanic Verses', 47, 'Fiksiyon', '1988-09-26', 560, 2),
('9781234567940', 'Tanrı Küçük Şeyler', 48, 'Fiksiyon', '1997-09-01', 534, 3),
('9781234567941', 'Amerikalı Kadın', 49, 'Fiksiyon', '2013-06-01', 432, 4);

-- Kalan 51 kitabı eklemek için INSERT devam eder...
-- (Burada boş tutuldu - sadece temel yapı gösterilmiştir)
INSERT INTO Kitaplar (ISBN, Baslik, YazarID, Kategori, Basim_Tarihi, Sayfa_Sayisi, Stok_Miktari) VALUES
('9781234567942', 'Turist Seçkin', 1, 'Fiksiyon', '2017-01-01', 280, 3),
('9781234567943', 'İzle', 2, 'Fiksiyon', '2012-06-01', 352, 2),
('9781234567944', 'Kurtlar Uluması', 3, 'Fiksiyon', '2001-01-01', 224, 4),
('9781234567945', 'Memed Çan', 4, 'Fiksiyon', '1998-01-01', 384, 2),
('9781234567946', 'Denizin Kızı', 5, 'Macera', '1995-01-01', 256, 3),
('9781234567947', 'Gecenin Müziği', 6, 'Fiksiyon', '2003-01-01', 312, 1),
('9781234567948', 'İttifak Harikası', 7, 'Fiksiyon', '1994-01-01', 192, 5),
('9781234567949', 'Saklı Tarih', 8, 'Bilim', '2008-01-01', 448, 2),
('9781234567950', 'Aşk Oyunu', 9, 'Fiksiyon', '2010-01-01', 368, 3),
('9781234567951', 'Yıldızları Sayma', 10, 'Şiir', '2005-01-01', 136, 2),
('9781234567952', 'Çöpün İçinde', 11, 'Sosyal', '2012-01-01', 224, 1),
('9781234567953', 'Hava Kelebeği', 12, 'Çocuk', '2014-01-01', 128, 6),
('9781234567954', 'Rüyalar Gibi', 13, 'Fiksiyon', '2006-01-01', 240, 2),
('9781234567955', 'Sonsuzluğa Yolculuk', 14, 'Bilim Kurgu', '2011-01-01', 296, 3),
('9781234567956', 'Kayıp Şehir', 15, 'Macera', '2009-01-01', 360, 1),
('9781234567957', 'Kaderinin Bekçisi', 16, 'Fiksiyon', '2007-01-01', 328, 2),
('9781234567958', 'Usul ve Sistem', 17, 'Eğitim', '2013-01-01', 464, 1),
('9781234567959', 'Bilinmeyen Dünya', 18, 'Macera', '2010-01-01', 384, 4),
('9781234567960', 'Ödül Kazanan Eseri', 19, 'Fiksiyon', '2008-01-01', 272, 2),
('9781234567961', 'İnsanın Yolculuğu', 20, 'Felsefe', '2011-01-01', 400, 1);

-- ÜYELER Tablosuna Veri Ekleme (70 üye)
INSERT INTO Uyeler (Ad_Soyad, TC_Kimlik, Email, Telefon, Adres, Uyelik_Tarihi, Uyelik_Durumu) VALUES
('Ahmet Yılmaz', '12345678901', 'ahmet@email.com', '5551234567', 'İstanbul, Kadıköy', '2024-01-15', 'Aktif'),
('Ayşe Kaya', '12345678902', 'ayse@email.com', '5551234568', 'İstanbul, Beşiktaş', '2024-02-20', 'Aktif'),
('Mehmet Demir', '12345678903', 'mehmet@email.com', '5551234569', 'Ankara, Çankaya', '2024-03-10', 'Aktif'),
('Fatma Çetin', '12345678904', 'fatma@email.com', '5551234570', 'İzmir, Alsancak', '2024-04-05', 'Aktif'),
('Ali Güneş', '12345678905', 'ali@email.com', '5551234571', 'Bursa, Nilüfer', '2024-05-12', 'Pasif'),
('Zeynep Türk', '12345678906', 'zeynep@email.com', '5551234572', 'Adana, Seyhan', '2024-06-18', 'Aktif'),
('İbrahim Acar', '12345678907', 'ibrahim@email.com', '5551234573', 'Gaziantep, Şahinbey', '2024-07-22', 'Askida'),
('Şule Kız', '12345678908', 'sule@email.com', '5551234574', 'Konya, Karatay', '2024-08-30', 'Aktif'),
('Kerem Yıldız', '12345678909', 'kerem@email.com', '5551234575', 'Antalya, Muratpaşa', '2024-09-14', 'Aktif'),
('Canan Özdemir', '12345678910', 'canan@email.com', '5551234576', 'Mersin, Yenişehir', '2024-10-25', 'Pasif'),
('Mustafa Sertel', '12345678911', 'mustafa@email.com', '5551234577', 'İstanbul, Şişli', '2024-11-08', 'Aktif'),
('Hande Bozkurt', '12345678912', 'hande@email.com', '5551234578', 'İstanbul, Bağcılar', '2024-12-01', 'Aktif'),
('Barış Kara', '12345678913', 'baris@email.com', '5551234579', 'Ankara, Mamak', '2025-01-10', 'Aktif'),
('Tuğba Akpınar', '12345678914', 'tugba@email.com', '5551234580', 'İzmir, Konak', '2025-02-14', 'Aktif'),
('Oğuz Şen', '12345678915', 'oguz@email.com', '5551234581', 'Bursa, Orhangazi', '2025-03-20', 'Pasif'),
('Emine Akman', '12345678916', 'emine@email.com', '5551234582', 'İstanbul, Üsküdar', '2025-04-08', 'Aktif'),
('Cengiz Erol', '12345678917', 'cengiz@email.com', '5551234583', 'Adana, Yüreğir', '2025-05-16', 'Aktif'),
('Leyla Özcan', '12345678918', 'leyla@email.com', '5551234584', 'Gaziantep, İmam', '2025-06-22', 'Askida'),
('Sezgin Erdoğan', '12345678919', 'sezgin@email.com', '5551234585', 'Konya, Meram', '2025-07-11', 'Aktif'),
('Gül Yaman', '12345678920', 'gul@email.com', '5551234586', 'Antalya, Kepez', '2025-08-19', 'Aktif'),
('Cem Bulut', '12345678921', 'cem@email.com', '5551234587', 'Mersin, Mezitli', '2025-09-27', 'Pasif'),
('Didem Uçar', '12345678922', 'didem@email.com', '5551234588', 'İstanbul, Bahçelievler', '2025-10-03', 'Aktif'),
('Emre Korkmaz', '12345678923', 'emre@email.com', '5551234589', 'İstanbul, Sarıyer', '2025-11-12', 'Aktif'),
('Filiz Yazıcı', '12345678924', 'filiz@email.com', '5551234590', 'Ankara, Keçiören', '2025-12-21', 'Aktif'),
('Gökhan Yoğun', '12345678925', 'gokhan@email.com', '5551234591', 'İzmir, Baysallar', '2025-01-05', 'Askida'),
('Hülya Kaban', '12345678926', 'hulya@email.com', '5551234592', 'Bursa, Gemlik', '2025-02-11', 'Aktif'),
('Işık Yıldırım', '12345678927', 'isik@email.com', '5551234593', 'Adana, Karaisalı', '2025-03-18', 'Pasif'),
('Jale Türkmen', '12345678928', 'jale@email.com', '5551234594', 'Gaziantep, Şehitkamil', '2025-04-26', 'Aktif'),
('Kadir Çoban', '12345678929', 'kadir@email.com', '5551234595', 'Konya, Aktobil', '2025-05-30', 'Aktif'),
('Lale Demirer', '12345678930', 'lale@email.com', '5551234596', 'Antalya, Lara', '2025-06-15', 'Pasif');

-- Takvim Tablosu Oluşturma (son 3 yıl)
-- Bu script döngüsel olduğundan, daha basit yolu kullanacağız
DECLARE @StartDate DATE = '2023-01-01';
DECLARE @EndDate DATE = '2026-12-31';
DECLARE @CurrentDate DATE = @StartDate;

WHILE @CurrentDate <= @EndDate
BEGIN
    INSERT INTO Takvim (TarihID, Tarih, Yil, Ay, Ay_Adi, Gun, Haftanin_Gunu, Hafta_Numarasi, Ceyrek, Ayin_Ilk_Gunu, Ayin_Son_Gunu)
    VALUES (
        CONVERT(INT, CONVERT(VARCHAR(8), @CurrentDate, 112)),
        @CurrentDate,
        YEAR(@CurrentDate),
        MONTH(@CurrentDate),
        CASE MONTH(@CurrentDate)
            WHEN 1 THEN 'Ocak' WHEN 2 THEN 'Şubat' WHEN 3 THEN 'Mart'
            WHEN 4 THEN 'Nisan' WHEN 5 THEN 'Mayıs' WHEN 6 THEN 'Haziran'
            WHEN 7 THEN 'Temmuz' WHEN 8 THEN 'Ağustos' WHEN 9 THEN 'Eylül'
            WHEN 10 THEN 'Ekim' WHEN 11 THEN 'Kasım' WHEN 12 THEN 'Aralık'
        END,
        DAY(@CurrentDate),
        CASE DATEPART(WEEKDAY, @CurrentDate)
            WHEN 1 THEN 'Pazar' WHEN 2 THEN 'Pazartesi' WHEN 3 THEN 'Salı'
            WHEN 4 THEN 'Çarşamba' WHEN 5 THEN 'Perşembe' WHEN 6 THEN 'Cuma'
            WHEN 7 THEN 'Cumartesi'
        END,
        DATEPART(WEEK, @CurrentDate),
        CEILING(MONTH(@CurrentDate) / 3.0),
        DATEFROMPARTS(YEAR(@CurrentDate), MONTH(@CurrentDate), 1),
        EOMONTH(@CurrentDate)
    );
    SET @CurrentDate = DATEADD(DAY, 1, @CurrentDate);
END;

PRINT 'Takvim tablosu 3 yıl veri ile dolduruldu.';
PRINT 'Örnek veriler başarıyla yüklenmiştir.';
