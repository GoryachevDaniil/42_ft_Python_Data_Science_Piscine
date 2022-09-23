#!/usr/local/bin/python3
import sys

def data():
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

def all_stocks():
    COMPANIES, STOCKS = data()
    words = sys.argv[1].replace(' ', '').split(',')
    for word in words:
        if word.upper() in STOCKS:
            print(f'{word.upper()} is a ticker symbol for {get_key(COMPANIES, word.upper())}')
        elif word.capitalize() in COMPANIES:
            print(f'{word.capitalize()} stock price is {STOCKS[COMPANIES[word.capitalize()]]}')
        elif not word:
            return (print(''))
        else:
            print(f'{word} is an unknown company or an unknown ticker symbol')

def main():
    if len(sys.argv) == 2:
        all_stocks()
    
if __name__ == '__main__':
    main()