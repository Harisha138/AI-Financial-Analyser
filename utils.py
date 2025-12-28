# utils.py

import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

def getStockTickers():
    """Returns a list of pre-defined stock tickers."""
    return ["NVDA", "AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "JPM"]

def getCandlestickChartData(ticker: str):
    """
    Fetches historical stock data and generates a candlestick chart.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        tuple: A pandas DataFrame with historical data and a Plotly Figure.
    """
    try:
        ticker = ticker.replace("$", "").strip().upper()
        stock = yf.Ticker(ticker)
        # Fetch 1 year of historical data
        historicalData = stock.history(period="1y")

        # Check if data was returned
        if historicalData.empty:
            return pd.DataFrame(), go.Figure().update_layout(title_text=f"No data found for {ticker}")

        # Reset index to make 'Date' a column
        historicalData.reset_index(inplace=True)
        historicalData['Date'] = pd.to_datetime(historicalData['Date'])

        # Create the candlestick chart
        candlestickChart = go.Figure(
            data=[
                go.Candlestick(
                    x=historicalData['Date'],
                    open=historicalData['Open'],
                    high=historicalData['High'],
                    low=historicalData['Low'],
                    close=historicalData['Close'],
                    name=ticker
                )
            ]
        )
        candlestickChart.update_layout(
            title_text=f"{ticker} Candlestick Chart (Last Year)",
            xaxis_title="Date",
            yaxis_title="Stock Price (USD)",
            xaxis_rangeslider_visible=False
        )

        # Prepare data for display (set Date as index)
        historicalData_display = historicalData.set_index('Date')
        return historicalData_display, candlestickChart

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame(), go.Figure().update_layout(title_text=f"Error fetching data for {ticker}")