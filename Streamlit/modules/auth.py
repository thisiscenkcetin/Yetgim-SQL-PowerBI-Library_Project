import streamlit as st
from config.settings import ROLES

class AuthManager:
    """Kimlik doğrulama ve yetkilendirme"""
    
    @staticmethod
    def login_page():
        """Giriş sayfası"""
        st.markdown("---")
        
        col1, col2 = st.columns([0.5, 0.5], gap="large")
        
        with col1:
            username = st.text_input("👤 Kullanıcı Adı", placeholder="kutuphane")
        with col2:
            password = st.text_input("🔒 Şifre", type="password")
        
        if st.button("🔑 Giriş Yap", use_container_width=True, type="primary"):
            if username in ROLES:
                if ROLES[username]["password"] == password:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.role = ROLES[username]["role"]
                    st.session_state.permissions = ROLES[username]["permissions"]
                    st.success("✅ Giriş başarılı! Sayfayı yeniliyoruz...")
                    st.rerun()
                else:
                    st.error("❌ Şifre hatalı!")
            else:
                st.error("❌ Kullanıcı bulunamadı! Lütfen yetkili kimlik bilgilerini girin.")
        
        st.caption("Kütüphane Yetkilisi Demo Kullanıcı Adı: kutuphane / Parola: 123456")
    
    @staticmethod
    def require_login():
        """Giriş gerekli mi kontrol et"""
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        
        if not st.session_state.authenticated:
            AuthManager.login_page()
            st.stop()
    
    @staticmethod
    def require_permission(permission):
        """İzin gerekli mi kontrol et"""
        if permission not in st.session_state.get("permissions", []):
            st.error(f"❌ Bu işlemi yapmaya yetkiniz yok. ({permission} gerekli)")
            st.stop()
    
    @staticmethod
    def logout():
        """Çıkış yap"""
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.permissions = []
