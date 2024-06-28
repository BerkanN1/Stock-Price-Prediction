import requests
import csv
from datetime import datetime

def get_financial_data(api_key, params):
    url = 'https://www.alphavantage.co/query'
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Hata alındı: {response.status_code}")
        return None

def get_forex_and_gold_tsla_prices_to_csv(api_key, output_file, start_date):
    params_eur_usd = {
        'function': 'FX_DAILY',
        'from_symbol': 'EUR',
        'to_symbol': 'USD',
        'apikey': api_key,
        'outputsize': 'full'
    }

    params_gold_usd = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': 'GLD',
        'apikey': api_key,
        'outputsize': 'full'
    }
    
    params_tsla = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': 'TSLA',
        'apikey': api_key,
        'outputsize': 'full'  # Tüm verileri çekmek için outputsize: 'full' ekleniyor
    }

    try:
        # EUR/USD döviz kuru verilerini çekme
        data_eur_usd = get_financial_data(api_key, params_eur_usd)
        if not data_eur_usd or 'Time Series FX (Daily)' not in data_eur_usd:
            print("EUR/USD verileri alınamadı.")
            return

        # Altın Ons (XAU/USD) fiyatlarını çekme
        data_gold_usd = get_financial_data(api_key, params_gold_usd)
        if not data_gold_usd or 'Time Series (Daily)' not in data_gold_usd:
            print("Altın (XAU/USD) verileri alınamadı.")
            return

        # Tesla (TSLA) hisse senedi fiyatlarını çekme
        data_tsla = get_financial_data(api_key, params_tsla)
        if not data_tsla or 'Time Series (Daily)' not in data_tsla:
            print("Tesla (TSLA) verileri alınamadı.")
            return

        # Ortak tarihleri bulma
        eur_usd_dates = set(data_eur_usd['Time Series FX (Daily)'].keys())
        gold_usd_dates = set(data_gold_usd['Time Series (Daily)'].keys())
        tsla_dates = set(data_tsla['Time Series (Daily)'].keys())
        common_dates = eur_usd_dates.intersection(gold_usd_dates).intersection(tsla_dates)

        # CSV dosyasını yazma işlemi
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Date', 'EUR/USD Close', 'Gold USD Close', 'TSLA Open', 'TSLA High', 'TSLA Low', 'TSLA Close', 'TSLA Volume'])

            # Ortak tarihler üzerinden verileri yazma
            for date in sorted(common_dates):
                eur_usd_close = data_eur_usd['Time Series FX (Daily)'][date]['4. close']
                gold_usd_close = data_gold_usd['Time Series (Daily)'][date]['4. close']
                tsla_values = data_tsla['Time Series (Daily)'][date]
                tsla_open = tsla_values['1. open']
                tsla_high = tsla_values['2. high']
                tsla_low = tsla_values['3. low']
                tsla_close = tsla_values['4. close']
                tsla_volume = tsla_values['5. volume']
                
                writer.writerow([date, eur_usd_close, gold_usd_close, tsla_open, tsla_high, tsla_low, tsla_close, tsla_volume])

        print(f"Veriler başarıyla '{output_file}' dosyasına kaydedildi.")

    except requests.RequestException as e:
        print(f"Hata oluştu: {e}")

# API anahtarınız, CSV dosyası adı ve başlangıç tarihiyle fonksiyonu çağırın
api_key = ''  # Buraya kendi AlphaVantage API anahtarınızı ekleyin
output_file = 'data.csv'  # Kaydedilecek CSV dosyasının adı
start_date = '2010-06-29'  # İstenen başlangıç tarihi
get_forex_and_gold_tsla_prices_to_csv(api_key, output_file, start_date)
