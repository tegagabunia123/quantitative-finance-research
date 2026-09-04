import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import pandas_datareader.data as web


def load_fred(series_id, timeframe):
    start_date = timeframe.min().strftime("%Y-%m-%d")
    end_date = timeframe.max().strftime("%Y-%m-%d")

    df = web.DataReader(series_id, "fred", start_date, end_date)

    df.columns = [series_id]

    return df.reindex(timeframe).ffill()


market_data = yf.download(
    ["^GSPC", "^VIX"],
    period="6y",
    # Here it is indicated that the data over 6 year period is being used, Change it to any date or any yearly time period. For specific dates use start and end (YYYY,MM,D - start="2025,05,5" (then below) end="2026,05,5")
    auto_adjust=True
)["Close"]

market_data.columns = ["SP500", "VIX"]

fed_daily = load_fred(
    "WALCL",
    market_data.index
)

data = pd.concat(
    [
        fed_daily["WALCL"],
        market_data["SP500"],
        market_data["VIX"]
    ],
    axis=1
)

data.columns = [
    "Fed Balance Sheet",
    "SP500",
    "VIX"
]

data = data.dropna()

data["SP500_scaled"] = data["SP500"] * 2000

fig, ax1 = plt.subplots(
    figsize=(12, 6)
)

line1 = ax1.plot(
    data.index,
    data["Fed Balance Sheet"],
    label="Fed Balance Sheet",
    color="blue"
)

line2 = ax1.plot(
    data.index,
    data["SP500_scaled"],
    label="S&P 500 (scaled)",
    color="orange"
)

ax1.set_xlabel("")
ax1.set_ylabel("Fed Assets / S&P")
ax1.set_title(
    "Fed Balance Sheet vs S&P 500 and VIX"
)

ax2 = ax1.twinx()

line3 = ax2.plot(
    data.index,
    data["VIX"],
    linestyle="--",
    color="black",
    label="VIX"
)

ax2.set_ylabel("VIX")

# Merged all legends into one single box so it does not block the visual line view
lines = line1 + line2 + line3
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper left")

plt.tight_layout()
plt.show()
