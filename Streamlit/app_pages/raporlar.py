import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from config.database import get_db_connection
from modules.utils import Utils

def show():
    """Raporlar Sayfası"""
    st.header("📊 Raporlar & Analizler")
    
    db = get_db_connection()
    
    if not db:
        st.warning("⚠️ Veritabanı bağlantısı kurulamadı. Lütfen SQL Server bilgilerini kontrol edin.")
        st.info("💡 Sistem bağlantısı yapıldığında raporlar gösterilecektir.")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Popülarite Sıralaması",
        "⚠️ Gecikmiş İadeleler",
        "👥 Üye İstatistikleri",
        "📈 Aylık Trend"
    ])
    
    # ===== SEKME 1: POPÜLARİTE =====
    with tab1:
        st.subheader("📚 En Popüler Kitaplar")
        
        pop_data = db.get_popurite_raporlari(limit=15)
        if pop_data is not None and len(pop_data) > 0:
            # Tablo
            display_columns = ['Baslik', 'Yazar', 'Odenç_Sayisi', 'Stok_Durumu']
            if all(col in pop_data.columns for col in display_columns):
                display_df = pop_data[display_columns].copy()
                display_df.columns = ['Başlık', 'Yazar', 'Ödünç Sayısı', 'Stok Durumu']
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Bar Chart
            st.subheader("📊 Ödünç Sayısı (Top 10)")
            top_10 = pop_data.head(10)
            
            fig = go.Figure(data=[go.Bar(
                x=top_10['Odenç_Sayisi'],
                y=top_10['Baslik'],
                orientation='h',
                marker=dict(color='#8B4513')
            )])
            
            fig.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=20, b=20),
                xaxis_title="Ödünç Sayısı",
                yaxis_title="Kitap Başlığı"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("💡 Henüz veri yok")
    
    # ===== SEKME 2: GECİKMİŞ İADELER =====
    with tab2:
        st.subheader("⚠️ Gecikmiş İadeleler")
        
        gecikmiş_df = db.get_gecikmiş_iadeleler()
        if gecikmiş_df is not None and len(gecikmiş_df) > 0:
            # İstatistikler
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Toplam Gecikmiş", len(gecikmiş_df))
            with col2:
                st.metric("Toplam Ceza", Utils.format_para(gecikmiş_df['Tahmini_Ceza_Tutari'].sum()))
            with col3:
                st.metric("Ortalama Gecikmiş Gün", f"{gecikmiş_df['Gecikmiş_Gun'].mean():.1f}")
            
            st.markdown("---")
            
            # Tablo
            display_columns = ['Üye_Adi', 'Kitap_Adi', 'Gecikmiş_Gun', 'Tahmini_Ceza_Tutari']
            if all(col in gecikmiş_df.columns for col in display_columns):
                display_df = gecikmiş_df[display_columns].copy()
                display_df.columns = ['Üye Adı', 'Kitap Adı', 'Gün', 'Ceza (TL)']
                display_df['Ceza (TL)'] = display_df['Ceza (TL)'].apply(lambda x: Utils.format_para(x))
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("💡 Gecikmiş iade yok! ✅")
    
    # ===== SEKME 3: ÜYE İSTATİSTİKLERİ =====
    with tab3:
        st.subheader("👥 Üye Analizi")
        
        uye_stats = db.get_uye_istatistikleri(limit=20)
        if uye_stats is not None and len(uye_stats) > 0:
            # İstatistikler
            total_uye = db.execute_query("SELECT COUNT(*) as cnt FROM Uyeler").iloc[0]['cnt']
            aktif_uye = db.execute_query("SELECT COUNT(*) as cnt FROM Uyeler WHERE Uyelik_Durumu='Aktif'").iloc[0]['cnt']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Toplam Üye", total_uye)
            with col2:
                st.metric("Aktif Üye", aktif_uye)
            with col3:
                st.metric("Pasif Üye", total_uye - aktif_uye)
            
            st.markdown("---")
            
            # En Aktif Üyeler
            st.subheader("🏆 En Aktif 10 Üye")
            display_columns = ['Ad_Soyad', 'Toplam_Odenç_Sayisi', 'Aktivite_Düzeyi']
            if all(col in uye_stats.columns for col in display_columns):
                display_df = uye_stats[display_columns].head(10).copy()
                display_df.columns = ['Ad-Soyad', 'Ödünç Sayısı', 'Aktivite']
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("💡 Henüz veri yok")
    
    # ===== SEKME 4: AYLIK TREND =====
    with tab4:
        st.subheader("Aylık Ödünç Trendi")
        
        trend_data = db.get_aylik_trend()
        if trend_data is not None and len(trend_data) > 0:
            trend_data = trend_data.sort_values(['Yil', 'Ay'])
            
            # Grafik
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=trend_data['Ay_Adi'],
                y=trend_data['Toplam_Odenç'],
                mode='lines+markers',
                name='Toplam Ödünç',
                line=dict(color='#8B4513', width=3),
                marker=dict(size=10)
            ))
            
            fig.add_trace(go.Bar(
                x=trend_data['Ay_Adi'],
                y=trend_data['Iade_Edilen'],
                name='İade Edilen',
                marker=dict(color='#70AD47'),
                opacity=0.5
            ))
            
            fig.update_layout(
                height=400,
                hovermode='x unified',
                margin=dict(l=20, r=20, t=20, b=20),
                barmode='overlay'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Tablo
            display_columns = ['Ay_Adi', 'Toplam_Odenç', 'Iade_Edilen', 'Penderler', 'Ort_Odenç_Gunu']
            if all(col in trend_data.columns for col in display_columns):
                display_df = trend_data[display_columns].copy()
                display_df.columns = ['Ay', 'Toplam', 'İade Edilen', 'Penderler', 'Ort. Gün']
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("💡 Henüz veri yok")
