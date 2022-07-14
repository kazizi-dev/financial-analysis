import requests
import config
from requests.auth import HTTPBasicAuth
from pprint import pprint



class Brokerage:
	"""
	This class contains methods that can retrieve historical data
	from an online brokerage.
	"""

	def __init__(self):
		pass

	# retrieve historical candle information
	def get_historical_data(self, ticker: str, start_time: str, end_time: str, timeframe: int):
		id = config.TICKERS[ticker]
		interval = config.INTERVALS[timeframe]
		URL = f"{config.API_SERVER}/v1/markets/candles/{id}?startTime={start_time}&endTime={end_time}&interval={interval}"
		response = requests.get(
			URL,
			headers= {
				'content-type': 'application/json', 
				'Authorization': config.TOKEN
			}
		)

		return response


	# retrieve information about the ticker using its id
	def get_ticker_info(self, id):
		URL = f"{config.API_SERVER}/v1/symbols/{id}"
		response = requests.get(
			URL,
			headers= {
				'content-type': 'application/json', 
				'Authorization': config.TOKEN
			}
		)

		return response



broker = Brokerage()
response = broker.get_historical_data("AAPL", config.START, config.END, 5)

if response.status_code == 200:
	close = [candle['close'] for candle in response.json()['candles']]
	pprint(close)
else:
	print("Response code: ", response.status_code)
