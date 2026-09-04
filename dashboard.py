import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import os

matplotlib.use("Agg")

st.sidebar.title("Quantitative Research Desk")

category = st.sidebar.selectbox(
    "Select Research Domain",
    ["graph-theory-portfolios", "qt-macro-liquidity"]
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

if os.path.exists(file_path):
    plt.clf()
    with open(file_path, "r", encoding="utf-8") as f:
        code = f.read()
    exec(code, {"__name__": "__main__"})
    st.pyplot(plt.gcf())
else:
    st.error(f"Could not locate file at: {file_path}")
