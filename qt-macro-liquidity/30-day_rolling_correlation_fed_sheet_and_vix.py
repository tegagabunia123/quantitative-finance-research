import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import pandas_datareader.data as web

# Use standard yfinance period notation (e.g., "5y", "6y", "10y").
# Set this to None if you want to use the specific start/end dates below instead.
PERIOD = "6y"

# Specific Date Range (Only used if PERIOD = None above)
START_DATE = "2019-01-01"
END_DATE   = "2025-01-01"
#==============================================================================

# Parse dates based on user settings
if PERIOD is not None:
    end_date = pd.Timestamp.now().strftime("%Y-%m-%d")
    days = int(PERIOD[:-1]) * 365 if PERIOD[-1].lower() == "y" else int(PERIOD[:-1])
    start_date = (pd.Timestamp.now() - pd.Timedelta(days=days)).strftime("%Y-%m-%d")
else:
    start_date = START_DATE
    end_date = END_DATE
fed_balance_sheet = web.DataReader("WALCL", "fred", start_date, end_date)  # native weekly (Wed)

if PERIOD is not None:
    vix = yf.download("^VIX", period=PERIOD, auto_adjust=True)["Close"]
else:
    vix = yf.download("^VIX", start=start_date, end=end_date, auto_adjust=True)["Close"]

if isinstance(vix, pd.DataFrame):
    vix = vix.iloc[:, 0]

vix_weekly = vix.resample("W-WED").last()

data = pd.concat([fed_balance_sheet["WALCL"], vix_weekly], axis=1)
data.columns = ["Fed Balance Sheet", "VIX"]
data = data.dropna()

data["Fed Change"] = data["Fed Balance Sheet"].pct_change()
data["VIX Change"] = data["VIX"].pct_change()

rolling_correlation = (
    data["Fed Change"].rolling(window=30).corr(data["VIX Change"])
)

plt.figure(figsize=(12, 5))
plt.plot(rolling_correlation.index, rolling_correlation, label="30-Week Rolling Correlation")
plt.axhline(0, linestyle="-")
plt.title("30-Day Rolling Correlation: Fed Balance Sheet vs VIX")
plt.ylabel("Correlation")
plt.tight_layout()
plt.show()
