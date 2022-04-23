import requests
import csv

CSV_FILENAME = 'result.csv'
CSV_HEADER_LIST = ['stock_symbol', 'percentage_change', 'current_price', 'last_close_price']

API_URL = 'https://finnhub.io/api/v1/'
API_KEY = 'c9hsnriad3idasnd99sg'


def get_latest_price(symbol: str):
    try:
        r = requests.get(f"{API_URL}/quote", params={'token': API_KEY, 'symbol': symbol})
        data = r.json()
        return {
            'stock_symbol': symbol,
            'percentage_change': data['dp'],
            'current_price': data['c'],
            'last_close_price': data['pc']
        }
    except Exception as e:
        print('Exception:', e)
        return False


def get_most_volatile_stock(old_most_volatile_stock:dict, symbol_data:dict):
    new_most_volatile_stock = old_most_volatile_stock
    if old_most_volatile_stock['percentage_change'] < symbol_data['percentage_change']:
        new_most_volatile_stock = symbol_data
    return new_most_volatile_stock


def save_most_volatile_stock(most_volatile_stock:dict):
    most_volatile_stock_values = list(most_volatile_stock.values())
    try:
        with open(CSV_FILENAME, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER_LIST)
            writer.writerow(most_volatile_stock_values)
    except Exception as e:
        print('Exception:', e)


def start_challenge(symbol_list:list):
    most_volatile_stock = None
    for symbol in symbol_list:
        symbol_data = get_latest_price(symbol)
        if most_volatile_stock is None:
            most_volatile_stock = symbol_data
        else:
            most_volatile_stock = get_most_volatile_stock(most_volatile_stock, symbol_data)
    if most_volatile_stock is not None:
        save_most_volatile_stock(most_volatile_stock)
        print('Most Volatile Stock saved.')
    else:
        print('Could not get the most volatile stock as of the moment')


if __name__ == "__main__":
    print('Starting Challenge')
    start_challenge(['AAPL', 'AMZN', 'NFLX', 'FB', 'GOOG'])
    print('End Challenge')