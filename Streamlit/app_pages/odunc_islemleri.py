import streamlit as st
from datetime import datetime, timedelta
from config.database import get_db_connection
from modules.validators import DataValidator
from config.settings import DEFAULT_ODENÇ_SURESI

def show():
    """Ödünç İşlemleri Sayfası"""
    st.header("📖 Ödünç Hareketini Kaydet")
    
    db = get_db_connection()
    
    if not db:
        st.warning("⚠️ Veritabanı bağlantısı kurulamadı. Demo modda çalışıyor...")
        st.info("💡 SQL Server bağlantısı yapıldığında ödünç işlemleri kayıt yapabileceksiniz.")
        return
    
    with st.form("odenç_form", border=True):
        st.subheader("Ödünç Bilgileri")
        
        col1, col2 = st.columns(2)
        
        # ===== ÜYE SEÇİMİ =====
        with col1:
            uyeler_df = db.get_uyeler(durum_filtresi=None)
            
            if uyeler_df is not None and len(uyeler_df) > 0:
                # Filtreleme - sadece Aktif ve Pasif
                uyeler_df = uyeler_df[uyeler_df['Uyelik_Durumu'].isin(['Aktif', 'Pasif'])]
                
                uye_options = [f"{row['Ad_Soyad']} ({row['TC_Kimlik']})" 
                              for _, row in uyeler_df.iterrows()]
                selected_uye_index = st.selectbox("👤 Üyeyi Seçin", range(len(uye_options)), 
                                                  format_func=lambda i: uye_options[i])
                
                selected_uye = uyeler_df.iloc[selected_uye_index]
                
                # Uyarı - Ceza
                if selected_uye['Ceza_Miktari'] > 0:
                    st.warning(f"⚠️ Bu üyenin {selected_uye['Ceza_Miktari']:.2f} TL cezası var!")
            else:
                st.error("❌ Üye bulunamadı!")
                selected_uye = None
        
        # ===== KİTAP SEÇİMİ =====
        with col2:
            kitaplar_df = db.get_kitaplar(stok_filtresi=True)
            
            if kitaplar_df is not None and len(kitaplar_df) > 0:
                kitap_options = [f"{row['Baslik']} ({row['ISBN']}) - {row['Yazar']}" 
                                for _, row in kitaplar_df.iterrows()]
                selected_kitap_index = st.selectbox("📚 Kitabı Seçin", range(len(kitap_options)),
                                                    format_func=lambda i: kitap_options[i])
                selected_kitap = kitaplar_df.iloc[selected_kitap_index]
            else:
                st.error("❌ Stokta kitap yok!")
                selected_kitap = None
        
        # ===== TARİH SEÇİMİ =====
        st.subheader("📅 Tarihler")
        col1, col2 = st.columns(2)
        
        with col1:
            odenç_tarihi = st.date_input("Ödünç Tarihi", value=datetime.today())
        
        with col2:
            default_iade = odenç_tarihi + timedelta(days=DEFAULT_ODENÇ_SURESI)
            iade_tarihi = st.date_input("İade Tarihi (14 gün sonrası)", value=default_iade)
        
        # ===== NOTLAR =====
        notlar = st.text_area("📝 Notlar (Opsiyonel)", max_chars=255, height=80)
        
        # ===== SUBMIT BUTTON =====
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("✅ Ödünç Ver", use_container_width=True, type="primary")
        with col2:
            cancelled = st.form_submit_button("❌ İptal", use_container_width=True)
        
        if submitted:
            # Validasyonlar
            if selected_uye is None or selected_kitap is None:
                st.error("❌ Üye ve kitap seçilmesi gerekli!")
            elif odenç_tarihi > iade_tarihi:
                st.error("❌ İade tarihi ödünç tarihinden sonra olmalı!")
            else:
                # Veritabanına kaydet
                success, message = db.yeni_odenç(
                    kitap_id=int(selected_kitap['KitapID']),
                    uye_id=int(selected_uye['UyeID']),
                    odenç_tarihi=odenç_tarihi,
                    iade_tarihi=iade_tarihi,
                    notlar=notlar if notlar else None
                )
                
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                else:
                    st.error(f"❌ Hata: {message}")
        
        if cancelled:
            st.info("İşlem iptal edildi.")
