import re
from datetime import datetime

class DataValidator:
    """Veri doğrulama"""
    
    @staticmethod
    def validate_tc_kimlik(tc):
        """TC Kimlik doğrulaması"""
        if not tc:
            return False, "TC Kimlik boş olamaz"
        if len(tc) != 11:
            return False, "TC Kimlik 11 karakter olmalı"
        if not tc.isdigit():
            return False, "TC Kimlik sadece rakamlardan oluşmalı"
        if tc[0] == '0':
            return False, "TC Kimlik 0 ile başlayamaz"
        return True, "Geçerli"
    
    @staticmethod
    def validate_email(email):
        """Email doğrulaması"""
        if not email:
            return True, "Geçerli"  # Optional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, "Geçerli"
        return False, "Geçersiz email formatı"
    
    @staticmethod
    def validate_isbn(isbn):
        """ISBN doğrulaması"""
        if not isbn:
            return False, "ISBN boş olamaz"
        isbn_clean = isbn.replace("-", "").replace(" ", "")
        if len(isbn_clean) not in [10, 13]:
            return False, "ISBN 10 veya 13 haneli olmalı"
        if not isbn_clean.isdigit():
            return False, "ISBN sadece rakamlardan oluşmalı"
        return True, "Geçerli"
    
    @staticmethod
    def validate_telefon(telefon):
        """Telefon doğrulaması"""
        if not telefon:
            return True, "Geçerli"  # Optional
        telefon_clean = telefon.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if len(telefon_clean) < 10:
            return False, "Telefon 10+ rakam olmalı"
        if not telefon_clean.isdigit():
            return False, "Telefon sadece rakamlardan oluşmalı"
        return True, "Geçerli"
    
    @staticmethod
    def validate_baslik(baslik):
        """Kitap başlığı doğrulaması"""
        if not baslik or len(baslik.strip()) < 3:
            return False, "Başlık en az 3 karakter olmalı"
        return True, "Geçerli"
    
    @staticmethod
    def validate_tarih_araligi(basla, bitis):
        """Tarih aralığı doğrulaması"""
        if basla > bitis:
            return False, "Başlangıç tarihi bitiş tarihinden önce olmalı"
        return True, "Geçerli"
    
    @staticmethod
    def validate_pozitif_sayi(sayi):
        """Pozitif sayı doğrulaması"""
        try:
            if float(sayi) < 0:
                return False, "Sayı pozitif olmalı"
            return True, "Geçerli"
        except:
            return False, "Geçersiz sayı"
    
    @staticmethod
    def validate_ad_soyad(ad_soyad):
        """Ad-soyad doğrulaması"""
        if not ad_soyad or len(ad_soyad.strip()) < 3:
            return False, "Ad-soyad en az 3 karakter olmalı"
        if any(char.isdigit() for char in ad_soyad):
            return False, "Ad-soyad rakam içeremez"
        return True, "Geçerli"
