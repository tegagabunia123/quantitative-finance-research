# DATA PERIOD:
# By default, this script uses a rolling 3-year lookback ending on the current date.
#
# To change the rolling period, simply change LOOKBACK_YEARS:
#     LOOKBACK_YEARS = 3    # Last 3 years
#     LOOKBACK_YEARS = 5    # Last 5 years
#     LOOKBACK_YEARS = 10   # Last 10 years
#
# To analyze a specific historical period instead, replace the
# automatic START/END calculation with:
#     START = datetime(2020, 1, 1)
#     END = datetime(2024, 12, 31)
#
# This allows users to switch between a dynamic rolling window
# and any specific historical date range they wish to study.



import warnings
warnings.filterwarnings("ignore")

from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

TICKERS = ["NVDA","AMD","PLTR","MSFT","GOOGL","META","TSLA","AAPL","IBM","ORCL"] #Add or remove any by inserting or deleting the stock's ticker
BENCHMARK = "^GSPC"
LOOKBACK_YEARS = 3
END = datetime.now()
START = END - timedelta(days=int(LOOKBACK_YEARS * 365.25))
OUT = Path("graphs_output")
OUT.mkdir(exist_ok=True)

def get_prices(tickers, start=START, end=END):
    data = yf.download(
        tickers,
        start=start.strftime("%Y-%m-%d"),
        end=(end + timedelta(days=1)).strftime("%Y-%m-%d"),
        auto_adjust=True,
        progress=False,
        group_by="column",
    )
    if isinstance(data.columns, pd.MultiIndex):
        level0 = data.columns.get_level_values(0)
        if "Close" in level0:
            data = data["Close"]
        elif "Adj Close" in level0:
            data = data["Adj Close"]
        else:
            raise ValueError("Close data was not returned by yfinance.")
    return data.dropna(how="all").ffill()

def finish(filename):
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=300, bbox_inches="tight")
    plt.show()

def ttm_operating_margin(ticker):
    stmt = yf.Ticker(ticker).quarterly_income_stmt
    if stmt is None or stmt.empty:
        return np.nan

    if "Operating Income" not in stmt.index or "Total Revenue" not in stmt.index:
        return np.nan

    op = stmt.loc["Operating Income"].dropna()
    rev = stmt.loc["Total Revenue"].dropna()
    common = op.index.intersection(rev.index)

    if len(common) < 4:
        return np.nan

    common = common.sort_values()
    ttm_op = op.loc[common[-4:]].sum()
    ttm_rev = rev.loc[common[-4:]].sum()

    if ttm_rev == 0:
        return np.nan
    return ttm_op / ttm_rev * 100

margin = pd.Series({t: ttm_operating_margin(t) for t in TICKERS}).dropna().sort_values()

plt.figure(figsize=(10, 7))
plt.barh(margin.index, margin.values)
plt.axvline(0, linewidth=1)
plt.title("TTM Operating Margin — Latest Available Financial Data")
plt.xlabel("Operating margin (%)")
plt.ylabel("Company")
plt.grid(axis="x", alpha=0.25)
finish("12_operating_margin.png")
