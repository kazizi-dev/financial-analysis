import config
from brokerage import Brokerage

broker = Brokerage()

response = broker.get_historical_data("AAPL", config.START, config.END, 5)

if response.status_code == 200:
 	close = [candle['close'] for candle in response.json()['candles']]
 	pprint(close)
else:
 	print("Response code: ", response.status_code)



#for i in range(8000, 9999):
#	response = broker.get_historical_data(i, config.START, config.END, 1)
#
#	if response.status_code == 200:
#		close = [candle['close'] for candle in response.json()['candles']]
#		if len(close) > 0:
#			if close[0] >= 26.00 and close[0] < 27.00:
#				print('--->', i, close)
#			else:
#				print(i, close)
#
#	else:
#		print("Response code: ", response.status_code)
