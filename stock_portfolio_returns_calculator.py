import yfinance as yf

def get_current_stock_price():
    ticker = input("Enter the stock ticker symbol (e.g., AAPL, TSLA, MSFT): ").upper()
    stock = yf.Ticker(ticker)
    try:
        price = stock.info["currentPrice"]
        print(f"The current price of {ticker} is: ${price}")
    except KeyError:
        print(f"Unable to retrieve the current price for {ticker}. The ticker may be invalid or unavailable.")

get_current_stock_price()