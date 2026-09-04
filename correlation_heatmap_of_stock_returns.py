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

daily_returns = prices.pct_change().dropna()

correlation_matrix = daily_returns.corr()


plt.figure(
    figsize=(12, 10)
)


image = plt.imshow(
    correlation_matrix,
    vmin=-1,
    vmax=1,
    cmap="coolwarm"
)


plt.xticks(
    ticks=np.arange(len(correlation_matrix.columns)),
    labels=correlation_matrix.columns,
    rotation=45,
    ha="right"
)


plt.yticks(
    ticks=np.arange(len(correlation_matrix.index)),
    labels=correlation_matrix.index
)


for i in range(len(correlation_matrix.index)):
    for j in range(len(correlation_matrix.columns)):

        value = correlation_matrix.iloc[i, j]

        plt.text(
            j,
            i,
            f"{value:.2f}",
            ha="center",
            va="center",
            fontsize=7
        )


plt.colorbar(
    image,
    label="Correlation"
)


plt.title(
    "Correlation Heatmap of Stock Returns"
)


plt.tight_layout()
plt.show()