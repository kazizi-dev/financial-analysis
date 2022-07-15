import config
from brokerage import Brokerage
from pprint import pprint

TICKERS = {
    'TSLA' : 38526,
    'AAPL' : 8049,
    'MSFT' : 27426,
    'NVDA' : 29814,
    'AMD' : 6770,
    'IBM' : 23364,
    'AMZN' : 7410,
    'QQQ' : 21806473,
    'SPY' : 34987,
    'VIX.IN' : 11367,
}

INTERVALS = {
    '1m': 'OneMinute',
	'3m': 'ThreeMinutes',
    '5m': 'FiveMinutes',
    '15m': 'FifteenMinutes',
	'30m': 'HalfHour',
	'1h': 'OneHour',
	'2h': 'TwoHours',
	'4h': 'FourHours',
	'1d': 'OneDay'
}


START = "2022-07-13T00:00:00-05:00"
END = "2022-07-14T23:59:59-05:00"


def print_ticker_info(tickers: list):
	for ticker in tickers:
		response = Brokerage().get_ticker_info_using_symbol(ticker)
		if response.status_code == 200:
			for entry in response.json()['symbols']:
				if entry['symbol'] == ticker and entry['isQuotable'] == True:
					print(f"'{ticker}' : {entry['symbolId']},")
		else:
			print("Response code: ", response.status_code)


def print_data(ticker: str):
	response = Brokerage().get_historical_data(ticker, START, END, INTERVALS['15m'])
	for candle in response.json()['candles']:
 		pprint(candle)


if __name__ == "__main__":
	tickers = [
		'TSLA', 'AAPL', 'MSFT', 'NVDA', 'AMD', 
		'IBM', 'AMZN', 'QQQ', 'SPY', 'VIX.IN',
		'GOOG'
	]

	print_ticker_info(tickers)
	# print_data(TICKERS['TSLA'])