#######################################################################
# This script is "Economically-sensible, statistically-quantifiable slow-converging inefficiencies"
# From Twitter thread: https://twitter.com/therobotjames/status/1359349194230693889
#######################################################################

import pandas as pd
import yfinance as yf


def fetch_data(ticker, start_date, end_date):
    """Ahoy! Fetch the treasure map (historical data) for a given ship's flag (ticker)."""
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


def calculate_momentum(data, window=14):
    """Calculate the wind in our sails (momentum) for the given sea chart (data)."""
    data['Momentum'] = data['Close'] - data['Close'].shift(window)
    return data


def calculate_moving_average(data, window=14):
    """Find the average course we've sailed over a given number of days."""
    data['MA'] = data['Close'].rolling(window=window).mean()
    return data


def identify_inefficiencies(data, threshold=0.05):
    """Spot the islands (inefficiencies) where we can find buried treasure or danger."""
    mean_momentum = data['Momentum'].mean()
    deviations = data['Momentum'] - mean_momentum

    # Mark the spots on the map where treasure be buried or danger lurks
    data['Cheap'] = (deviations < -threshold) & (data['Close'] < data['MA'])
    data['Expensive'] = (deviations > threshold) & (data['Close'] > data['MA'])

    return data


def main():
    ticker = "AAPL"  # The ship's flag we be trackin'
    start_date = "2020-01-01"
    end_date = "2023-01-01"

    data = fetch_data(ticker, start_date, end_date)
    data = calculate_momentum(data)
    data = calculate_moving_average(data)
    data = identify_inefficiencies(data)

    cheap_dates = data[data['Cheap']].index
    expensive_dates = data[data['Expensive']].index

    print(f"Dates when {ticker} be lookin' like a sunken ship (too cheap):", cheap_dates)
    print(f"Dates when {ticker} be lookin' like a king's ransom (too expensive):", expensive_dates)


if __name__ == "__main__":
    main()
