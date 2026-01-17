# Veritabanı Bağlantı Ayarları

import streamlit as st
from modules.database_handler import DatabaseHandler
import logging

# Loglama seviyesini azalt
logging.getLogger('pyodbc').setLevel(logging.CRITICAL)
logging.getLogger().setLevel(logging.CRITICAL)

def get_db_connection():
    """Veritabanı bağlantısını al veya oluştur"""
    if "db_connection" not in st.session_state:
        try:
            # Streamlit secrets'tan bilgileri oku
            server = st.secrets["database"]["server"]
            database = st.secrets["database"]["database"]
            username = st.secrets["database"]["username"]
            password = st.secrets["database"]["password"]
            
            # Bağlantı oluştur (sessiz modu aktif)
            db = DatabaseHandler(server, database, username, password)
            if db.connect():
                st.session_state.db_connection = db
                return db
            else:
                # Sessiz başarısız - demo modunda çalışacak
                st.session_state.db_connection = None
                return None
        except Exception as e:
            # Sessiz başarısız - demo modunda çalışacak
            st.session_state.db_connection = None
            return None
    return st.session_state.db_connection

def test_connection():
    """Bağlantıyı test et"""
    db = get_db_connection()
    if db:
        try:
            result = db.execute_query("SELECT COUNT(*) FROM Kitaplar")
            return True, "✅ Bağlantı başarılı!"
        except Exception as e:
            return False, f"❌ Test hatası: {str(e)}"
    return False, "❌ Bağlantı kurulamadı!"
