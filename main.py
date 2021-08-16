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
    get user inputs on what information to display or save.
"""
def get_user_input():
    option_dates = []

    print("Enter expiry dates (type 'done' when done): ")
    user_input = ''
    while user_input != 'done':
        user_input = input('> ')
        
        if len(user_input) == 0:
            option_dates.append('all')
            break
        elif user_input != 'done':
            option_dates.append(user_input)
        
    print(option_dates)


    print("Enter tickers (type 'done' when done): ")
    tickers = []
    user_input = ''
    while user_input != 'done':
        user_input = input("> ")

        if len(user_input) == 0 and 'SPY' not in tickers:
            tickers.append('SPY')
        elif user_input != 'done':
            option_dates.append(user_input)
        
    print(tickers)

    user_input = int(input("Enter volume range (numbers only): "))
    volume_range = user_input if user_input > 0 else 10

    print(volume_range)

    return option_dates, tickers, volume_range


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
        'put-vol': puts['volume'].sum(),
        'call-vol': calls['volume'].sum(),
        'put-call-vol-ratio': (puts['volume'].sum()/calls['volume'].sum()).round(2),
        # 'call-vol-range': calculate_vol_for_strike_range(calls, VOLUME_RANGE),
        # 'put-vol-range': calculate_vol_for_strike_range(puts, VOLUME_RANGE)
    }


if __name__ == '__main__':
    COLUMNS = ['strike', 'bid', 'ask', 'volume', 'openInterest','impliedVolatility']


    option_dates, tickers, volume_range = get_user_input()

    for ticker in tickers:
        print(f"==================================================================")
        print(f"                             {ticker}                             ")
        print(f"==================================================================")

        stock = yf.Ticker(ticker)

        if 'all' in option_dates:
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
            
            data = option_analysis(date, opt, ticker, COLUMNS, PATH, volume_range)
            # pprint(data)
            print(data)

            # # save snapshot from option analysis output 
            # PATH = PATH + '/' + 'data.json'
            # with open(PATH, 'w', encoding='utf-8') as f:
            #     json.dump(data, f, ensure_ascii=False, indent=4)