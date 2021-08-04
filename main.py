import yfinance as yf
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
from itertools import groupby

"""
    helps to understand the market behaviour from volume as strike price changes.
"""
def graph_x_and_y_cols(df, option_date, cols, type):
    name = 'calls' if 'calls' in type else 'puts'
    plt.plot(df[cols[0]], df[cols[1]])
    plt.title(f'[{name}] expiring on {option_date}')
    plt.xlabel(cols[0])
    plt.ylabel(cols[1])
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
    calls other functions to perform operations.
"""
def option_analysis(TICKER_NAME, COLUMNS):
    stock = yf.Ticker(TICKER_NAME)
    option_date = stock.options[0]
    opt = stock.option_chain(option_date)
    calls = opt.calls
    calls = calls[COLUMNS]

    puts = opt.puts
    puts = puts[COLUMNS]

    
    # the columns to use for graphs
    cols = ['strike', 'impliedVolatility']
    graph_x_and_y_cols(calls, option_date, cols, 'calls-iv')
    graph_x_and_y_cols(puts, option_date, cols, 'puts-iv')

    cols = ['strike', 'volume']
    graph_x_and_y_cols(calls, option_date, cols, 'calls-volume')
    graph_x_and_y_cols(puts, option_date, cols, 'puts-volume')

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
