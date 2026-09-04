import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# You can insert any ticker of any stock into the Stocks = [ ] line

stocks = [
    "AAPL",
    "AMZN",
    "CAT",
    "COST",
    "GOOGL",
    "JPM",
    "LLY",
    "LMT",
    "META",
    "MSFT",
    "NVDA",
    "PG",
    "UNH",
    "WMT",
    "XOM",
    "CVX",
    "KO",
    "BAC"
]

data = yf.download(
    stocks,
    period="1y", #Here it is indicated that the data over 1 year period is being used, Change it to any date or any yearly time period. For specific dates use start and end (YYYY,MM,D - start="2025,05,5" (then below) end="2026,05,5")
    auto_adjust=True,
    progress=False
)

prices = data["Close"]

daily_returns = prices.pct_change()

monthly_average_returns = (
    daily_returns
    .resample("ME")
    .mean()
)

plt.figure(figsize=(14, 8))

monthly_average_returns.plot(
    kind="bar",
    width=0.8,
    ax=plt.gca()
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title(
    "Monthly Average Returns of Selected Stocks"
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Average Return"
)

plt.legend(
    title=None,
    ncol=3,
    fontsize=8
)

plt.xticks(
    rotation=90
)

plt.tight_layout()

plt.show()