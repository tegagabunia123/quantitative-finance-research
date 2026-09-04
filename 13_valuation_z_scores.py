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

TICKERS = ["NVDA", "AMD", "PLTR", "MSFT", "GOOGL", "META", "TSLA", "AAPL", "IBM", "ORCL"] #Add or remove any by inserting or deleting the stock's ticker
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


relative = prices[TICKERS].div(prices[BENCHMARK], axis=0)
log_relative = np.log(relative.replace(0, np.nan))

current_z = {}
for ticker in TICKERS:
    s = log_relative[ticker].dropna()
    mu = s.mean()
    sigma = s.std(ddof=1)

    if sigma > 0 and len(s) > 0:
        current_z[ticker] = (s.iloc[-1] - mu) / sigma
    else:
        current_z[ticker] = np.nan

z = pd.Series(current_z).dropna().sort_values(ascending=False)

plt.figure(figsize=(12, 7))
plt.bar(z.index, z.values, color="skyblue", edgecolor="navy")

plt.axhline(2, linestyle="--", color="red", linewidth=1.5, label="+2σ Threshold (Extreme Overperformance)")
plt.axhline(-2, linestyle="--", color="green", linewidth=1.5, label="-2σ Threshold (Extreme Underperformance)")
plt.axhline(0, color="black", linewidth=1)

plt.title(f"Relative-Valuation / Price-Divergence Z-Scores - {LOOKBACK_YEARS}-Year Lookback")
plt.ylabel("Z-Score (vs. S&P 500 Log Ratio)")
plt.xlabel("Stock Ticker")
plt.grid(axis="y", alpha=0.25)
plt.legend()

finish("13_valuation_z_scores.png")

print("\nCurrent Valuation Z-Scores (vs S&P 500):")
print(z.to_string())