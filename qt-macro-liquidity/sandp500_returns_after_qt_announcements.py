import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Use standard yfinance period notation (e.g., "3y", "5y", "max")
# To use specific start and end dates instead, set PERIOD = None and uncomment the lines below:
PERIOD = "5y"

# START_DATE = "2022-05-01"
# END_DATE   = "2025-12-31"

if PERIOD is not None:
    sp500 = yf.download(
        "^GSPC",
        period=PERIOD,
        auto_adjust=True
    )["Close"]
else:
    sp500 = yf.download(
        "^GSPC",
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True
    )["Close"]

if isinstance(sp500, pd.DataFrame):
    sp500 = sp500.iloc[:, 0]

sp500_returns = sp500.pct_change()

qt_events = [
    "2022-06-01",
    "2023-09-20",
    "2025-10-15"
]


days_after = 20

plt.figure(
    figsize=(12, 5)
)


for event_date in qt_events:

    event_date = pd.Timestamp(event_date)

    event_position = sp500_returns.index.searchsorted(
        event_date
    )

    event_window = sp500_returns.iloc[
        event_position:
        event_position + days_after
    ]

    plt.plot(
        range(len(event_window)),
        event_window.values,
        marker="o",
        label=f"QT {event_date.strftime('%Y-%m-%d')}"
    )

plt.axhline(
    0,
    linestyle="--",
    color="black"
)


plt.title(
    "S&P 500 Returns After QT Announcements"
)

plt.xlabel(
    "Days After QT Announcement"
)

plt.ylabel(
    "S&P 500 Daily Return"
)

plt.legend()

plt.tight_layout()
plt.show()
