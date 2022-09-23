#!/usr/local/bin/python3
import sys

def data() -> tuple:
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }
    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    return COMPANIES, STOCKS

def get_key(my_dict, val):
    for key, value in my_dict.items():
         if val == value:
             return key

def ticker_symbols(ticker_symbol: str) -> None:
    s = sys.argv[1].upper()
    COMPANIES, STOCKS = data()
    if s in STOCKS:
        print(get_key(COMPANIES, s), STOCKS[s])
    else:
        print("Unknown ticker")

def main():
    if len(sys.argv) == 2:
        ticker_symbols(sys.argv[1])

if __name__ == '__main__':
    main()