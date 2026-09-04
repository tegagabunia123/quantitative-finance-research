import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# You can insert any ticker of any stock into the Stocks = [ ] line

stocks = [
    "AAPL",
    "MSFT",
    "NVDA",
    "META",
    "GOOGL",
    "AMZN",
    "WMT",
    "COST",
    "PG",
    "KO",
    "JPM",
    "BAC",
    "XOM",
    "CVX",
    "CAT",
    "LMT",
    "UNH",
    "LLY"
]


data = yf.download(
    stocks,
    period="1y", #Here it is indicated that the data over 1 year period is being used, Change it to any date or any yearly time period. For specific dates use start and end (YYYY,MM,D - start="2025,05,5" (then below) end="2026,05,5")
    auto_adjust=True,
    progress=False
)

prices = data["Close"]

correlation_values = np.linspace(
    -1,
    1,
    100
)


distance_values = np.sqrt(
    2 * (1 - correlation_values)
)


plt.figure(
    figsize=(10, 6)
)


plt.plot(
    correlation_values,
    distance_values
)


# Horizontal line at rho = 0 distance
zero_correlation_distance = np.sqrt(2)

plt.axhline(
    y=zero_correlation_distance,
    linestyle="--",
    color="black",
    linewidth=1
)

plt.axvline(
    x=0,
    linestyle="--",
    color="black",
    linewidth=1
)


plt.title(
    "Transformation from Correlation to Distance"
)


plt.xlabel(
    "Correlation (ρ)"
)


plt.ylabel(
    "Distance d = √(2(1 - ρ))"
)


plt.tight_layout()
plt.show()