import yfinance as yf
from pprint import pprint
# import pandas as pd
import matplotlib.pyplot as plt
# import seaborn as sns
from itertools import groupby
import os
import json


"""
    graph the data from two columns to understand market behaviour.
"""
def graph_x_and_y_cols(df, OPTION_DATE, COLS, TYPE, PATH, TICKER):
    name = 'calls' if 'calls' in TYPE else 'puts'
    plt.plot(df[COLS[0]], df[COLS[1]])
    plt.title(f'{TICKER} {name} expiring on {OPTION_DATE}')
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
    calculate the put to call ratio for many option dates.
"""
def get_put_to_call_ratio_of_option_chains(dates, COLUMNS):
    outer = dict()
    inner = dict()

    for date in dates:
        opt = stock.option_chain(date)

        calls = opt.calls
        calls = calls[COLUMNS]

        puts = opt.puts
        puts = puts[COLUMNS]

        outer[date] = {
            'put-to-call-ratio' : (puts['volume'].sum()/calls['volume'].sum()).round(3),
            'put-volume' : puts['volume'].sum(),
            'calls-volume': calls['volume'].sum()
        }

    return outer

"""
    calls other functions to perform operations.
"""
def option_analysis(option_dates, opt, TICKER, COLUMNS, PATH):
    calls = opt.calls
    calls = calls[COLUMNS]
    graph_x_and_y_cols(calls, option_dates[0], ['strike', 'impliedVolatility'], 'calls-iv', PATH, TICKER)
    graph_x_and_y_cols(calls, option_dates[0], ['strike', 'volume'], 'calls-volume', PATH, TICKER)

    puts = opt.puts
    puts = puts[COLUMNS]
    graph_x_and_y_cols(puts, option_dates[0], ['strike', 'impliedVolatility'], 'puts-iv', PATH, TICKER)
    graph_x_and_y_cols(puts, option_dates[0], ['strike', 'volume'], 'puts-volume', PATH, TICKER)

    return {
        'ticker': TICKER,
        'put-call-vol-ratio': (puts['volume'].sum()/calls['volume'].sum()).round(2),
        'call-volume-range': calculate_vol_for_strike_range(calls, 50),
        'put-volume-range': calculate_vol_for_strike_range(puts, 50),
        'pc-vol-ratio(all)': get_put_to_call_ratio_of_option_chains(option_dates, COLUMNS)
    }


if __name__ == '__main__':
    COLUMNS = ['strike', 'bid', 'ask', 'volume', 'openInterest','impliedVolatility']
    TICKERS = ['QQQ']

    for ticker in TICKERS:
        stock = yf.Ticker(ticker)

        option_dates = stock.options
        opt = stock.option_chain(option_dates[0])

        # create directory for graph data
        PATH = f'./graphs/{ticker}'
        if(not os.path.exists(PATH)):
            os.mkdir(PATH)
        PATH = PATH + '/' + option_dates[0]
        if(not os.path.exists(PATH)):
            os.mkdir(PATH)
        
        data = option_analysis(option_dates, opt, ticker, COLUMNS, PATH)
        pprint(data)

        # save snapshot from option analysis output 
        PATH = PATH + '/' + 'data.json'
        with open(PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)