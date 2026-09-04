import streamlit as st

st.sidebar.title("Main Desk")

page = st.sidebar.radio(
    "Select Research Track", 
    ["graph-theory-portfolios", "qt-macro-liquidity"]
)

if page == "graph-theory-portfolios":
    import portfolio_risk_and_return_bar_chart_comparsion

elif page == "qt-macro-liquidity":
    import fed_balance_sheet_vs_sandp500_and_vix
