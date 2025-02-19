import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf

def show_stock_page():
    st.sidebar.header('User Input Features')

    # Load Data (Cached)
    @st.cache_data
    def load_data():
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        html = pd.read_html(url, header=0)
        df = html[0]
        return df

    df = load_data()

    # Persistent Selection using Session State
    if "selected_sector" not in st.session_state:
        st.session_state.selected_sector = []

    selected_sector = st.sidebar.multiselect(
        'Sector', sorted(df['GICS Sector'].unique()), default=st.session_state.selected_sector
    )
    st.session_state.selected_sector = selected_sector  # Store selection persistently

    # Filter data based on selection
    df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

    # Show warning only when user tries to fetch data without selecting a sector
    if not selected_sector:
        st.warning("⚠️ Please select a sector from the sidebar to view stock data.")
        return

    st.header('Companies in Selected Sector')
    st.write(f'Data Dimension: {df_selected_sector.shape[0]} rows and {df_selected_sector.shape[1]} columns.')
    st.dataframe(df_selected_sector)

    # Download CSV Function
    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
        return href

    st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

    # Ensure at least one company is selected before fetching stock data
    if df_selected_sector.empty or "Symbol" not in df_selected_sector.columns:
        st.warning("⚠️ No valid stock tickers found for the selected sector.")
        return

    selected_symbols = list(df_selected_sector.Symbol.dropna())[:10]  # Ensure no NaN values
    if not selected_symbols:
        st.warning("⚠️ No valid stock tickers available for fetching data.")
        return

    # Fetch stock data
    try:
        data = yf.download(
            tickers=selected_symbols,
            period="ytd",
            interval="1d",
            group_by='ticker',
            auto_adjust=True,
            prepost=True,
            threads=True,
            proxy=None
        )
    except Exception as e:
        st.error(f"⚠️ Error fetching stock data: {e}")
        return

    if data.empty:
        st.warning("⚠️ No stock data found for the selected tickers.")
        return

    # Function to plot stock price
    def price_plot(symbol):
        if symbol not in data or "Close" not in data[symbol]:
            st.warning(f"⚠️ No closing price data for {symbol}")
            return

        df = pd.DataFrame(data[symbol].Close)
        df['Date'] = df.index

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
        ax.plot(df.Date, df.Close, color='skyblue', alpha=0.8)

        ax.set_xticks(df.Date[::len(df)//10])  # Reduce number of x-ticks
        ax.set_xticklabels(df.Date[::len(df)//10], rotation=45)

        ax.set_title(symbol, fontweight='bold')
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Closing Price', fontweight='bold')

        st.pyplot(fig)

    num_company = st.sidebar.slider('Number of Companies', 1, min(5, len(selected_symbols)))

    if st.button('Show Plots'):
        st.header('Stock Closing Price')
        for i in selected_symbols[:num_company]:
            price_plot(i)
