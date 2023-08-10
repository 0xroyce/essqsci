#######################################################################
# This script is "Economically-sensible, statistically-quantifiable slow-converging inefficiencies"
# From Twitter thread: https://twitter.com/therobotjames/status/1359349194230693889
#######################################################################

import pandas as pd
import yfinance as yf

def fetch_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def calculate_momentum(data, window=14):
    data['Momentum'] = data['Close'] - data['Close'].shift(window)
    return data

def identify_inefficiencies(data, threshold=0.05):
    mean_momentum = data['Momentum'].mean()
    deviations = data['Momentum'] - mean_momentum

    data['Cheap'] = deviations < -threshold
    data['Expensive'] = deviations > threshold

    return data


def main():
    ticker = "AAPL"  # Change the ticker
    start_date = "2020-01-01"
    end_date = "2023-01-01"

    data = fetch_data(ticker, start_date, end_date)
    data = calculate_momentum(data)
    data = identify_inefficiencies(data)

    cheap_dates = data[data['Cheap']].index
    expensive_dates = data[data['Expensive']].index

    print(f"Dates when {ticker} was trading too cheap:", cheap_dates)
    print(f"Dates when {ticker} was trading too expensive:", expensive_dates)


if __name__ == "__main__":
    main()