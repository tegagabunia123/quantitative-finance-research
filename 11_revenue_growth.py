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

TICKERS = [
    "NVDA", "AMD", "PLTR", "MSFT", "GOOGL",
    "META", "TSLA", "AAPL", "IBM", "ORCL"
]

#Add or remove any by inserting or deleting the stock's ticker

BENCHMARK = "^GSPC"


LOOKBACK_YEARS = 3

END = datetime.now()
START = END - timedelta(days=int(LOOKBACK_YEARS * 365.25))

OUT = Path("graphs_output")
OUT.mkdir(exist_ok=True)


def finish(filename):
    plt.tight_layout()
    plt.savefig(
        OUT / filename,
        dpi=300,
        bbox_inches="tight"
    )
    plt.show()


def get_quarterly_revenue(ticker):
    try:
        t = yf.Ticker(ticker)
        q_fin = t.quarterly_financials

        if q_fin.empty:
            return pd.Series(dtype=float)

        rev_row = None
        for key in ["Total Revenue", "Operating Revenue"]:
            if key in q_fin.index:
                rev_row = q_fin.loc[key]
                break

        if rev_row is None:
            return pd.Series(dtype=float)

        revenue = rev_row.dropna().astype(float)
        revenue.index = pd.to_datetime(revenue.index)
        revenue = revenue.sort_index()

        revenue = revenue[revenue.index >= START]

        return revenue

    except Exception as e:
        print(f"{ticker}: Fetch error -> {e}")
        return pd.Series(dtype=float)


def ttm_revenue_growth(ticker):
    try:
        revenue = get_quarterly_revenue(ticker)

        print(
            f"{ticker}: {len(revenue)} quarterly observations "
            f"returned within the last {LOOKBACK_YEARS} years."
        )

        if len(revenue) < 8:
            if len(revenue) >= 5:
                latest_q = revenue.iloc[-1]
                yoy_q = revenue.iloc[-5]
                if yoy_q <= 0:
                    return np.nan
                return ((latest_q / yoy_q) - 1) * 100

            print(f"{ticker}: Not enough data for TTM calculation.")
            return np.nan

        latest_ttm = revenue.iloc[-4:].sum()

        previous_ttm = revenue.iloc[-8:-4].sum()

        if previous_ttm <= 0:
            return np.nan

        growth = ((latest_ttm / previous_ttm) - 1) * 100
        return growth

    except Exception as e:
        print(f"{ticker}: ERROR -> {e}")
        return np.nan



growth = pd.Series(
    {ticker: ttm_revenue_growth(ticker) for ticker in TICKERS},
    dtype=float
).dropna().sort_values()

print("\nTTM Revenue Growth (%):")
print(growth)

if growth.empty:
    raise ValueError(
        "Yahoo Finance did not return usable quarterly revenue data."
    )


plt.figure(figsize=(10, 7))

plt.barh(
    growth.index,
    growth.values,
    color="skyblue",
    edgecolor="navy",
    zorder=3
)

plt.axvline(
    0,
    color="red",
    linestyle="--",
    linewidth=1.5,
    zorder=10,
    label="0% Growth"
)

plt.title(f"TTM Revenue Growth (Last {LOOKBACK_YEARS} Years)")
plt.xlabel("TTM Revenue Growth (%)")
plt.ylabel("Company")
plt.grid(axis="x", alpha=0.3, zorder=0)
plt.legend()

finish("11_revenue_growth.png")