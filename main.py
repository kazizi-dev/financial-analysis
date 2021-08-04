import yfinance as yf
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
from itertools import groupby
import os

"""
    graph the data from two columns to understand market behaviour.
"""
def graph_x_and_y_cols(df, option_date, cols, type):
    name = 'calls' if 'calls' in type else 'puts'
    plt.plot(df[cols[0]], df[cols[1]])
    plt.title(f'[{name}] expiring on {option_date}')
    plt.xlabel(cols[0])
    plt.ylabel(cols[1])
    plt.savefig(f'{option_date}-{type}.png')
    plt.close()


"""
    calculate volume for different strike price range.
"""
def calculate_vol_for_strike_range(df, BREAKDOWN_RANGE):
    range = dict()
    for (key, group) in groupby(df['strike'], key=lambda x: x // BREAKDOWN_RANGE):
        volume = 0
        for val in group:
            volume += df[df['strike'] == val]['volume'].sum()
        range[key * BREAKDOWN_RANGE] = int(volume)

    return range
        

"""
    calls other functions to perform operations.
"""
def option_analysis(option_date, opt, TICKER_NAME, COLUMNS):
    calls = opt.calls
    calls = calls[COLUMNS]
    graph_x_and_y_cols(calls, option_date, ['strike', 'impliedVolatility'], 'calls-iv')
    graph_x_and_y_cols(calls, option_date, ['strike', 'volume'], 'calls-volume')

    puts = opt.puts
    puts = puts[COLUMNS]
    graph_x_and_y_cols(puts, option_date, ['strike', 'impliedVolatility'], 'puts-iv')
    graph_x_and_y_cols(puts, option_date, ['strike', 'volume'], 'puts-volume')

    return {
        'ticker': TICKER_NAME,
        'put-call-vol-ratio': (puts['volume'].sum()/calls['volume'].sum()).round(2),
        'call-volume-range': calculate_vol_for_strike_range(calls, 100),
        'put-volume-range': calculate_vol_for_strike_range(puts, 100)
    }


if __name__ == '__main__':
    COLUMNS = ['strike', 'bid', 'ask', 'volume', 'openInterest','impliedVolatility']
    TICKER_NAME = 'TSLA'

    stock = yf.Ticker(TICKER_NAME)
    option_date = stock.options[0]
    opt = stock.option_chain(option_date)
    
    output = option_analysis(option_date, opt, TICKER_NAME, COLUMNS)
    pprint(output)