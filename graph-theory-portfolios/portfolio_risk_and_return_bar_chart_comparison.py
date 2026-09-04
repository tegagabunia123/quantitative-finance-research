import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# You can insert any ticker of any stock into the portfolio_a (or b) = [ ] line

portfolio_a = [
    "AAPL",
    "META",
    "AMZN",
    "WMT",
    "JPM",
    "XOM",
    "LMT",
    "NVDA",
    "CVX",
    "BAC"
]



portfolio_b = [
    "NVDA",
    "MSFT",
    "UNH",
    "LLY",
    "NOC",
    "CAT",
    "PG",
    "COST",
    "GOOGL",
    "KO"
]

all_stocks = list(
    set(portfolio_a + portfolio_b)
)


data = yf.download(
    tickers=all_stocks,
    period="1y", #Here it is indicated that the data over 1 year period is being used, Change it to any date or any yearly time period. For specific dates use start and end (YYYY,MM,D - start="2025,05,5" (then below) end="2026,05,5")
    auto_adjust=True,
    progress=False
)

prices = data["Close"]


daily_returns = prices.pct_change().dropna()


portfolio_a_returns = daily_returns[
    portfolio_a
].mean(axis=1)


portfolio_b_returns = daily_returns[
    portfolio_b
].mean(axis=1)


def calculate_metrics(
    portfolio_returns,
    portfolio_stocks,
    all_returns
):

    annual_return = (
        portfolio_returns.mean() * 252
    )


    annual_volatility = (
        portfolio_returns.std() * np.sqrt(252)
    )


    correlation_matrix = all_returns[
        portfolio_stocks
    ].corr()


    upper_triangle = correlation_matrix.where(
        np.triu(
            np.ones(
                correlation_matrix.shape
            ),
            k=1
        ).astype(bool)
    )


    average_internal_correlation = (
        upper_triangle.stack().mean()
    )


    ticker_rf = yf.Ticker("^IRX")
    current_rf_yield = ticker_rf.history(period="1d")["Close"].iloc[-1]
    risk_free_rate = current_rf_yield / 1000


    sharpe_ratio = (
        annual_return - risk_free_rate
    ) / annual_volatility


    return {
        "Annual Return": annual_return,
        "Annual Volatility": annual_volatility,
        "Average Internal Correlation":
            average_internal_correlation,
        "Sharpe Ratio": sharpe_ratio
    }


metrics_a = calculate_metrics(
    portfolio_a_returns,
    portfolio_a,
    daily_returns
)

metrics_b = calculate_metrics(
    portfolio_b_returns,
    portfolio_b,
    daily_returns
)

portfolio_names = [
    "Portfolio A",
    "Portfolio B"
]


annual_returns = [
    metrics_a["Annual Return"],
    metrics_b["Annual Return"]
]


annual_volatility = [
    metrics_a["Annual Volatility"],
    metrics_b["Annual Volatility"]
]


average_correlation = [
    metrics_a[
        "Average Internal Correlation"
    ],
    metrics_b[
        "Average Internal Correlation"
    ]
]


sharpe_ratios = [
    metrics_a["Sharpe Ratio"],
    metrics_b["Sharpe Ratio"]
]


fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8)
)


axes[0, 0].bar(
    portfolio_names,
    annual_returns
)


axes[0, 0].set_title(
    "Annual Return"
)


axes[0, 0].set_ylabel(
    "Value"
)


axes[0, 1].bar(
    portfolio_names,
    annual_volatility
)


axes[0, 1].set_title(
    "Annual Volatility"
)


axes[0, 1].set_ylabel(
    "Value"
)


axes[1, 0].bar(
    portfolio_names,
    average_correlation
)


axes[1, 0].set_title(
    "Average Internal Correlation"
)


axes[1, 0].set_ylabel(
    "Value"
)

axes[1, 1].bar(
    portfolio_names,
    sharpe_ratios
)


axes[1, 1].set_title(
    "Sharpe Ratio"
)


axes[1, 1].set_ylabel(
    "Value"
)


plt.tight_layout()


plt.show()
