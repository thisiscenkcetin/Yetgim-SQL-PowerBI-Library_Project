from datetime import datetime
from config.settings import ODENÇ_CEZASI_GUNLUK

class Utils:
    """Yardımcı fonksiyonlar"""
    
    @staticmethod
    def format_para(sayi):
        """Paranı Türkçe formatında göster"""
        return f"{sayi:,.2f} TL".replace(",", "X").replace(".", ",").replace("X", ".")
    
    @staticmethod
    def format_tarih(tarih):
        """Tarihi Türkçe formatında göster"""
        if isinstance(tarih, str):
            return tarih
        return tarih.strftime("%d.%m.%Y")
    
    @staticmethod
    def hesapla_ceza(gercek_iade_tarihi, planlanan_iade_tarihi):
        """Cezayı hesapla"""
        if not gercek_iade_tarihi or not planlanan_iade_tarihi:
            return 0
        
        fark = (gercek_iade_tarihi - planlanan_iade_tarihi).days
        if fark > 0:
            return fark * ODENÇ_CEZASI_GUNLUK
        return 0
    
    @staticmethod
    def hesapla_odenç_gunu(odenç_tarihi, iade_tarihi):
        """Ödünç gün sayısını hesapla"""
        if not odenç_tarihi or not iade_tarihi:
            return 0
        return (iade_tarihi - odenç_tarihi).days
    
    @staticmethod
    def durum_rengi(durum):
        """Duruma göre renk döndür"""
        durum_map = {
            "Aktif": "🟢",
            "Pasif": "🟡",
            "Askıda": "🔴",
            "GECİKMİŞ": "🔴",
            "ZAMANINDA": "🟢",
            "Stok Bitti": "🔴",
            "Az Stok": "🟡",
            "Yeterli Stok": "🟢"
        }
        return durum_map.get(durum, "⚪")
    
    @staticmethod
    def aktivite_seviyesi(odenç_sayisi):
        """Aktivite seviyesini belirle"""
        if odenç_sayisi > 20:
            return "🟢 Çok Aktif"
        elif odenç_sayisi > 5:
            return "🟡 Orta Aktif"
        elif odenç_sayisi > 0:
            return "🟡 Az Aktif"
        else:
            return "🔴 Pasif"
    
    @staticmethod
    def secim_listesi_olustur(veri, id_col, label_col):
        """Dropdown için seçim listesi oluştur"""
        if veri is None or len(veri) == 0:
            return {}, {}
        return {f"{row[label_col]}": row[id_col] for _, row in veri.iterrows()}, {row[id_col]: row[label_col] for _, row in veri.iterrows()}
