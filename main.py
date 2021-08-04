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
def graph_x_and_y_cols(df, OPTION_DATE, COLS, TYPE, PATH):
    name = 'calls' if 'calls' in TYPE else 'puts'
    plt.plot(df[COLS[0]], df[COLS[1]])
    plt.title(f'[{name}] expiring on {OPTION_DATE}')
    plt.xlabel(COLS[0])
    plt.ylabel(COLS[1])

    plt.savefig(PATH + '/' + f'{TYPE}.png')
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
def option_analysis(option_date, opt, TICKER_NAME, COLUMNS, PATH):
    calls = opt.calls
    calls = calls[COLUMNS]
    graph_x_and_y_cols(calls, option_date, ['strike', 'impliedVolatility'], 'calls-iv', PATH)
    graph_x_and_y_cols(calls, option_date, ['strike', 'volume'], 'calls-volume', PATH)

    puts = opt.puts
    puts = puts[COLUMNS]
    graph_x_and_y_cols(puts, option_date, ['strike', 'impliedVolatility'], 'puts-iv', PATH)
    graph_x_and_y_cols(puts, option_date, ['strike', 'volume'], 'puts-volume', PATH)

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

    # create directory for graph data
    PATH = f'./graphs/{option_date}'
    if(not os.path.exists(PATH)):
        os.mkdir(PATH)
    
    output = option_analysis(option_date, opt, TICKER_NAME, COLUMNS, PATH)
    pprint(output)