import streamlit as st
from config.database import get_db_connection
from modules.validators import DataValidator
from modules.utils import Utils
from datetime import datetime

def show():
    """Üye Yönetimi Sayfası"""
    st.header("👥 Üye Yönetimi")
    
    db = get_db_connection()
    
    if not db:
        st.warning("⚠️ Veritabanı bağlantısı kurulamadı. Lütfen SQL Server bilgilerini kontrol edin.")
        st.info("💡 Sistem bağlantısı yapıldığında üye işlemleri yapabileceksiniz.")
        return
    
    tab1, tab2 = st.tabs(["➕ Yeni Üye Kayıt", "🔍 Üye Sorgula & Güncelle"])
    
    # ===== SEKME 1: YENİ ÜYE KAYIT =====
    with tab1:
        st.subheader("Yeni Üye Kaydet")
        
        with st.form("uye_kayit_form", border=True):
            col1, col2 = st.columns(2)
            
            with col1:
                ad_soyad = st.text_input("👤 Ad-Soyad", placeholder="Örn: Ahmet Kaya")
                tc_kimlik = st.text_input("🆔 TC Kimlik (11 Rakam)", placeholder="12345678901")
            
            with col2:
                email = st.text_input("📧 Email (Opsiyonel)", placeholder="ahmet@example.com")
                telefon = st.text_input("📱 Telefon (Opsiyonel)", placeholder="5551234567")
            
            adres = st.text_area("🏠 Adres", height=80)
            
            submitted = st.form_submit_button("✅ Üyeyi Kaydet", use_container_width=True, type="primary")
            
            if submitted:
                # Validasyonlar
                valid_ad, msg_ad = DataValidator.validate_ad_soyad(ad_soyad)
                valid_tc, msg_tc = DataValidator.validate_tc_kimlik(tc_kimlik)
                valid_email, msg_email = DataValidator.validate_email(email)
                valid_telefon, msg_telefon = DataValidator.validate_telefon(telefon)
                
                if not valid_ad:
                    st.error(f"❌ Ad-Soyad: {msg_ad}")
                elif not valid_tc:
                    st.error(f"❌ TC Kimlik: {msg_tc}")
                elif not valid_email:
                    st.error(f"❌ Email: {msg_email}")
                elif not valid_telefon:
                    st.error(f"❌ Telefon: {msg_telefon}")
                elif not db.tc_benzersiz_mi(tc_kimlik):
                    st.error("❌ Bu TC Kimlik zaten kayıtlı!")
                else:
                    success, message = db.uye_kaydet(ad_soyad, tc_kimlik, email, telefon, adres)
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ Hata: {message}")
    
    # ===== SEKME 2: SORGULA & GÜNCELLE =====
    with tab2:
        st.subheader("Üye Bilgileri")
        
        uyeler_df = db.get_uyeler()
        if uyeler_df is not None and len(uyeler_df) > 0:
            uye_options = [f"{row['Ad_Soyad']} ({row['TC_Kimlik']})" 
                          for _, row in uyeler_df.iterrows()]
            selected_uye_index = st.selectbox("👤 Üyeyi Seçin", range(len(uye_options)),
                                             format_func=lambda i: uye_options[i])
            
            selected_uye = uyeler_df.iloc[selected_uye_index]
            
            st.markdown("---")
            
            # Bilgileri göster
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Ad-Soyad", selected_uye['Ad_Soyad'])
                st.metric("TC Kimlik", selected_uye['TC_Kimlik'])
                st.metric("Email", selected_uye['Email'] or "Yok")
            
            with col2:
                st.metric("Telefon", selected_uye['Telefon'] or "Yok")
                st.metric("Üyelik Tarihi", str(selected_uye['Uyelik_Tarihi']))
                st.metric("Durum", f"{Utils.durum_rengi(selected_uye['Uyelik_Durumu'])} {selected_uye['Uyelik_Durumu']}")
            
            st.metric("Toplam Ceza", f"{Utils.format_para(selected_uye['Ceza_Miktari'])}")
            
            st.markdown("---")
            st.subheader("⚙️ İşlemler")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🚫 Üyeliği Askıya Al", use_container_width=True):
                    success, msg = db.uye_guncelle(
                        int(selected_uye['UyeID']),
                        Uyelik_Durumu="Askıda"
                    )
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            
            with col2:
                if st.button("✅ Üyeliği Aktif Et", use_container_width=True):
                    success, msg = db.uye_guncelle(
                        int(selected_uye['UyeID']),
                        Uyelik_Durumu="Aktif"
                    )
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            
            with col3:
                if st.button("💰 Cezayı Sıfırla", use_container_width=True):
                    if st.session_state.get("role") == "Administrator":
                        success, msg = db.uye_guncelle(
                            int(selected_uye['UyeID']),
                            Ceza_Miktari=0
                        )
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    else:
                        st.error("❌ Sadece administrator ceza sıfırlayabilir!")
        else:
            st.info("💡 Henüz üye yok!")
