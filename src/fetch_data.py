"""
Fetch historical stock data from Yahoo Finance.

Usage:
    python src/fetch_data.py --ticker AAPL --start 2020-01-01 --end 2024-12-31
"""
import argparse
import os
import yfinance as yf
import pandas as pd

DEFAULT_TICKER = "AAPL"
DEFAULT_START  = "2020-01-01"
DEFAULT_END    = "2024-12-31"
DATA_DIR       = "data"


def fetch(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download adjusted OHLCV data for a ticker between two dates."""
    print(f"Fetching {ticker} from {start} to {end}...")
    df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"No data returned for {ticker}. Check ticker symbol / dates.")
    # Flatten MultiIndex columns if present (newer yfinance versions)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.index.name = "Date"
    return df


def save(df: pd.DataFrame, ticker: str) -> str:
    """Save dataframe as CSV under data/ and return filepath."""
    os.makedirs(DATA_DIR, exist_ok=True)
    path = os.path.join(
        DATA_DIR,
        f"{ticker}_{df.index.min().date()}_{df.index.max().date()}.csv",
    )
    df.to_csv(path)
    print(f"Saved -> {path}")
    return path


def main():
    p = argparse.ArgumentParser(description="Fetch stock price data from Yahoo Finance.")
    p.add_argument("--ticker", default=DEFAULT_TICKER, help="Ticker symbol (e.g. AAPL)")
    p.add_argument("--start",  default=DEFAULT_START,  help="Start date YYYY-MM-DD")
    p.add_argument("--end",    default=DEFAULT_END,    help="End date YYYY-MM-DD")
    args = p.parse_args()

    df = fetch(args.ticker, args.start, args.end)
    save(df, args.ticker)
    print("\nPreview (last 5 rows):")
    print(df.tail())


if __name__ == "__main__":
    main()