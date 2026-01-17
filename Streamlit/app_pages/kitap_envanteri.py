import streamlit as st
from config.database import get_db_connection
from modules.validators import DataValidator
from config.settings import KITAP_KATEGORILERI
from datetime import datetime

def show():
    """Kitap Envanteri Sayfası"""
    st.header("📚 Kitap Envanteri")
    
    db = get_db_connection()
    
    if not db:
        show_demo_kitap_envanteri()
        return
    
    tab1, tab2 = st.tabs(["➕ Yeni Kitap Ekle", "📊 Stok Yönetimi"])
    
    # ===== SEKME 1: YENİ KİTAP EKLE =====
    with tab1:
        st.subheader("Yeni Kitap Ekle")
        
        if not db:
            st.info("💡 Kitap ekleme özelliği veritabanı bağlantısı gerektirir")
        else:
            with st.form("kitap_form", border=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    isbn = st.text_input("ISBN", placeholder="Örn: 9789876543210")
                    baslik = st.text_input("📖 Kitap Başlığı", placeholder="Kitabın adı")
                
                with col2:
                    # Yazar seçimi
                    yazarlar_df = db.get_yazarlar()
                    if yazarlar_df is not None and len(yazarlar_df) > 0:
                        yazar_options = list(yazarlar_df['Ad_Soyad'])
                        yazar_secimi = st.selectbox("✍️ Yazar", yazar_options)
                        yazar_id = int(yazarlar_df[yazarlar_df['Ad_Soyad'] == yazar_secimi].iloc[0]['YazarID'])
                    else:
                        st.warning("⚠️ Henüz yazar kayıtlı değil!")
                        yazar_id = None
                
                col1, col2 = st.columns(2)
                with col1:
                    kategori = st.selectbox("📂 Kategori", KITAP_KATEGORILERI)
                
                with col2:
                    stok = st.number_input("📦 Stok Miktarı", min_value=1, value=1, step=1)
                
                col1, col2 = st.columns(2)
                with col1:
                    basim_tarihi = st.date_input("📅 Basım Tarihi")
                
                with col2:
                    sayfa = st.number_input("📄 Sayfa Sayısı", min_value=1, value=100, step=1)
                
                submitted = st.form_submit_button("✅ Kitabı Ekle", use_container_width=True, type="primary")
                
                if submitted:
                    # Validasyonlar
                    valid_isbn, msg = DataValidator.validate_isbn(isbn)
                    valid_baslik, msg2 = DataValidator.validate_baslik(baslik)
                    
                    if not valid_isbn:
                        st.error(f"❌ ISBN: {msg}")
                    elif not valid_baslik:
                        st.error(f"❌ Başlık: {msg2}")
                    elif not db.isbn_benzersiz_mi(isbn):
                        st.error("❌ Bu ISBN zaten kayıtlı!")
                    elif yazar_id is None:
                        st.error("❌ Lütfen yazar seçiniz!")
                    else:
                        success, message = db.kitap_ekle(isbn, baslik, yazar_id, kategori, basim_tarihi, sayfa, stok)
                        if success:
                            st.success(f"✅ {message}")
                            st.balloons()
                        else:
                            st.error(f"❌ Hata: {message}")
    
    # ===== SEKME 2: STOK YÖNETİMİ =====
    with tab2:
        st.subheader("Stok Durumu")
        
        if not db:
            st.info("💡 Stok verisi veritabanı bağlantısı gerektirir")
        else:
            kitaplar_df = db.get_kitaplar()
            if kitaplar_df is not None and len(kitaplar_df) > 0:
                # Filtreleme
                col1, col2 = st.columns(2)
                with col1:
                    kategori_filtre = st.multiselect("📂 Kategoriye Göre Filtrele", KITAP_KATEGORILERI, placeholder="Seçiniz")
                
                with col2:
                    stok_durumu = st.selectbox("📦 Stok Durumuna Göre", 
                                              ["Tümü", "Stok Bitti", "Az Stok (≤5)", "Yeterli Stok (>5)"])
                
                # Filtreleme uyguła
                filtered_df = kitaplar_df.copy()
                if kategori_filtre:
                    filtered_df = filtered_df[filtered_df['Kategori'].isin(kategori_filtre)]
                
                if stok_durumu == "Stok Bitti":
                    filtered_df = filtered_df[filtered_df['Stok_Miktari'] == 0]
                elif stok_durumu == "Az Stok (≤5)":
                    filtered_df = filtered_df[(filtered_df['Stok_Miktari'] > 0) & (filtered_df['Stok_Miktari'] <= 5)]
                elif stok_durumu == "Yeterli Stok (>5)":
                    filtered_df = filtered_df[filtered_df['Stok_Miktari'] > 5]
                
                # Tablo göster
                display_df = filtered_df[['Baslik', 'Yazar', 'Kategori', 'Stok_Miktari', 'Odenç_Sayisi']].copy()
                display_df.columns = ['Başlık', 'Yazar', 'Kategori', 'Stok', 'Ödünç Sayısı']
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                st.markdown("---")
                st.markdown(f"**Toplam Stok:** {filtered_df['Stok_Miktari'].sum()} | **Toplam Ödünç:** {filtered_df['Odenç_Sayisi'].sum()}")
            else:
                st.info("💡 Henüz kitap yok!")

def show_demo_kitap_envanteri():
    """Demo Kitap Envanteri - veritabanı yok"""
    st.warning("⚠️ Veritabanı bağlantısı kurulamadı. Demo veriler gösteriliyor...")
    
    tab1, tab2 = st.tabs(["➕ Yeni Kitap Ekle", "📊 Stok Yönetimi"])
    
    with tab1:
        st.subheader("Yeni Kitap Ekle (Demo)")
        st.info("💡 SQL Server bağlantısı yapıldığında yeni kitap ekleyebileceksiniz.")
    
    with tab2:
        st.subheader("Stok Durumu (Demo)")
        
        # Demo tablo
        demo_kitaplar = {
            'Başlık': ['Savaş ve Barış', 'Suç ve Ceza', '1984', 'Hayvan Çiftliği', 'Büyük Gatsby'],
            'Yazar': ['Tolstoy', 'Dostoyevski', 'Orwell', 'Orwell', 'Fitzgerald'],
            'Kategori': ['Edebiyat', 'Edebiyat', 'Distopya', 'Distopya', 'Edebiyat'],
            'Stok': [5, 3, 8, 2, 6],
            'Ödünç Sayısı': [12, 8, 25, 15, 10]
        }
        
        import pandas as pd
        df_demo = pd.DataFrame(demo_kitaplar)
        st.dataframe(df_demo, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown(f"**Toplam Stok:** {df_demo['Stok'].sum()} | **Toplam Ödünç:** {df_demo['Ödünç Sayısı'].sum()}")
