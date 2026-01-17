import streamlit as st
from datetime import datetime
from config.database import get_db_connection
from modules.utils import Utils

def show():
    """İade İşlemleri Sayfası"""
    st.header("✅ İade İşlemini Kaydet")
    
    db = get_db_connection()
    
    if not db:
        st.warning("⚠️ Veritabanı bağlantısı kurulamadı. Demo modda çalışıyor...")
        st.info("💡 SQL Server bağlantısı yapıldığında iade işlemleri kayıt yapabileceksiniz.")
        return
    
    st.subheader("Aktif Ödünçleri Listele")
    
    # Üye filtrelemesi (opsiyonel)
    uyeler_df = db.get_uyeler()
    if uyeler_df is not None and len(uyeler_df) > 0:
        uye_options = ["Tümü"] + [f"{row['Ad_Soyad']} ({row['TC_Kimlik']})" 
                                 for _, row in uyeler_df.iterrows()]
        selected_uye_filter = st.selectbox("👤 Üyeye Göre Filtrele", uye_options)
        
        # Filtreleme
        if selected_uye_filter != "Tümü":
            tc = selected_uye_filter.split("(")[1].split(")")[0]
            selected_uye_id = uyeler_df[uyeler_df['TC_Kimlik'] == tc].iloc[0]['UyeID']
            aktif_odencs = db.get_aktif_odencs(uye_id=selected_uye_id)
        else:
            aktif_odencs = db.get_aktif_odencs()
    else:
        aktif_odencs = db.get_aktif_odencs()
    
    if aktif_odencs is None or len(aktif_odencs) == 0:
        st.info("💡 Şu an iade bekleyen kitap yok! ✅")
        return
    
    # Tablo olarak göster
    st.dataframe(
        aktif_odencs[[
            'HareketID', 'Üye', 'Kitap', 'Odenç_Tarihi', 
            'Iade_Tarihi_Planlandi', 'Gecen_Gun_Sayisi'
        ]].head(20),
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    st.subheader("📝 İade İşlemini Tamamla")
    
    with st.form("iade_form", border=True):
        # Hareket seçimi
        if aktif_odencs is not None and len(aktif_odencs) > 0:
            hareket_options = [
                f"#{int(row['HareketID'])} - {row['Üye']} / {row['Kitap']}"
                for _, row in aktif_odencs.iterrows()
            ]
            selected_hareket_index = st.selectbox(
                "📖 Iade edilecek kitabı seçin",
                range(len(hareket_options)),
                format_func=lambda i: hareket_options[i]
            )
            
            selected_hareket = aktif_odencs.iloc[selected_hareket_index]
            
            # Ön görünüm
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Üye", selected_hareket['Üye'])
            with col2:
                st.metric("Kitap", selected_hareket['Kitap'])
            with col3:
                st.metric("Gecikmiş Gün", int(selected_hareket['Gecen_Gun_Sayisi']))
            
            # İade tarihi seçimi
            col1, col2 = st.columns(2)
            with col1:
                iade_tarihi_gercek = st.date_input("✅ İade Tarihi", value=datetime.today())
            
            with col2:
                # Ceza tahmini
                from datetime import datetime as dt
                gecikmiş_gün = (iade_tarihi_gercek - selected_hareket['Iade_Tarihi_Planlandi']).days
                ceza = max(0, gecikmiş_gün * 5)
                st.metric("Tahmini Ceza", f"{ceza:.2f} TL")
            
            # Kütüphaneci onayı
            onayla = st.checkbox("✋ Kütüphaneci olarak onaylıyorum")
            
            submitted = st.form_submit_button("✅ İade İşlemini Tamamla", use_container_width=True, type="primary")
            
            if submitted:
                if not onayla:
                    st.error("❌ Onaylanız gerekli!")
                else:
                    success, message = db.iade_işlemi(
                        hareket_id=int(selected_hareket['HareketID']),
                        iade_tarihi_gercek=iade_tarihi_gercek
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        if ceza > 0:
                            st.info(f"💰 Uygulanan Ceza: {Utils.format_para(ceza)}")
                        st.balloons()
                    else:
                        st.error(f"❌ Hata: {message}")
