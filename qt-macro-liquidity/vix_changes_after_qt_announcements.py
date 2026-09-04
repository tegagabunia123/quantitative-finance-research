import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Use standard yfinance period notation (e.g., "3y", "5y", "max")
# To use specific start and end dates instead, set PERIOD = None and uncomment the lines below:
PERIOD = "5y"

# START_DATE = "2022-05-01"
# END_DATE   = "2025-12-31"
#==============================================================================

if PERIOD is not None:
    vix = yf.download(
        "^VIX",
        period=PERIOD,
        auto_adjust=True
    )["Close"]
else:
    vix = yf.download(
        "^VIX",
        start=START_DATE,
        end=END_DATE,
        auto_adjust=True
    )["Close"]

if isinstance(vix, pd.DataFrame):
    vix = vix.iloc[:, 0]

vix_changes = vix.pct_change()



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

    event_position = vix_changes.index.searchsorted(
        event_date
    )

    event_window = vix_changes.iloc[
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
    "VIX Changes After QT Announcements"
)

plt.xlabel(
    "Days After QT Announcement"
)

plt.ylabel(
    "VIX Daily Change"
)

plt.legend()

plt.tight_layout()
plt.show()
