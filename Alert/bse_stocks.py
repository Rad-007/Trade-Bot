import requests

def get_all_stock_symbols():
    api_key = '5F1ESCFPKC1B4S6P'
    url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}'
    
    response = requests.get(url)
    data = response.json()
    
    stock_symbols = []
    
    if 'data' in data:
        for entry in data['data']:
            if 'symbol' in entry:
                symbol = entry['symbol']
                stock_symbols.append(symbol)
    
    return stock_symbols

def filter_bse_symbols(symbols):
    bse_symbols = [symbol for symbol in symbols if ".BSE" in symbol]
    return bse_symbols

def main():
    all_symbols = get_all_stock_symbols()
    bse_symbols = filter_bse_symbols(all_symbols)
    
    for symbol in bse_symbols:
        print(symbol)

if __name__ == "__main__":
    main()
