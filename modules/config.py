# BIST Teknik Analiz Uygulaması Konfigürasyonu

# En popüler BIST hisseleri
BIST_SYMBOLS = {
    "THYAO.IS": "Türk Hava Yolları",
    "TUPRS.IS": "Tüpraş",
    "BIMAS.IS": "BİM",
    "AKBNK.IS": "Akbank",
    "GARAN.IS": "Garanti Bankası",
    "ISCTR.IS": "İş Bankası",
    "HALKB.IS": "Halkbank",
    "VAKBN.IS": "Vakıfbank",
    "ARCLK.IS": "Arçelik",
    "KCHOL.IS": "Koç Holding",
    "EREGL.IS": "Ereğli Demir Çelik",
    "PETKM.IS": "Petkim",
    "TCELL.IS": "Turkcell",
    "ASELS.IS": "Aselsan",
    "TOASO.IS": "Tofaş",
    "SISE.IS": "Şişe Cam",
    "KOZAL.IS": "Koton",
    "MGROS.IS": "Migros",
    "FROTO.IS": "Ford Otosan",
    "SAHOL.IS": "Sabancı Holding",
    "DOHOL.IS": "Doğan Holding",
    "PGSUS.IS": "Pegasus",
    "EKGYO.IS": "Emlak Konut GYO",
    "VESTL.IS": "Vestel",
    "KOZAA.IS": "Koza Altın",
    "ENKAI.IS": "Enka İnşaat",
    "TAVHL.IS": "TAV Havalimanları",
    "ULKER.IS": "Ülker",
    "SOKM.IS": "Şok Marketler",
    "TATGD.IS": "TAT Gıda"
}

# Teknik indikatör konfigürasyonu
INDICATORS_CONFIG = {
    "sma_20": {
        "name": "Basit Hareketli Ortalama (20)",
        "period": 20,
        "default": True
    },
    "sma_50": {
        "name": "Basit Hareketli Ortalama (50)",
        "period": 50,
        "default": True
    },
    "ema_12": {
        "name": "Üssel Hareketli Ortalama (12)",
        "period": 12,
        "default": False
    },
    "ema_26": {
        "name": "Üssel Hareketli Ortalama (26)",
        "period": 26,
        "default": False
    },
    "rsi": {
        "name": "Göreceli Güç Endeksi (RSI)",
        "period": 14,
        "default": True,
        "overbought": 70,
        "oversold": 30
    },
    "macd": {
        "name": "MACD",
        "fast": 12,
        "slow": 26,
        "signal": 9,
        "default": True
    },
    "bollinger": {
        "name": "Bollinger Bantları",
        "period": 20,
        "std": 2,
        "default": True
    },
    "stoch": {
        "name": "Stokastik Osilatör",
        "k_period": 14,
        "d_period": 3,
        "default": False
    },
    "williams_r": {
        "name": "Williams %R",
        "period": 14,
        "default": False
    },
    "cci": {
        "name": "Emtia Kanal Endeksi (CCI)",
        "period": 20,
        "default": False
    }
}

# Alert konfigürasyonu
ALERT_CONFIG = {
    "rsi_oversold": 30,
    "rsi_overbought": 70,
    "volume_spike_multiplier": 2.0,
    "price_change_threshold": 5.0,  # Yüzde
    "update_interval": 300,  # Saniye (5 dakika)
}

# Grafik renkleri
CHART_COLORS = {
    "green": "#00ff00",
    "red": "#ff0000",
    "blue": "#0000ff",
    "orange": "#ffa500",
    "purple": "#800080",
    "gray": "#808080",
    "yellow": "#ffff00",
    "cyan": "#00ffff"
}

# Zaman aralıkları
TIME_PERIODS = {
    "1d": "1 Gün",
    "5d": "5 Gün", 
    "1mo": "1 Ay",
    "3mo": "3 Ay",
    "6mo": "6 Ay",
    "1y": "1 Yıl",
    "2y": "2 Yıl",
    "5y": "5 Yıl",
    "10y": "10 Yıl",
    "ytd": "Yıl Başından İtibaren",
    "max": "Maksimum"
} 