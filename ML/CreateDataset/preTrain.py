import pandas as pd
import talib as ta

# CSV dosyasını okuma
df = pd.read_csv('data.csv')

# Tarih sütununu datetime'a dönüştürme
df['Date'] = pd.to_datetime(df['Date'])

# Verileri tarihe göre sıralama (en eski tarihten en yeni tarihe)
df = df.sort_values(by='Date')

# Eksik tarihleri içeren tam tarih aralığıyla veri çerçevesini yeniden oluşturma
min_date = df['Date'].min()
max_date = df['Date'].max()
all_dates = pd.date_range(start=min_date, end=max_date)
df = df.set_index('Date').reindex(all_dates).rename_axis('Date').reset_index()

# Eksik değerleri bir önceki günün değerleriyle doldurma
df = df.fillna(method='ffill')

# Günlük kapanış fiyatlarıyla EMA hesaplama (örnek olarak TSLA Close fiyatları üzerinden)
df['EMA_25'] = ta.EMA(df['TSLA Close'], timeperiod=25)
df['EMA_50'] = ta.EMA(df['TSLA Close'], timeperiod=50)
df['EMA_100'] = ta.EMA(df['TSLA Close'], timeperiod=100)
df['EMA_200'] = ta.EMA(df['TSLA Close'], timeperiod=200)
df['EMA_300'] = ta.EMA(df['TSLA Close'], timeperiod=300)

# Bollinger bantlarını günlük kapanış fiyatlarıyla hesaplama (örnek olarak TSLA Close fiyatları üzerinden)
n = 20  # Bant genişliği için kullanılacak dönem sayısı
df['Bollinger_up'], df['Bollinger_mid'], df['Bollinger_low'] = ta.BBANDS(df['TSLA Close'], timeperiod=n, nbdevup=2, nbdevdn=2)

# RSI (Relative Strength Index) hesaplama (örnek olarak TSLA Close fiyatları üzerinden)
df['RSI'] = ta.RSI(df['TSLA Close'], timeperiod=14)

# MACD (Moving Average Convergence Divergence) hesaplama (örnek olarak TSLA Close fiyatları üzerinden)
macd, macdsignal, macdhist = ta.MACD(df['TSLA Close'], fastperiod=12, slowperiod=26, signalperiod=9)
df['MACD'] = macd
df['MACD_Signal'] = macdsignal

# USD/EUR (EUR/USD) ve Altın fiyatları (Gold USD Close) verilerini kullanarak analizler yapma
# Örnek olarak, CSV dosyasındaki USD/EUR ve Altın fiyatları sütunlarını kullanabiliriz

# USD/EUR (EUR/USD) ve Altın fiyatları (Gold USD Close) sütunlarını kullanarak analizler yapma
df['EUR/USD Close'] = df['EUR/USD Close']  # EUR/USD kapanış fiyatları
df['Gold USD Close'] = df['Gold USD Close']  # Altın USD kapanış fiyatları

# Verileri tarihe göre sıralama (en yeni tarihten en eski tarihe)
df = df.sort_values(by='Date', ascending=False)

# Sonuçları yeni bir CSV dosyasına yazma
df.to_csv('finalData.csv', index=False)

print("EMA'lar, Bollinger bantları, RSI, MACD ve dış veriler (EUR/USD Close, Gold USD Close) günlük verilerle başarıyla hesaplandı ve finalData.csv dosyasına kaydedildi.")
