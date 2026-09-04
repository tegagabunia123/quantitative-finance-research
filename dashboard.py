import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import os

matplotlib.use("Agg")

st.sidebar.title("Main Desk")

category = st.sidebar.selectbox(
    "Select Research Domain",
    ["graph-theory-portfolios", "qt-macro-liquidity", "ai-bubble-speculation"]
)

if category == "graph-theory-portfolios":
    page = st.sidebar.radio(
        "Select Model",
        [
            "Risk-Return Comparison of the Two Portfolios",
            "Portfolio Risk and Return Bar Chart Comparison",
            "Complete Weighted Stock Network",
            "Correlation Heatmap of Stock Returns",
            "Minimum Spanning Tree with Distance Labels",
            "Monthly Average Returns Graph",
            "Transformation from Correlation to Distance"
        ]
    )
    
    st.title("Network-Based Portfolio Analytics Matrix")
    st.caption("Note: All network architectures and statistical metrics are processed dynamically over a rolling 6-year lookback timeframe.")
    
    if page == "Risk-Return Comparison of the Two Portfolios":
        file_path = os.path.join("graph-theory-portfolios", "risk-return_comparison_of_the_two_portfolios.py")
    elif page == "Portfolio Risk and Return Bar Chart Comparison":
        file_path = os.path.join("graph-theory-portfolios", "portfolio_risk_and_return_bar_chart_comparison.py")
    elif page == "Complete Weighted Stock Network":
        file_path = os.path.join("graph-theory-portfolios", "complete_weighted_stock_network.py")
    elif page == "Correlation Heatmap of Stock Returns":
        file_path = os.path.join("graph-theory-portfolios", "correlation_heatmap_of_stock_returns.py")
    elif page == "Minimum Spanning Tree with Distance Labels":
        file_path = os.path.join("graph-theory-portfolios", "minimum_spanning_tree_with_distance_labels.py")
    elif page == "Monthly Average Returns Graph":
        file_path = os.path.join("graph-theory-portfolios", "nonthly_average_returns_graph.py")
    elif page == "Transformation from Correlation to Distance":
        file_path = os.path.join("graph-theory-portfolios", "transformationfrom_correlation_to_distance.py")

elif category == "qt-macro-liquidity":
    page = st.sidebar.radio(
        "Select Model",
        [
            "VIX Changes After QT Announcements",
            "S&P 500 Returns After QT Announcements",
            "30-Day Rolling Correlation Fed Sheet and VIX",
            "Reserves vs Repo and T-Bills",
            "Fed Balance Sheet vs S&P 500 and VIX"
        ]
    )
    
    st.title("Rolling Correlation: Fed Balance Sheet vs VIX")
    st.caption("Note: All macroeconomic data indicators and rolling correlation vectors utilize an active 6-year data collection framework.")
    
    if page == "VIX Changes After QT Announcements":
        file_path = os.path.join("qt-macro-liquidity", "vix_changes_after_qt_announcements.py")
    elif page == "S&P 500 Returns After QT Announcements":
        file_path = os.path.join("qt-macro-liquidity", "sandp500_returns_after_qt_announcements.py")
    elif page == "30-Day Rolling Correlation Fed Sheet and VIX":
        file_path = os.path.join("qt-macro-liquidity", "30-day_rolling_correlation_fed_sheet_and_vix.py")
    elif page == "Reserves vs Repo and T-Bills":
        file_path = os.path.join("qt-macro-liquidity", "reserves_vs_repo_and_t-bills.py")
    elif page == "Fed Balance Sheet vs S&P 500 and VIX":
        file_path = os.path.join("qt-macro-liquidity", "fed_balance_sheet_vs_sandp500_and_vix.py")

elif category == "ai-bubble-speculation":
    page = st.sidebar.radio(
        "Select Valuation Metric",
        [
            "01 Indexed Returns",
            "02 PE Ratio",
            "03 PS Ratio",
            "04 EV Revenue",
            "05 Rolling Volatility",
            "06 Correlation Matrix",
            "07 Drawdowns",
            "08 Trailing PE",
            "09 Price to Sales",
            "10 EV Revenue Analysis",
            "11 Revenue Growth",
            "12 Operating Margin",
            "13 Valuation Z Scores",
            "14 Cointegration SP500"
        ]
    )
    
    st.title("The 2025 AI Bubble: Innovation, Speculation, and Market Reality")
    st.caption("Note: The data metrics in this analytics suite evaluate live market and corporate valuation matrices dynamically over a 3-year lookback timeframe.")
    
    if page == "01 Indexed Returns":
        file_path = os.path.join("ai-bubble-speculation", "01_indexed_returns.py")
    elif page == "02 PE Ratio":
        file_path = os.path.join("ai-bubble-speculation", "02_pe_ratio.py")
    elif page == "03 PS Ratio":
        file_path = os.path.join("ai-bubble-speculation", "03_ps_ratio.py")
    elif page == "04 EV Revenue":
        file_path = os.path.join("ai-bubble-speculation", "04_ev_revenue.py")
    elif page == "05 Rolling Volatility":
        file_path = os.path.join("ai-bubble-speculation", "05_rolling_volatility.py")
    elif page == "06 Correlation Matrix":
        file_path = os.path.join("ai-bubble-speculation", "06_correlation_matrix.py")
    elif page == "07 Drawdowns":
        file_path = os.path.join("ai-bubble-speculation", "07_drawdowns.py")
    elif page == "08 Trailing PE":
        file_path = os.path.join("ai-bubble-speculation", "08_trailing_pe.py")
    elif page == "09 Price to Sales":
        file_path = os.path.join("ai-bubble-speculation", "09_price_to_sales.py")
    elif page == "10 EV Revenue Analysis":
        file_path = os.path.join("ai-bubble-speculation", "10_ev_revenue.py")
    elif page == "11 Revenue Growth":
        file_path = os.path.join("ai-bubble-speculation", "11_revenue_growth.py")
    elif page == "12 Operating Margin":
        file_path = os.path.join("ai-bubble-speculation", "12_operating_margin.py")
    elif page == "13 Valuation Z Scores":
        file_path = os.path.join("ai-bubble-speculation", "13_valuation_z_scores.py")
    elif page == "14 Cointegration SP500":
        file_path = os.path.join("ai-bubble-speculation", "14_cointegration_sp500.py")

if os.path.exists(file_path):
    plt.clf()
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    exec(code, {"__name__": "__main__"})
    st.pyplot(plt.gcf())
else:
    st.error(f"Could not locate file at: {file_path}")
