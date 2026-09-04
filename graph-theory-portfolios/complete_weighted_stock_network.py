import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# You can insert any ticker of any stock into the Stocks = [ ] line

stocks = [
    "AAPL",
    "MSFT",
    "NVDA",
    "GOOGL",
    "AMZN",
    "META",
    "XOM",
    "LLY",
    "JPM",
    "WMT",
    "CAT",
    "LMT",
    "COST",
    "UNH",
    "PG",
    "CVX",
    "KO",
    "BAC"
]

data = yf.download(
    tickers=stocks,
    period="1y", #Here it is indicated that the data over 1 year period is being used, Change it to any date or any yearly time period. For specific dates use start and end (YYYY,MM,D - start="2025,05,5" (then below) end="2026,05,5")
    auto_adjust=True,
    progress=False
)

prices = data["Close"]

daily_returns = prices.pct_change().dropna()

correlation_matrix = daily_returns.corr()

distance_matrix = np.sqrt(
    2 * (1 - correlation_matrix)
)

G = nx.Graph()


# Add stocks as nodes
for stock in stocks:
    G.add_node(stock)

for i in range(len(stocks)):

    for j in range(i + 1, len(stocks)):

        stock_1 = stocks[i]
        stock_2 = stocks[j]

        distance = distance_matrix.loc[
            stock_1,
            stock_2
        ]

        G.add_edge(
            stock_1,
            stock_2,
            weight=distance
        )

positions = nx.spring_layout(
    G,
    seed=42
)

plt.figure(
    figsize=(16, 10)
)

nx.draw_networkx_nodes(
    G,
    positions,
    node_size=1600
)

nx.draw_networkx_edges(
    G,
    positions,
    width=0.7,
    alpha=0.7
)

nx.draw_networkx_labels(
    G,
    positions,
    font_size=10,
    font_weight="bold"
)

edge_labels = {}

for stock_1, stock_2, attributes in G.edges(data=True):

    edge_labels[
        (stock_1, stock_2)
    ] = f"{attributes['weight']:.2f}"

nx.draw_networkx_edge_labels(
    G,
    positions,
    edge_labels=edge_labels,
    font_size=6
)

plt.title(
    "Complete Weighted Stock Network",
    fontsize=16
)


plt.axis("off")


plt.tight_layout()


plt.show()
