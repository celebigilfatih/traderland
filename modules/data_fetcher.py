import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import time
from typing import Optional, Dict, List

class BISTDataFetcher:
    """Borsa İstanbul verilerini çeken sınıf"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_stock_data(self, symbol: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Hisse verilerini çeker
        
        Args:
            symbol: Hisse kodu (örn: "THYAO.IS")
            period: Zaman aralığı (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Veri aralığı (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        
        Returns:
            DataFrame: OHLCV verileri
        """
        try:
            # Yahoo Finance kullanarak veri çek
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                print(f"Veri bulunamadı: {symbol}")
                return None
            
            # Sütun isimlerini düzenle
            df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # NaN değerleri temizle
            df = df.dropna()
            
            # Veri tiplerini kontrol et
            for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Son veriyi kontrol et
            if len(df) < 50:  # En az 50 gün veri olsun
                print(f"Yetersiz veri: {symbol} - {len(df)} kayıt")
                return None
            
            return df
            
        except Exception as e:
            print(f"Veri çekme hatası {symbol}: {str(e)}")
            return None
    
    def get_real_time_data(self, symbol: str) -> Optional[Dict]:
        """
        Gerçek zamanlı veri çeker
        
        Args:
            symbol: Hisse kodu
            
        Returns:
            Dict: Anlık veriler
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Güncel fiyat bilgileri
            current_data = {
                'symbol': symbol,
                'current_price': info.get('currentPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'open': info.get('open', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('forwardPE', 0),
                'change': 0,
                'change_percent': 0
            }
            
            # Değişim hesapla
            if current_data['previous_close'] > 0:
                current_data['change'] = current_data['current_price'] - current_data['previous_close']
                current_data['change_percent'] = (current_data['change'] / current_data['previous_close']) * 100
            
            return current_data
            
        except Exception as e:
            print(f"Gerçek zamanlı veri hatası {symbol}: {str(e)}")
            return None
    
    def get_multiple_stocks(self, symbols: List[str], period: str = "1y") -> Dict[str, pd.DataFrame]:
        """
        Birden fazla hissenin verilerini çeker
        
        Args:
            symbols: Hisse kodları listesi
            period: Zaman aralığı
            
        Returns:
            Dict: Hisse kodu -> DataFrame eşlemesi
        """
        results = {}
        
        for symbol in symbols:
            df = self.get_stock_data(symbol, period)
            if df is not None:
                results[symbol] = df
            time.sleep(0.1)  # Rate limiting
        
        return results
    
    def get_bist_index_data(self, index: str = "XU100.IS", period: str = "1y") -> Optional[pd.DataFrame]:
        """
        BIST endeks verilerini çeker
        
        Args:
            index: Endeks kodu (XU100.IS, XU030.IS, vb.)
            period: Zaman aralığı
            
        Returns:
            DataFrame: Endeks verileri
        """
        return self.get_stock_data(index, period)
    
    def validate_symbol(self, symbol: str) -> bool:
        """
        Hisse kodunun geçerli olup olmadığını kontrol eder
        
        Args:
            symbol: Hisse kodu
            
        Returns:
            bool: Geçerli ise True
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return 'symbol' in info or 'shortName' in info
        except:
            return False
    
    def get_company_info(self, symbol: str) -> Optional[Dict]:
        """
        Şirket bilgilerini çeker
        
        Args:
            symbol: Hisse kodu
            
        Returns:
            Dict: Şirket bilgileri
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            company_info = {
                'name': info.get('longName', 'Bilinmiyor'),
                'sector': info.get('sector', 'Bilinmiyor'),
                'industry': info.get('industry', 'Bilinmiyor'),
                'employees': info.get('fullTimeEmployees', 0),
                'website': info.get('website', ''),
                'summary': info.get('longBusinessSummary', ''),
                'market_cap': info.get('marketCap', 0),
                'enterprise_value': info.get('enterpriseValue', 0),
                'pe_ratio': info.get('forwardPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'dividend_yield': info.get('dividendYield', 0)
            }
            
            return company_info
            
        except Exception as e:
            print(f"Şirket bilgisi hatası {symbol}: {str(e)}")
            return None 