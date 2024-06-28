import yfinance as yf
import pandas as pd

def get_stock_data(symbol, start_date, end_date):

    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

def get_currency_data(symbol, start_date, end_date):

    currency_data = yf.download(symbol, start=start_date, end=end_date)
    return currency_data

def save_to_csv(dataframe, filename):

    dataframe.to_csv(filename)

# TSLA hisse senedi verilerini alıp DataFrame'e dönüştürme
tsla_data = get_stock_data("TSLA", "2010-06-29", "2024-04-27")

# Euro/Dolar endeksi verilerini alıp DataFrame'e dönüştürme
eurusd_data = get_currency_data("EURUSD=X", "2010-06-29", "2024-04-27")

# Altın ons fiyatı verilerini alıp DataFrame'e dönüştürme
gold_data = get_stock_data("GC=F", "2010-06-29", "2024-04-27")

# Verileri birleştirme
merged_data = pd.concat([eurusd_data['Close'], gold_data['Close'], tsla_data[['Open', 'High', 'Low', 'Close', 'Volume']]], axis=1)
merged_data.columns = ['EUR/USD Close', 'Gold USD Close', 'TSLA Open', 'TSLA High', 'TSLA Low', 'TSLA Close', 'TSLA Volume']

# Birleştirilmiş verileri CSV dosyasına kaydetme
save_to_csv(merged_data, "data.csv")
