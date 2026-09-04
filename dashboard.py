import streamlit as st
import matplotlib
import os

matplotlib.use("Agg")

st.sidebar.title("Main Desk")

page = st.sidebar.radio(
    "Select Research Track", 
    ["graph-theory-portfolios", "qt-macro-liquidity"]
)

if page == "graph-theory-portfolios":
    st.title("Network-Based Portfolio Analytics Matrix")
    
    # Target path inside your folder
    file_path = os.path.join("graph-theory-portfolios", "portfolio_risk_and_return_bar_chart_comparsion.py")
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        
        exec(code, {"__name__": "__main__"})
        
        st.pyplot(plt.gcf())
    else:
        st.error(f"Could not locate file at: {file_path}")

elif page == "qt-macro-liquidity":
    st.title("Rolling Correlation: Fed Balance Sheet vs VIX")
    
    file_path = os.path.join("qt-macro-liquidity", "fed_balance_sheet_vs_sandp500_and_vix.py")
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
            
        exec(code, {"__name__": "__main__"})
        st.pyplot(plt.gcf())
    else:
        st.error(f"Could not locate file at: {file_path}")
