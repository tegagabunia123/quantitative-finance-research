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
    ["^GSPC"],
    period="6y",
    # Here it is indicated that the data over 6 year period is being used, Change it to any date or any yearly time period. For specific dates use start and end (YYYY,MM,D - start="2025,05,5" (then below) end="2026,05,5")
    auto_adjust=True
)["Close"]

date_index = market_data.index

bank_reserves = load_fred("WRESBAL", date_index)
repo_rate = load_fred("SOFR", date_index)
three_month_tbill = load_fred("DGS3MO", date_index)

data = pd.concat(
    [
        bank_reserves["WRESBAL"],
        repo_rate["SOFR"],
        three_month_tbill["DGS3MO"]
    ],
    axis=1
)

data.columns = [
    "Bank Reserves",
    "Repo Rate",
    "3M T-Bill"
]

data = data.dropna()

fig, ax1 = plt.subplots(
    figsize=(12, 6)
)

line1 = ax1.plot(
    data.index,
    data["Bank Reserves"],
    color="darkgreen",
    label="Bank Reserves"
)

ax1.set_ylabel("Reserves")
ax1.set_title(
    "Liquidity Stress: Reserves vs Repo & T-Bills"
)

ax2 = ax1.twinx()

line2 = ax2.plot(
    data.index,
    data["Repo Rate"],
    label="Repo Rate"
)

line3 = ax2.plot(
    data.index,
    data["3M T-Bill"],
    label="3M T-Bill"
)

ax2.set_ylabel("Rates")

lines = line1 + line2 + line3
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper left")

plt.tight_layout()
plt.show()
