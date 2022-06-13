import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd


tickers = ["SQQQ"]

def get_closing_price(tickers, time_period="ytd"):
    response = yf.Tickers(" ".join(tickers))
    
    df = pd.DataFrame
    for ticker, ticker_obj in response.tickers.items():
        # grab date and the closing ticker price
        df = ticker_obj.history(period=time_period)
        df = df[["Close"]]
        df.reset_index(level=0, inplace=True)
        df.columns = ["date", "close"]

    return df


def get_macd_and_signal(df):
    data = dict()

    # calculate MACD
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    data['macd'] = exp1 - exp2

    # calculate signal
    data['signal'] = data['macd'].ewm(span=9, adjust=False).mean()

    return data


def plot_macd_chart(df, ticker, macd, signal):
    plt.plot(df['date'], macd, label=f"{ticker} MACD", color="blue", linewidth=0.75)
    plt.plot(df['date'], signal, label="Signal Line", color="darkorange", linewidth=1)
    plt.legend(loc="lower left")
    plt.show()


df = get_closing_price(tickers, "ytd")
data = get_macd_and_signal(df)
plot_macd_chart(df, tickers[0], data['macd'], data['signal'])


# TODO: find crossed lines
