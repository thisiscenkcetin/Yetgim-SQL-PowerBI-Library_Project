import pyodbc
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Loglama seviyesini CRITICAL olarak ayarla - connection errors gösterilmeyecek
logger.setLevel(logging.CRITICAL)

class DatabaseHandler:
    """SQL Server veritabanı işlemleri"""
    
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        # Windows Authentication kullan
        self.connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"Trusted_Connection=yes"
        )
        self.conn = None
    
    def connect(self):
        """Veritabanına bağlan"""
        try:
            self.conn = pyodbc.connect(self.connection_string)
            logger.info("✅ Veritabanı bağlantısı başarılı")
            return True
        except Exception as e:
            # Sessiz başarısızlık - logger.error çağırma, doğrudan False dön
            return False
    
    def execute_query(self, query, params=None):
        """SQL sorgusu çalıştır ve sonuç döndür - pyodbc cursor ile"""
        try:
            if self.conn is None:
                self.connect()
            
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Sütun isimlerini al
            columns = [column[0] for column in cursor.description]
            
            # Verileri al
            rows = cursor.fetchall()
            
            # DataFrame oluştur
            data = [dict(zip(columns, row)) for row in rows]
            df = pd.DataFrame(data)
            
            cursor.close()
            return df
        except Exception as e:
            logger.error(f"❌ Sorgu hatası: {str(e)}")
            return None
    
    # ========== ÜYE İŞLEMLERİ ==========
    def get_uyeler(self, durum_filtresi=None):
        """Üyeleri al"""
        query = """
        SELECT UyeID, Ad_Soyad, TC_Kimlik, Email, Telefon, Adres, 
               Uyelik_Tarihi, Uyelik_Durumu, Ceza_Miktari
        FROM Uyeler
        """
        if durum_filtresi:
            query += f" WHERE Uyelik_Durumu = '{durum_filtresi}'"
        query += " ORDER BY Ad_Soyad"
        return self.execute_query(query)
    
    def get_uye_by_id(self, uye_id):
        """ID'ye göre üye al"""
        query = f"SELECT * FROM Uyeler WHERE UyeID = {uye_id}"
        result = self.execute_query(query)
        return result.iloc[0].to_dict() if result is not None and len(result) > 0 else None
    
    def uye_kaydet(self, ad_soyad, tc_kimlik, email, telefon, adres):
        """Yeni üye kayıt"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Uyeler (Ad_Soyad, TC_Kimlik, Email, Telefon, Adres, Uyelik_Tarihi)
                VALUES (?, ?, ?, ?, ?, CAST(GETDATE() AS DATE))
            """, ad_soyad, tc_kimlik, email, telefon, adres)
            self.conn.commit()
            logger.info(f"✅ Üye kaydı başarılı: {ad_soyad}")
            return True, "Üye başarıyla kaydedildi."
        except Exception as e:
            self.conn.rollback()
            logger.error(f"❌ Üye kayıt hatası: {str(e)}")
            return False, str(e)
    
    def tc_benzersiz_mi(self, tc_kimlik):
        """TC Kimlik benzersizliğini kontrol et"""
        result = self.execute_query(f"SELECT COUNT(*) as cnt FROM Uyeler WHERE TC_Kimlik = '{tc_kimlik}'")
        return result.iloc[0]["cnt"] == 0 if result is not None else True
    
    def uye_guncelle(self, uye_id, **kwargs):
        """Üye bilgilerini güncelle"""
        try:
            cursor = self.conn.cursor()
            fields = []
            values = []
            for key, val in kwargs.items():
                fields.append(f"{key} = ?")
                values.append(val)
            
            values.append(uye_id)
            query = f"UPDATE Uyeler SET {', '.join(fields)} WHERE UyeID = ?"
            cursor.execute(query, values)
            self.conn.commit()
            logger.info(f"✅ Üye güncellendi: {uye_id}")
            return True, "Üye başarıyla güncellendi."
        except Exception as e:
            self.conn.rollback()
            return False, str(e)
    
    # ========== KİTAP İŞLEMLERİ ==========
    def get_kitaplar(self, stok_filtresi=False):
        """Kitapları al"""
        query = """
        SELECT k.KitapID, k.ISBN, k.Baslik, y.Ad_Soyad AS Yazar, 
               k.Kategori, k.Stok_Miktari, k.Odenç_Sayisi
        FROM Kitaplar k
        LEFT JOIN Yazarlar y ON k.YazarID = y.YazarID
        """
        if stok_filtresi:
            query += " WHERE k.Stok_Miktari > 0"
        query += " ORDER BY k.Baslik"
        return self.execute_query(query)
    
    def kitap_ekle(self, isbn, baslik, yazar_id, kategori, basim_tarihi, sayfa_sayisi, stok_miktari=1):
        """Yeni kitap ekle"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Kitaplar (ISBN, Baslik, YazarID, Kategori, Basim_Tarihi, Sayfa_Sayisi, Stok_Miktari)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, str(isbn), str(baslik), int(yazar_id), str(kategori), basim_tarihi, int(sayfa_sayisi), int(stok_miktari))
            self.conn.commit()
            logger.info(f"✅ Kitap eklendi: {baslik}")
            return True, "Kitap başarıyla eklendi."
        except Exception as e:
            self.conn.rollback()
            logger.error(f"❌ Kitap ekleme hatası: {str(e)}")
            return False, str(e)
    
    def isbn_benzersiz_mi(self, isbn):
        """ISBN benzersizliğini kontrol et"""
        result = self.execute_query(f"SELECT COUNT(*) as cnt FROM Kitaplar WHERE ISBN = '{isbn}'")
        return result.iloc[0]["cnt"] == 0 if result is not None else True
    
    # ========== YAZAR İŞLEMLERİ ==========
    def get_yazarlar(self):
        """Yazarları al"""
        query = "SELECT YazarID, Ad_Soyad FROM Yazarlar WHERE Aktif = 1 ORDER BY Ad_Soyad"
        return self.execute_query(query)
    
    def yazar_ekle(self, ad_soyad, dogum_tarihi=None, milliyet=None):
        """Yeni yazar ekle"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Yazarlar (Ad_Soyad, Dogum_Tarihi, Milliyet, Aktif)
                VALUES (?, ?, ?, 1)
            """, ad_soyad, dogum_tarihi, milliyet)
            self.conn.commit()
            logger.info(f"✅ Yazar eklendi: {ad_soyad}")
            return True, "Yazar başarıyla eklendi."
        except Exception as e:
            self.conn.rollback()
            return False, str(e)
    
    # ========== ÖDÜNÇ İŞLEMLERİ ==========
    def yeni_odenç(self, kitap_id, uye_id, odenç_tarihi, iade_tarihi, notlar=None):
        """Yeni ödünç hareketini kaydet (SP çağır)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                EXEC sp_Yeni_Odenç_Kaydet 
                @KitapID=?, @UyeID=?, @Odenç_Tarihi=?, 
                @Iade_Tarihi_Planlandi=?, @Notlar=?
            """, kitap_id, uye_id, odenç_tarihi, iade_tarihi, notlar)
            self.conn.commit()
            logger.info(f"✅ Ödünç kaydedildi: Kitap {kitap_id}, Üye {uye_id}")
            return True, "Ödünç hareketi başarıyla kaydedildi."
        except Exception as e:
            self.conn.rollback()
            logger.error(f"❌ Ödünç hatası: {str(e)}")
            return False, str(e)
    
    def get_aktif_odencs(self, uye_id=None):
        """İade edilmemiş ödünçleri al"""
        query = "SELECT * FROM vw_Aktif_Odenç"
        if uye_id:
            query += f" WHERE UyeID = {uye_id}"
        return self.execute_query(query)
    
    def iade_işlemi(self, hareket_id, iade_tarihi_gercek):
        """İade işlemini tamamla (SP çağır)"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                EXEC sp_Iade_Işlemi_Tamamla 
                @HareketID=?, @Iade_Tarihi_Gercek=?
            """, hareket_id, iade_tarihi_gercek)
            self.conn.commit()
            logger.info(f"✅ İade işlemi tamamlandı: Hareket {hareket_id}")
            return True, "İade işlemi başarıyla tamamlandı."
        except Exception as e:
            self.conn.rollback()
            logger.error(f"❌ İade hatası: {str(e)}")
            return False, str(e)
    
    # ========== RAPORLAR ==========
    def get_popurite_raporlari(self, limit=10):
        """En popüler kitapları al"""
        query = f"SELECT TOP {limit} * FROM vw_Kitap_Popülarite"
        return self.execute_query(query)
    
    def get_gecikmiş_iadeleler(self):
        """Gecikmiş iadeleri al"""
        return self.execute_query("SELECT * FROM vw_Gecikmiş_Iadeleler")
    
    def get_uye_istatistikleri(self, limit=10):
        """Üye istatistiklerini al"""
        query = f"SELECT TOP {limit} * FROM vw_Uye_İstatistikleri ORDER BY Toplam_Odenç_Sayisi DESC"
        return self.execute_query(query)
    
    def get_aylik_trend(self):
        """Aylık trend verilerini al"""
        return self.execute_query("SELECT * FROM vw_Aylik_Odenç_Trendi ORDER BY Yil DESC, Ay DESC")
    
    def get_dashboard_ozet(self):
        """Dashboard için özet istatistikleri"""
        try:
            result = self.execute_query("SELECT COUNT(*) as cnt FROM Kitaplar WHERE Aktif=1")
            toplam_kitap = result.iloc[0]["cnt"] if result is not None and not result.empty else 0
            
            result = self.execute_query("SELECT COUNT(*) as cnt FROM Uyeler WHERE Uyelik_Durumu='Aktif'")
            aktif_uye = result.iloc[0]["cnt"] if result is not None and not result.empty else 0
            
            result = self.execute_query("SELECT COUNT(*) as cnt FROM Odenç_Hareketleri WHERE Iade_Tarihi_Gercek IS NULL")
            aktif_odenç = result.iloc[0]["cnt"] if result is not None and not result.empty else 0
            
            result = self.execute_query("""
                SELECT COUNT(*) as cnt FROM Odenç_Hareketleri 
                WHERE Iade_Tarihi_Gercek IS NULL 
                AND CAST(GETDATE() AS DATE) > Iade_Tarihi_Planlandi
            """)
            gecikmiş_odenç = result.iloc[0]["cnt"] if result is not None and not result.empty else 0
            
            stats = {
                "toplam_kitap": toplam_kitap,
                "aktif_uye": aktif_uye,
                "aktif_odenç": aktif_odenç,
                "gecikmiş_odenç": gecikmiş_odenç
            }
            return stats
        except Exception as e:
            logger.error(f"Dashboard özet hatası: {str(e)}")
            return {
                "toplam_kitap": 0,
                "aktif_uye": 0,
                "aktif_odenç": 0,
                "gecikmiş_odenç": 0
            }
