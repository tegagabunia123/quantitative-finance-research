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
from statsmodels.tsa.stattools import coint

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

prices = get_prices(TICKERS + [BENCHMARK])
benchmark = prices[BENCHMARK]

results = {}
for ticker in TICKERS:
    pair = pd.concat([prices[ticker], benchmark], axis=1).dropna()
    if len(pair) < 250:
        results[ticker] = np.nan
        continue

    try:
        statistic, pvalue, critical_values = coint(
            pair.iloc[:, 0],
            pair.iloc[:, 1],
            trend="c",
            autolag="aic"
        )
        results[ticker] = pvalue
    except Exception:
        results[ticker] = np.nan

pvalues = pd.Series(results).dropna().sort_values()

plt.figure(figsize=(12, 7))

plt.bar(pvalues.index, pvalues.values, zorder=2)

plt.axhline(0.05, color="red", linestyle="--", linewidth=1.5, zorder=5, label="5% significance")
plt.axhline(0.10, color="darkred", linestyle=":", linewidth=1.5, zorder=5, label="10% significance")

plt.title(f"Engle-Granger Cointegration with S&P 500 - Rolling {LOOKBACK_YEARS}-Year Lookback")
plt.xlabel("Stock")
plt.ylabel("p-value")
plt.grid(axis="y", alpha=0.25, zorder=1)
plt.legend()

finish("14_cointegration_sp500.png")

print("\nCointegration p-values:")
print(pvalues.to_string())