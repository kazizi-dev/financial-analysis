import yfinance as yf
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
from itertools import groupby

"""
    helps to understand the market behaviour from volume as strike price changes.
"""
def graph_strike_over_volume(df, option_date, type):
    plt.plot(df['strike'], df['volume'])
    plt.title(f'[{type}] -> {option_date}')
    plt.xlabel('strike')
    plt.ylabel('volume')
    plt.savefig(f'{type}.png')
    plt.close()

def calculate_vol_for_strike_range(df):
    range = dict()

    for (key, group) in groupby(df['strike'], key=lambda x: x // 100):
        volume = 0
        for val in group:
            volume += df[df['strike'] == val]['volume'].sum()
        
        range[key*100] = int(volume)

    return range
        

"""
    calls other functions to make graphs.
"""
def option_analysis(TICKER_NAME, COLUMNS):
    stock = yf.Ticker(TICKER_NAME)
    option_date = stock.options[0]
    opt = stock.option_chain(option_date)

    calls = opt.calls
    calls = calls[COLUMNS]
    graph_strike_over_volume(calls, option_date, 'calls')

    puts = opt.puts
    puts = puts[COLUMNS]
    graph_strike_over_volume(puts, option_date, 'puts')

    return {
        'ticker': TICKER_NAME,
        'put-call-vol-ratio': (puts['volume'].sum()/calls['volume'].sum()).round(2),
        'call-volume-range': calculate_vol_for_strike_range(calls),
        'put-volume-range': calculate_vol_for_strike_range(puts)
    }


if __name__ == '__main__':
    COLUMNS = ['strike', 'bid', 'ask', 'volume', 'openInterest','impliedVolatility']
    TICKER_NAME = 'TSLA'
    
    pprint(option_analysis(TICKER_NAME, COLUMNS))




# thoughts:

# sns.distplot(calls['ask'], label = 'impliedVolatility')
# plt.plot(calls['strike'], calls['volume'])
# # g = sns.jointplot("strike", "ask", calls, kind='hex')
# # sns.pairplot(calls)
# plt.title(f'{option_date}')
# plt.xlabel('strike')
# plt.ylabel('volume')
# plt.savefig(f'calls.png')
# plt.close()
