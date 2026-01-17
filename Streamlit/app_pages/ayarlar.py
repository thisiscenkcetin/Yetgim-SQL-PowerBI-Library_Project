import streamlit as st
from config.database import get_db_connection, test_connection
from config.settings import DEFAULT_ODENÇ_SURESI, ODENÇ_CEZASI_GUNLUK

def show():
    """Ayarlar Sayfası"""
    st.header("⚙️ Sistem Ayarları")
    
    db = get_db_connection()
    
    # Admin kontrolü
    if st.session_state.get("role") != "Kütüphaneci":
        st.error("❌ Bu sayfaya erişim yetkiniz yok.")
        return
    
    tab1, tab2, tab3 = st.tabs(["🗄️ Veritabanı", "⚙️ Kütüphane Ayarları", "📋 Sistem Günlüğü"])
    
    # ===== SEKME 1: VERİTABANI =====
    with tab1:
        st.subheader("Veritabanı Bağlantısı")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Bağlantı Durumu**")
            if db:
                st.success("✅ Bağlı")
            else:
                st.error("❌ Bağlantı Yok")
        
        with col2:
            if st.button("🔄 Bağlantıyı Test Et", use_container_width=True):
                success, message = test_connection()
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        st.markdown("---")
        st.markdown("**Veritabanı Bilgileri**")
        
        if db:
            try:
                stats = db.execute_query("""
                    SELECT 
                        COUNT(DISTINCT KitapID) as Kitap_Sayisi,
                        COUNT(DISTINCT UyeID) as Uye_Sayisi,
                        COUNT(*) as Hareket_Sayisi
                    FROM Odenç_Hareketleri
                """)
                
                if stats is not None:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Toplam Kitap", db.execute_query("SELECT COUNT(*) as cnt FROM Kitaplar").iloc[0]['cnt'])
                    with col2:
                        st.metric("Toplam Üye", db.execute_query("SELECT COUNT(*) as cnt FROM Uyeler").iloc[0]['cnt'])
                    with col3:
                        st.metric("Toplam Hareket", stats.iloc[0]['Hareket_Sayisi'])
            except:
                st.warning("⚠️ Bilgiler alınamadı")
    
    # ===== SEKME 2: KUTUPHANE AYARLARI =====
    with tab2:
        st.subheader("⚙️ Kütüphane Ayarları")
        
        st.info("💡 Bu ayarlar demo amaçlıdır. Gerçek ayarlar config/settings.py'da yapılır.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            odenç_suresi = st.number_input(
                "📅 Varsayılan Ödünç Süresi (gün)",
                min_value=1,
                max_value=60,
                value=DEFAULT_ODENÇ_SURESI,
                disabled=True
            )
        
        with col2:
            ceza_orani = st.number_input(
                "💰 Gecikme Cezası (TL/gün)",
                min_value=0.5,
                max_value=50.0,
                value=ODENÇ_CEZASI_GUNLUK,
                step=0.5,
                disabled=True
            )
        
        st.markdown("---")
        st.subheader("👤 Kullanıcı Yönetimi")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Demo Hesapları**")
            st.code("""
Kütüphaneci:
- Kullanıcı: kutuphane
- Şifre: 123456

Administrator:
- Kullanıcı: admin
- Şifre: admin123
            """)
    
    # ===== SEKME 3: SISTEM GÜNLÜĞÜ =====
    with tab3:
        st.subheader("📋 Sistem Günlüğü")
        
        if db:
            try:
                # Yakın zamandaki işlemler (Ödünç + İade)
                gunluk = db.execute_query("""
                    SELECT TOP 100
                        o.HareketID as Hareket_ID,
                        k.Baslik as Kitap,
                        u.Ad_Soyad as Uye,
                        o.Odenç_Tarihi as Tarih,
                        CASE WHEN o.Iade_Tarihi_Gercek IS NULL THEN 'Bekleniyor'
                             ELSE 'İade Edildi' END as Durum
                    FROM Odenç_Hareketleri o
                    JOIN Kitaplar k ON o.KitapID = k.KitapID
                    JOIN Uyeler u ON o.UyeID = u.UyeID
                    ORDER BY o.Odenç_Tarihi DESC
                """)
                
                if gunluk is not None and len(gunluk) > 0:
                    gunluk.columns = ['Hareket ID', 'Kitap', 'Üye', 'Tarih', 'Durum']
                    st.dataframe(gunluk, use_container_width=True, hide_index=True)
                else:
                    st.info("💡 Henüz işlem kaydı yok")
            except Exception as e:
                st.error(f"❌ Günlük alınamadı: {str(e)}")
        else:
            st.error("❌ Veritabanı bağlantısı yok!")
