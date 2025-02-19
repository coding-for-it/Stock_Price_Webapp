import streamlit as st
from PIL import Image
import stock  # Import stock.py

def show_home_page():
    """Home Page UI"""
    st.markdown(
        """
        <h1 style="text-align: center;">📈 Stock Price Webapp</h1>
        <h5 style="text-align: center; color: gray;">Analyze S&P 500 company stock prices easily</h5>
        """,
        unsafe_allow_html=True
    )

    # Load and display the image
    st.image("./stock_price.jpg", use_container_width=True)

    # Sidebar Expanders
    with st.sidebar.expander("ℹ️ How It Works", expanded=False):
        st.write("1. Loads the list of S&P 500 companies from Wikipedia.")
        st.write("2. Filters companies based on the user's selected sector.")
        st.write("3. Fetches stock price data using Yahoo Finance (yf.download()).")
        st.write("4. Displays plots showing stock price trends for selected companies.")

    with st.sidebar.expander("💡 Use Cases", expanded=False):
        st.write("✅ Investors & Traders → Analyze stock price trends before investing.")
        st.write("✅ Finance Students & Analysts → Study market trends and sector performance.")
        st.write("✅ Business Decision-Makers → Compare sector-wise stock performances.")
        st.write("✅ General Users → Explore stock market trends in an easy-to-use web app.")

    # Centered Get Started button
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state["page"] = "stock"

    # Load stock analysis page
    if st.session_state.get("page") == "stock":
        stock.show_stock_page()
