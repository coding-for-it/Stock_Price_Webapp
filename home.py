import streamlit as st
from PIL import Image
import stock  # Import stock.py as a module instead of exec()

# 🎯 Centered Title and Subheading
st.markdown(
    """
    <h1 style="text-align: center;">📈 Stock Price Webapp</h1>
    <h5 style="text-align: center; color: gray;">Analyze S&P 500 company stock prices easily</h5>
    """,
    unsafe_allow_html=True
)

# Load and display the image
st.image("./stock_price.jpg", use_container_width=True)

# Initialize session state for navigation
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# Buttons for navigation
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("🛠️How It Works?"):
        st.write("1.Loads the list of S&P 500 companies from Wikipedia.")
        st.write("2.Filters companies based on the user's selected sector.")
        st.write("3.Fetches stock price data using Yahoo Finance (yf.download()).")
        st.write("4.Displays plots showing stock price trends for selected companies")

with col2:
    if st.button("📌 Use Cases"):
        st.write("✅ Investors & Traders → Analyze stock price trends before investing.")
        st.write("✅ Finance Students & Analysts → Study market trends and sector performance.")
        st.write("✅ Business Decision-Makers → Compare sector-wise stock performances.")
        st.write("✅ General Users → Explore stock market trends in an easy-to-use web app.")

with col3:
    if st.button("🚀Get Started"):
        st.session_state["page"] = "stock"

# Load the appropriate page
if st.session_state["page"] == "stock":
    stock.show_stock_page()  # Call function from stock.py
