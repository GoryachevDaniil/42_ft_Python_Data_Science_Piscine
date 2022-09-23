#!/usr/local/bin/python3

def data() -> list:
    country_codes_dict = {
        'Russia': '25',
        'France': '132',
        'Germany': '132',
        'Spain': '178',
        'Italy': '162',
        'Portugal': '17',
        'Finland': '3',
        'Hungary': '2',
        'The Netherlands': '28',
        'The USA': '610',
        'The United Kingdom': '95',
        'China': '83',
        'Iran': '76',
        'Turkey': '65',
        'Belgium': '34',
        'Canada': '28',
        'Switzerland': '26',
        'Brazil': '25',
        'Austria': '14',
        'Israel': '12'
    }
    return country_codes_dict

def dict_sorted():
    dt = {k: int(v) for k, v in data().items()}
    dt = dict(sorted(dt.items(), key=lambda item: item[1], reverse=True))
    for k, v in dt.items():
        print(f'{k}')        

if __name__ == '__main__':
    dict_sorted()