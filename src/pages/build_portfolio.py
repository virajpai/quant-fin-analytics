import streamlit as st
import yfinance as yf

import pandas as pd
import numpy as np

from datetime import datetime
from commons import portfolio

import logging
import sys

### LOGGER #####################################################################
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)
################################################################################

# Load a curated list of Indian stock tickers (NSE/BSE)
# Source: Predefined CSV (replace with your own URL or local file)
TICKERS_CSV_URL = "static/data/EQUITY_L.csv"

@st.cache_data
def load_tickers():
    # Load tickers from CSV (columns: ticker, name, exchange)
    try:
        df = pd.read_csv(TICKERS_CSV_URL)
        return df[['SYMBOL', 'NAME OF COMPANY']].values.tolist()  # Format: [[TICKER.NS, Name], ...]
    except:
        return [
            ['RELIANCE', 'Reliance Industries (NSE)'],
            ['TCS', 'Tata Consultancy Services (NSE)'],
            ['HDFCBANK', 'HDFC Bank (NSE)'],
            # Add more tickers if CSV fails to load
        ]

# Initialize session state for portfolio
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# Function to fetch the last closing price
def get_last_close_price(ticker):
    try:
        stock = yf.Ticker(f"{ticker}.NS")
        hist = stock.history(period="1d")
        if not hist.empty:
            return hist['Close'].iloc[-1]
        else:
            return None
    except:
        logger.error(e)
        return None

def reset_selectbox():
    st.session_state.selected_option = "" 

# Streamlit app
st.title("📈 India Stock Portfolio Tracker (NSE/BSE)")

# Load tickers and create searchable dropdown
tickers_list = load_tickers()
ticker_options = {ticker: f"{name} ({ticker})" for ticker, name in tickers_list}

# Searchable dropdown in the main interface
st.header("Add Stocks to Portfolio")
selected_ticker_label = st.selectbox(
    "Search for a stock:",
    options=list(ticker_options.values()),
    index= None, # 0,
    help="Type to search for stocks (e.g., 'Reliance', 'HDFC')",
    key= "selected_option"
)
logger.info('Selected Ticker Label: ', selected_ticker_label)

if not selected_ticker_label is None:
    # Extract the ticker from the selected label
    selected_ticker = [ticker for ticker, label in ticker_options.items() if label == selected_ticker_label][0]

    # Input quantity and add to portfolio
    quantity = st.number_input("Quantity", min_value=1, value=1)
    if st.button("Add Stock to Portfolio"):
        with st.spinner("Fetching stock data..."):
            last_close_price = get_last_close_price(selected_ticker)
            if last_close_price:
                # Check if ticker already exists in portfolio
                existing_stock = next((s for s in st.session_state.portfolio if s['ticker'] == selected_ticker), None)
                if existing_stock:
                    existing_stock['quantity'] += quantity  # Update quantity if exists
                else:
                    st.session_state.portfolio.append({
                        "ticker": selected_ticker,
                        "quantity": quantity,
                        "last_close_price": last_close_price,
                        # "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                st.success(f"Added {quantity} shares of {ticker_options[selected_ticker]}")
            else:
                st.error("Failed to fetch data. Check the ticker or try again later.")
    
        # reset_selectbox()


# Display and manage portfolio
st.header("Your Portfolio")
if st.session_state.portfolio:
    # Create DataFrame
    portfolio_df = pd.DataFrame(st.session_state.portfolio)
    portfolio_df["Value"] = portfolio_df["quantity"] * portfolio_df["last_close_price"]
    portfolio_df.insert(0, "Delete", False)  # Checkbox column at beginning
    # portfolio_df.insert(0, "Delete", "🗑️")

    # Display as an editable table
    edited_df = st.data_editor(
        portfolio_df,
        column_config={
            "Delete": st.column_config.CheckboxColumn(
                " 🗑️",
                help="Check to delete this row",
                disabled=False  # Make the column non-editable
            ),
            "ticker": st.column_config.SelectboxColumn(
                "Stock",
                options=[ticker for ticker, _ in tickers_list],
                required=True,
                disabled=True
            ),
            "quantity": st.column_config.NumberColumn(
                "Qty",
                min_value=1,
                format="%d"
            ),
            "last_close_price": st.column_config.NumberColumn(
                "Price(₹)",
                disabled=True,
                format="₹%.2f"
            ),
            "Value": st.column_config.NumberColumn(
                "Value(₹)",
                disabled=True,
                format="₹%.2f"
            )
        },
        key="portfolio_editor",
        hide_index=True
    )

    # Update portfolio based on edits
    # if not edited_df.equals(portfolio_df[['ticker', 'quantity', 'last_close_price']]):
    #     st.session_state.portfolio = edited_df.to_dict("records")
    #     st.rerun()
    #     # Process deletions and updates
    
    if not edited_df.equals(portfolio_df):
        # Remove checked rows
        updated_portfolio = edited_df[~edited_df["Delete"]].drop(columns=["Delete"])
        st.session_state.portfolio = updated_portfolio.to_dict("records")
        st.rerun()

    # Remove stocks
    if st.button("Remove All Stocks"):
        st.session_state.portfolio = []
        st.rerun()

    # Calculate total portfolio value
    total_value = portfolio_df["Value"].sum()
    st.subheader(f"Total Portfolio Value: :green[₹{total_value:,.2f}]")

    ### Simulate Portfolio
    if st.button("Simulate Portfolio"):
        stocks = [s + ".NS" for s in portfolio_df["ticker"].values]
        stock_qty = portfolio_df["quantity"].values

        sim_df = portfolio.simulate_portfolio(stocks, stock_qty)

        stat_df = pd.DataFrame(sim_df.median(axis=1).T) # .astype(int))
        stat_df.columns = ['Expected Value']

        stat_df['Worst Case (5% chance)'] = sim_df.quantile(0.05, axis=1) #.astype(int)
        stat_df['Best Case (5% chance)'] = sim_df.quantile(0.95, axis=1) #.astype(int)
        
        num_rows = len(stat_df)

        # Date Index
        date_index = pd.date_range(start=pd.Timestamp.today().date(), periods=num_rows, freq='90D')
        formatted_index = date_index.strftime("%b-%Y")

        stat_df.index = formatted_index

        st.data_editor(
            stat_df,
            column_config= {
                "Expected Value": st.column_config.NumberColumn(
                "Expected Value(₹)",
                disabled=True,
                format="₹%.2f"),
                "Worst Case (5% chance)": st.column_config.NumberColumn(
                "Worst Case (5% chance)",
                disabled=True,
                format="₹%.2f"),
                "Best Case (5% chance)": st.column_config.NumberColumn(
                "Best Case (5% chance)",
                disabled=True,
                format="₹%.2f")
            }
        )

        # Display Simulation Chart
        sim_df.index = formatted_index

        st.pyplot(portfolio.plot_mc_gbm(sim_df))

else:
    st.info("No stocks in your portfolio. Add stocks above.")
