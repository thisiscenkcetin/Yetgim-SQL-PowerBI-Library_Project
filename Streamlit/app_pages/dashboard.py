import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from config.database import get_db_connection
from modules.utils import Utils

def show():
    """Dashboard Sayfası"""
    st.header("📊 Sistem Özeti")
    
    db = get_db_connection()
    
    if not db:
        st.warning("⚠️ Veritabanı bağlantısı kurulamadı. Demo veriler gösteriliyor...")
        # Demo veriler
        stats = {
            'toplam_kitap': 1250,
            'aktif_uye': 340,
            'aktif_odenç': 85,
            'gecikmiş_odenç': 12
        }
    else:
        stats = db.get_dashboard_ozet()
    
    # ===== KPI KARTLARI =====
    st.subheader("Anlık Durum")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📚 Toplam Kitap",
            f"{stats['toplam_kitap']:,}",
            delta=None,
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "👥 Aktif Üye",
            f"{stats['aktif_uye']:,}",
            delta=None,
            delta_color="off"
        )
    
    with col3:
        st.metric(
            "📖 Aktif Ödünç",
            f"{stats['aktif_odenç']:,}",
            delta=None,
            delta_color="off"
        )
    
    with col4:
        st.metric(
            "⏰ Gecikmiş İade",
            f"{stats['gecikmiş_odenç']:,}",
            delta=None,
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # ===== GRAFIKLER =====
    st.subheader("📊 Analizler")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Aylık Ödünç Trendi (Son 12 Ay)")
        if db:
            trend_data = db.get_aylik_trend()
            
            if trend_data is not None and len(trend_data) > 0:
                # Tarih oluştur (YYYY-MM formatında)
                trend_data['Tarih'] = trend_data.apply(
                    lambda x: f"{int(x['Yil'])}-{int(x['Ay']):02d}", axis=1
                )
                trend_data = trend_data.sort_values('Tarih').tail(12)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=trend_data['Ay_Adi'],
                    y=trend_data['Toplam_Odenç'],
                    mode='lines+markers',
                    name='Ödünç Sayısı',
                    line=dict(color='#8B4513', width=3),
                    marker=dict(size=10)
                ))
                
                fig.update_layout(
                    height=350,
                    hovermode='x unified',
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Henüz veri yok")
        else:
            st.info("💡 Demo: Grafik veritabanı bağlantısı gerektirir")
    
    with col2:
        st.markdown("#### Kategori Dağılımı")
        if db:
            cat_data = db.execute_query("""
                SELECT Kategori, COUNT(*) as Sayı
                FROM Kitaplar
                WHERE Kategori IS NOT NULL
                GROUP BY Kategori
                ORDER BY Sayı DESC
            """)
            
            if cat_data is not None and len(cat_data) > 0:
                fig = go.Figure(data=[go.Pie(
                    labels=cat_data['Kategori'],
                    values=cat_data['Sayı'],
                    hole=0.3,
                    hovertemplate='<b>%{label}</b><br>%{value} Kitap<extra></extra>'
                )])
                
                fig.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("💡 Henüz veri yok")
        else:
            st.info("💡 Demo: Grafik veritabanı bağlantısı gerektirir")
    
    st.markdown("---")
    
    # ===== GECİKMİŞ İADELER TABLOSU =====
    st.subheader("⚠️ Gecikmiş İadeleler")
    if db:
        gecikmiş_df = db.get_gecikmiş_iadeleler()
        
        if gecikmiş_df is not None and len(gecikmiş_df) > 0:
            # Görüntülenecek sütunları seç
            display_columns = ['Üye_Adi', 'Kitap_Adi', 'Gecikmiş_Gun', 'Tahmini_Ceza_Tutari']
            if all(col in gecikmiş_df.columns for col in display_columns):
                display_df = gecikmiş_df[display_columns].head(10).copy()
                display_df.columns = ['Üye Adı', 'Kitap Adı', 'Gün', 'Ceza (TL)']
                display_df['Ceza (TL)'] = display_df['Ceza (TL)'].apply(lambda x: Utils.format_para(x))
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info("💡 Şu an gecikmiş iade yok! ✅")
        else:
            st.info("💡 Şu an gecikmiş iade yok! ✅")
    else:
        st.info("💡 Demo: Gecikmiş iade veritabanı bağlantısı gerektirir")
    
    st.markdown("---")
    
    # ===== EN POPÜLER KİTAPLAR =====
    st.subheader("📚 En Popüler 5 Kitap")
    if db:
        pop_data = db.get_popurite_raporlari(limit=5)
        
        if pop_data is not None and len(pop_data) > 0:
            display_columns = ['Baslik', 'Yazar', 'Odenç_Sayisi']
            if all(col in pop_data.columns for col in display_columns):
                display_df = pop_data[display_columns].copy()
                display_df.columns = ['Başlık', 'Yazar', 'Ödünç Sayısı']
                st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("💡 Demo: Popüler kitaplar veritabanı bağlantısı gerektirir")
    
    if pop_data is not None and len(pop_data) > 0:
        display_columns = ['Baslik', 'Yazar', 'Odenç_Sayisi']
        if all(col in pop_data.columns for col in display_columns):
            display_df = pop_data[display_columns].copy()
            display_df.columns = ['Kitap Başlığı', 'Yazar', 'Ödünç Sayısı']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
