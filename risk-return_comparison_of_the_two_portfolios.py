import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ==========================================
# PORTFOLIO A
# ==========================================

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


# ==========================================
# PORTFOLIO B
# ==========================================

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


# ==========================================
# ALL STOCKS
# ==========================================

all_stocks = list(
    set(portfolio_a + portfolio_b)
)


# ==========================================
# DOWNLOAD DATA
# ==========================================

data = yf.download(
    tickers=all_stocks,
    start="2025-03-01",
    end="2026-04-01",
    auto_adjust=True,
    progress=False
)


# ==========================================
# EXTRACT CLOSE PRICES
# ==========================================

prices = data["Close"]


# ==========================================
# CALCULATE DAILY RETURNS
# ==========================================

daily_returns = prices.pct_change().dropna()


# ==========================================
# EQUAL-WEIGHTED PORTFOLIO RETURNS
# ==========================================

portfolio_a_returns = daily_returns[
    portfolio_a
].mean(axis=1)


portfolio_b_returns = daily_returns[
    portfolio_b
].mean(axis=1)


# ==========================================
# ANNUAL RETURN
# ==========================================

portfolio_a_annual_return = (
    portfolio_a_returns.mean() * 252
)


portfolio_b_annual_return = (
    portfolio_b_returns.mean() * 252
)


# ==========================================
# ANNUAL VOLATILITY
# ==========================================

portfolio_a_volatility = (
    portfolio_a_returns.std() * np.sqrt(252)
)


portfolio_b_volatility = (
    portfolio_b_returns.std() * np.sqrt(252)
)


# ==========================================
# CREATE SCATTER PLOT
# ==========================================

plt.figure(
    figsize=(10, 8)
)


# ==========================================
# PORTFOLIO A
# ==========================================

plt.scatter(
    portfolio_a_volatility,
    portfolio_a_annual_return,
    s=250
)


plt.text(
    portfolio_a_volatility + 0.002,
    portfolio_a_annual_return + 0.002,
    "Portfolio A",
    fontsize=11
)


# ==========================================
# PORTFOLIO B
# ==========================================

plt.scatter(
    portfolio_b_volatility,
    portfolio_b_annual_return,
    s=250
)


plt.text(
    portfolio_b_volatility + 0.002,
    portfolio_b_annual_return + 0.002,
    "Portfolio B",
    fontsize=11
)


# ==========================================
# TITLES
# ==========================================

plt.title(
    "Risk-Return Comparison of the Two Portfolios"
)


plt.xlabel(
    "Annual Volatility"
)


plt.ylabel(
    "Annual Return"
)


plt.tight_layout()


plt.show()