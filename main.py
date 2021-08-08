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
    calls other functions to perform operations.
"""
def option_analysis(option_date, opt, TICKER, COLUMNS, PATH, VOLUME_RANGE):
    calls = opt.calls
    calls = calls[COLUMNS]
    graph_x_and_y_cols(calls, option_date, ['strike', 'impliedVolatility'], 'calls-iv', PATH, TICKER)
    graph_x_and_y_cols(calls, option_date, ['strike', 'volume'], 'calls-volume', PATH, TICKER)

    puts = opt.puts
    puts = puts[COLUMNS]
    graph_x_and_y_cols(puts, option_date, ['strike', 'impliedVolatility'], 'puts-iv', PATH, TICKER)
    graph_x_and_y_cols(puts, option_date, ['strike', 'volume'], 'puts-volume', PATH, TICKER)

    return {
        'ticker': TICKER,
        'expiry-date': option_date,
        'put-call-vol-ratio': (puts['volume'].sum()/calls['volume'].sum()).round(2),
        'call-vol-range': calculate_vol_for_strike_range(calls, VOLUME_RANGE),
        'put-vol-range': calculate_vol_for_strike_range(puts, VOLUME_RANGE)
    }


if __name__ == '__main__':
    COLUMNS = ['strike', 'bid', 'ask', 'volume', 'openInterest','impliedVolatility']


    ######################### You can modify these #########################
    TICKERS = ['QQQ', 'SPY']        # add '' around it followed by a comma     
    VOLUME_RANGE = 100
    ########################################################################

    for ticker in TICKERS:
        print(f"==================================================================")
        print(f"                             {ticker}                             ")
        print(f"==================================================================")

        stock = yf.Ticker(ticker)
        option_dates = stock.options

        for date in option_dates:
            opt = stock.option_chain(date)

            # create directory for graph data
            PATH = f'./graphs/{ticker}'
            if(not os.path.exists(PATH)):
                os.mkdir(PATH)
            PATH = PATH + '/' + date
            if(not os.path.exists(PATH)):
                os.mkdir(PATH)
            
            data = option_analysis(date, opt, ticker, COLUMNS, PATH, VOLUME_RANGE)
            pprint(data)

            # save snapshot from option analysis output 
            PATH = PATH + '/' + 'data.json'
            with open(PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)