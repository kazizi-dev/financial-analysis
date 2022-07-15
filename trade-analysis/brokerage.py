import requests
import config


class Brokerage:
	"""
	This class contains methods that can retrieve historical data
	from an online brokerage.
	"""

	def __init__(self):
		pass

	# retrieve historical candle information
	def get_historical_data(self, id, start_time: str, end_time: str, interval: int):
		URL = f"{config.API_SERVER}/v1/markets/candles/{id}?startTime={start_time}&endTime={end_time}&interval={interval}"
		response = requests.get(
			URL,
			headers= {
				'content-type': 'application/json', 
				'Authorization': config.TOKEN
			}
		)

		return response

	
	# retrieve ticker id based on name
	def get_ticker_info_using_symbol(self, ticker: str):
		URL = f"{config.API_SERVER}/v1/symbols/search?prefix={ticker}"
		response = requests.get(
			URL,
			headers= {
				'content-type': 'application/json', 
				'Authorization': config.TOKEN
			}
		)

		return response


	# retrieve information about the ticker using its id
	def get_ticker_info_using_id(self, id: int):
		URL = f"{config.API_SERVER}/v1/symbols/{id}"
		response = requests.get(
			URL,
			headers= {
				'content-type': 'application/json', 
				'Authorization': config.TOKEN
			}
		)

		return response
