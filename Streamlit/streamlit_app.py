import streamlit as st
from modules.auth import AuthManager
from app_pages import dashboard, odenç_islemleri, iade_islemleri, uye_yonetimi, kitap_envanteri, raporlar, ayarlar

# ===== SAYFA AYARI =====
st.set_page_config(
    page_title="Yetgim Kütüphanesi",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== STİL =====
st.markdown("""
<style>
    [data-testid="stMetric"] {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.title("📚 Pendik Belediyesi YETGİM Kütüphanesi")
st.markdown("**Kütüphane Yönetim Sistemi - Kütüphaneci Paneli**")

# ===== AUTHENTİKASYON =====
if not st.session_state.get("authenticated", False):
    AuthManager.login_page()
else:
    # ===== HEADER + LOGOUT =====
    col1, col2, col3 = st.columns([2, 2, 1])
    with col3:
        logout_col1, logout_col2 = st.columns(2)
        with logout_col1:
            st.markdown(f"**Hoş geldiniz**")
            st.markdown(f"*{st.session_state.get('role', 'Rol')}*")
        with logout_col2:
            if st.button("🚪 Çıkış", use_container_width=True):
                AuthManager.logout()
                st.rerun()
    
    st.markdown("---")
    
    # ===== NAVİGASYON MENÜSÜ =====
    st.sidebar.markdown("### 📋 Menü")
    
    page = st.sidebar.radio(
        "Sayfayı Seçin:",
        [
            "Kontrol Paneli",
            "Ödünç İşlemleri",
            "İade İşlemleri",
            "Üye Yönetimi",
            "Kitap Envanteri",
            "Raporlar",
            "Ayarlar"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Sistem Bilgisi:**")
    st.sidebar.info("v1.0 Beta | SQL Server | Streamlit")
    
    # ===== SAYFA ROUTU =====
    if page == "Kontrol Paneli":
        dashboard.show()
    
    elif page == "Ödünç İşlemleri":
        AuthManager.require_permission("write_odenç")
        odenç_islemleri.show()
    
    elif page == "İade İşlemleri":
        AuthManager.require_permission("write_iade")
        iade_islemleri.show()
    
    elif page == "Üye Yönetimi":
        AuthManager.require_permission("read")
        uye_yonetimi.show()
    
    elif page == "Kitap Envanteri":
        AuthManager.require_permission("read")
        kitap_envanteri.show()
    
    elif page == "Raporlar":
        AuthManager.require_permission("read")
        raporlar.show()
    
    elif page == "Ayarlar":
        AuthManager.require_permission("admin")
        ayarlar.show()

# ===== FOOTER =====
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    © 2026 Pendik Belediyesi YETGİM Kütüphanesi v1.0
    </div>
    """, unsafe_allow_html=True)
