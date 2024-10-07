import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

# Function to get stock data
def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        current_price = stock.info['regularMarketPrice']
        
        # Get the low of the week
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        hist = stock.history(start=start_date, end=end_date)
        low_of_week = hist['Low'].min()
        
        return current_price, low_of_week
    except:
        return None, None

# Function to calculate position size
def calculate_position_size(portfolio_size, risk_percentage, entry_price, stop_loss):
    risk_amount = portfolio_size * (risk_percentage / 100)
    risk_per_share = entry_price - stop_loss
    shares = int(risk_amount / risk_per_share)
    position_size = shares * entry_price
    return risk_amount, risk_per_share, shares, position_size

# Main app
def main():
    st.set_page_config(page_title="Position Size Calculator", layout="wide")
    
    # Sidebar for navigation
    st.sidebar.title("Calculator Type")
    calculator_type = st.sidebar.radio("", ["Price-Based Stop Loss", "Percentage-Based Stop Loss"])
    
    if calculator_type == "Price-Based Stop Loss":
        price_based_calculator()
    else:
        percentage_based_calculator()

# Price-based stop loss calculator
def price_based_calculator():
    st.title("Position Size Calculator (Price-Based Stop Loss)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        symbol = st.text_input("Stock Symbol", value="AAPL")
        portfolio_size = st.number_input("Portfolio Size ($)", min_value=0.0, value=10000.0, step=100.0)
        risk_percentage = st.number_input("Risk Percentage (%)", min_value=0.0, max_value=100.0, value=1.0, step=0.1)
        use_low_of_week = st.checkbox("Use Low of Week", value=True)
    
    with col2:
        current_price, low_of_week = get_stock_data(symbol)
        
        if current_price and low_of_week:
            entry_price = st.number_input("Entry Price ($)", min_value=0.0, value=float(current_price), step=0.01)
            if use_low_of_week:
                stop_loss = st.number_input("Stop Loss Price ($)", min_value=0.0, value=float(low_of_week), step=0.01)
            else:
                stop_loss = st.number_input("Stop Loss Price ($)", min_value=0.0, value=float(current_price) * 0.95, step=0.01)
        else:
            entry_price = st.number_input("Entry Price ($)", min_value=0.0, value=100.0, step=0.01)
            stop_loss = st.number_input("Stop Loss Price ($)", min_value=0.0, value=95.0, step=0.01)
    
    if st.button("Calculate Position Size"):
        risk_amount, risk_per_share, shares, position_size = calculate_position_size(portfolio_size, risk_percentage, entry_price, stop_loss)
        
        st.subheader("Results")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Symbol: {symbol}")
            st.write(f"Portfolio Size: ${portfolio_size:,.2f}")
            st.write(f"Risk Amount: ${risk_amount:,.2f}")
            st.write(f"Entry Price: ${entry_price:.2f}")
            st.write(f"Stop Loss: ${stop_loss:.2f}")
        with col2:
            st.write(f"Risk Per Share: ${risk_per_share:.2f}")
            st.write(f"Shares: {shares}")
            st.write(f"Position Size: ${position_size:,.2f}")

# Percentage-based stop loss calculator
def percentage_based_calculator():
    st.title("Position Size Calculator (Percentage-Based Stop Loss)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        symbol = st.text_input("Stock Symbol", value="AAPL")
        portfolio_size = st.number_input("Portfolio Size ($)", min_value=0.0, value=10000.0, step=100.0)
        risk_percentage = st.number_input("Risk Percentage (%)", min_value=0.0, max_value=100.0, value=1.0, step=0.1)
    
    with col2:
        current_price, _ = get_stock_data(symbol)
        
        if current_price:
            entry_price = st.number_input("Entry Price ($)", min_value=0.0, value=float(current_price), step=0.01)
        else:
            entry_price = st.number_input("Entry Price ($)", min_value=0.0, value=100.0, step=0.01)
        
        stop_loss_percentage = st.number_input("Stop Loss (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1)
    
    if st.button("Calculate Position Size"):
        stop_loss = entry_price * (1 - stop_loss_percentage / 100)
        risk_amount, risk_per_share, shares, position_size = calculate_position_size(portfolio_size, risk_percentage, entry_price, stop_loss)
        
        st.subheader("Results")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Symbol: {symbol}")
            st.write(f"Portfolio Size: ${portfolio_size:,.2f}")
            st.write(f"Risk Amount: ${risk_amount:,.2f}")
            st.write(f"Entry Price: ${entry_price:.2f}")
            st.write(f"Stop Loss (%): {stop_loss_percentage:.2f}%")
        with col2:
            st.write(f"Stop Loss Price: ${stop_loss:.2f}")
            st.write(f"Risk Per Share: ${risk_per_share:.2f}")
            st.write(f"Shares: {shares}")
            st.write(f"Position Size: ${position_size:,.2f}")

if __name__ == "__main__":
    main()
