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
    "NOC",
    "BAC"
]

data = yf.download(
    tickers=stocks,
    period="1y", # Here it is indicated that the data over 1 year period is being used, Change it to any date or any yearly time period. For specific dates use start and end (YYYY,MM,D - start="2025,05,5" (then below) end="2026,05,5")
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


MST = nx.minimum_spanning_tree(
    G,
    weight="weight"
)


positions = nx.spring_layout(
    MST,
    seed=42
)

plt.figure(
    figsize=(14, 10)
)

nx.draw_networkx_nodes(
    MST,
    positions,
    node_size=1500
)

nx.draw_networkx_edges(
    MST,
    positions,
    width=1.2
)

nx.draw_networkx_labels(
    MST,
    positions,
    font_size=10
)

edge_labels = {}

for stock_1, stock_2, attributes in MST.edges(data=True):

    edge_labels[
        (stock_1, stock_2)
    ] = f"{attributes['weight']:.2f}"

nx.draw_networkx_edge_labels(
    MST,
    positions,
    edge_labels=edge_labels,
    font_size=8
)


plt.title(
    "Minimum Spanning Tree with Distance Labels"
)


plt.axis("off")


plt.tight_layout()


plt.show()
