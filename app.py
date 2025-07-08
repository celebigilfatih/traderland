import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

# Kendi modüllerimizi import ediyoruz
from modules.data_fetcher import BISTDataFetcher
from modules.technical_analysis import TechnicalAnalyzer
from modules.alert_system import AlertSystem
from modules.config import BIST_SYMBOLS, INDICATORS_CONFIG

# Sayfa konfigürasyonu
st.set_page_config(
    page_title="BIST Teknik Analiz Uygulaması",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS stili
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1e3d59;
    }
    .buy-signal {
        color: #00ff00;
        font-weight: bold;
    }
    .sell-signal {
        color: #ff0000;
        font-weight: bold;
    }
    .hold-signal {
        color: #ffa500;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">📈 BIST Teknik Analiz Uygulaması</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("⚙️ Ayarlar")
    
    # Hisse seçimi
    selected_symbol = st.sidebar.selectbox(
        "📊 Hisse Seçin",
        options=list(BIST_SYMBOLS.keys()),
        format_func=lambda x: f"{x} - {BIST_SYMBOLS[x]}"
    )
    
    # Zaman aralığı seçimi
    time_period = st.sidebar.selectbox(
        "📅 Zaman Aralığı",
        ["1mo", "3mo", "6mo", "1y", "2y"]
    )
    
    # İndikatör seçimi
    st.sidebar.subheader("📈 İndikatörler")
    selected_indicators = {}
    for indicator, config in INDICATORS_CONFIG.items():
        selected_indicators[indicator] = st.sidebar.checkbox(
            config["name"], 
            value=config["default"]
        )
    
    # Alert ayarları
    st.sidebar.subheader("🚨 Alert Ayarları")
    enable_alerts = st.sidebar.checkbox("Alertleri Aktifleştir", value=True)
    
    if enable_alerts:
        alert_methods = st.sidebar.multiselect(
            "Alert Yöntemleri",
            ["Email", "Telegram", "Desktop"],
            default=["Desktop"]
        )
    
    # Ana içerik
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader(f"📊 {selected_symbol} - {BIST_SYMBOLS[selected_symbol]}")
        
        # Veri çekme ve analiz
        try:
            with st.spinner("Veriler yükleniyor..."):
                fetcher = BISTDataFetcher()
                df = fetcher.get_stock_data(selected_symbol, period=time_period)
                
                if df is not None and not df.empty:
                    analyzer = TechnicalAnalyzer(df)
                    
                    # Teknik indikatörleri hesapla
                    for indicator, enabled in selected_indicators.items():
                        if enabled:
                            analyzer.add_indicator(indicator)
                    
                    # Ana grafik
                    fig = create_chart(df, analyzer, selected_indicators)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Al-Sat sinyali hesapla
                    alert_system = AlertSystem()
                    signal = alert_system.generate_signal(analyzer)
                    
                    # Sinyal gösterimi
                    signal_color = "buy-signal" if signal == "AL" else "sell-signal" if signal == "SAT" else "hold-signal"
                    st.markdown(f'<div class="{signal_color}">🎯 Sinyal: {signal}</div>', unsafe_allow_html=True)
                    
                else:
                    st.error("Veri yüklenemedi!")
                    
        except Exception as e:
            st.error(f"Hata oluştu: {str(e)}")
    
    with col2:
        st.subheader("📈 Güncel Bilgiler")
        if 'df' in locals() and df is not None:
            latest = df.iloc[-1]
            prev = df.iloc[-2]
            
            change = latest['Close'] - prev['Close']
            change_pct = (change / prev['Close']) * 100
            
            st.metric(
                label="Son Fiyat",
                value=f"₺{latest['Close']:.2f}",
                delta=f"{change:.2f} ({change_pct:.2f}%)"
            )
            
            st.metric(
                label="Hacim",
                value=f"{latest['Volume']:,.0f}"
            )
            
            st.metric(
                label="En Yüksek",
                value=f"₺{latest['High']:.2f}"
            )
            
            st.metric(
                label="En Düşük",
                value=f"₺{latest['Low']:.2f}"
            )
    
    with col3:
        st.subheader("🎯 İndikatör Değerleri")
        if 'analyzer' in locals():
            indicator_values = analyzer.get_latest_indicators()
            for indicator, value in indicator_values.items():
                if selected_indicators.get(indicator, False):
                    st.metric(
                        label=INDICATORS_CONFIG[indicator]["name"],
                        value=f"{value:.2f}" if value else "N/A"
                    )

def create_chart(df, analyzer, selected_indicators):
    """Grafik oluşturur"""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_width=[0.7, 0.15, 0.15],
        subplot_titles=('Fiyat Grafiği', 'Hacim', 'İndikatörler')
    )
    
    # Candlestick grafiği
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name="Fiyat"
        ),
        row=1, col=1
    )
    
    # Seçilen indikatörleri ekle
    if selected_indicators.get('sma_20', False):
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=analyzer.indicators.get('sma_20'),
                name="SMA 20",
                line=dict(color='blue', width=1)
            ),
            row=1, col=1
        )
    
    if selected_indicators.get('sma_50', False):
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=analyzer.indicators.get('sma_50'),
                name="SMA 50",
                line=dict(color='red', width=1)
            ),
            row=1, col=1
        )
    
    # Bollinger Bands
    if selected_indicators.get('bollinger', False):
        bb_upper = analyzer.indicators.get('bb_upper')
        bb_lower = analyzer.indicators.get('bb_lower')
        if bb_upper is not None and bb_lower is not None:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=bb_upper,
                    name="BB Üst",
                    line=dict(color='gray', dash='dash')
                ),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=bb_lower,
                    name="BB Alt",
                    line=dict(color='gray', dash='dash'),
                    fill='tonexty'
                ),
                row=1, col=1
            )
    
    # Hacim grafiği
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name="Hacim",
            marker_color='lightblue'
        ),
        row=2, col=1
    )
    
    # RSI
    if selected_indicators.get('rsi', False):
        rsi = analyzer.indicators.get('rsi')
        if rsi is not None:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=rsi,
                    name="RSI",
                    line=dict(color='purple')
                ),
                row=3, col=1
            )
            # RSI referans çizgileri
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    fig.update_layout(
        title=f"{df.index[0].strftime('%Y-%m-%d')} - {df.index[-1].strftime('%Y-%m-%d')}",
        xaxis_rangeslider_visible=False,
        height=800
    )
    
    return fig

if __name__ == "__main__":
    main() 