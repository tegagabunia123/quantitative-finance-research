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

prices = get_prices(TICKERS)
peaks = prices.cummax()
drawdown = prices / peaks - 1

plt.figure(figsize=(13, 7))
for ticker in TICKERS:
    plt.plot(drawdown.index, drawdown[ticker] * 100, label=ticker, linewidth=1.2)

plt.axhline(0, linewidth=1)
plt.title(f"Cumulative Drawdowns from Peak — Rolling {LOOKBACK_YEARS}-Year Lookback")
plt.xlabel("Date")
plt.ylabel("Drawdown (%)")
plt.grid(alpha=0.25)
plt.legend(ncol=2)
finish("07_drawdowns.png")
