import yfinance as yf
import pandas as pd

def load_price_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date, group_by="ticker")

    # If MultiIndex columns exist, extract the relevant ticker data
    if isinstance(df.columns, pd.MultiIndex):
        df = df[ticker]

    df = df.copy()
    df.reset_index(inplace=True)  # Promote index to 'Date'
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df = df[['Date', 'High', 'Low', 'Close']].dropna()

    return df