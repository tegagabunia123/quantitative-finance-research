import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("graph-theory-portfolios"))
sys.path.append(os.path.abspath("qt-macro-liquidity"))

st.sidebar.title("Quantitative Research Desk")

page = st.sidebar.radio(
    "Select Research Track", 
    ["graph-theory-portfolios", "qt-macro-liquidity"]
)

if page == "graph-theory-portfolios":
    import portfolio_risk_and_return_bar_chart_comparsion

elif page == "qt-macro-liquidity":
    import fed_balance_sheet_vs_sandp500_and_vix
