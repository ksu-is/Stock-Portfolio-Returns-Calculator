import yfinance as yf

def get_stock_data(ticker, shares, buy_price):
    stock = yf.Ticker(ticker)
    try:
        current_price = stock.info["currentPrice"]
        total_cost = shares * buy_price
        current_value = shares * current_price
        profit_or_loss = current_value - total_cost

        return {
            "ticker": ticker,
            "shares": shares,
            "buy_price": buy_price,
            "current_price": current_price,
            "total_cost": total_cost,
            "current_value": current_value,
            "profit_or_loss": profit_or_loss
        }

    except KeyError:
        print(f"Unable to retrieve data for {ticker}. Skipping.")
        return None


def main():
    portfolio = []

    while True:
        ticker = input("\nEnter a stock ticker (or type 'done' to finish): ").upper()
        if ticker == "DONE":
            break

        try:
            shares = float(input(f"How many shares of {ticker} do you own? "))
            buy_price = float(input(f"What price did you buy {ticker} at? "))
            stock_data = get_stock_data(ticker, shares, buy_price)
            if stock_data:
                portfolio.append(stock_data)
        except ValueError:
            print("Invalid input. Try again.")

    # Display portfolio summary
    if portfolio:
        total_cost = 0
        total_value = 0
        print("\n----- Portfolio Summary -----")
        for stock in portfolio:
            print(f"\n{stock['ticker']}")
            print(f"  Shares Owned: {stock['shares']}")
            print(f"  Buy Price: ${stock['buy_price']:.2f}")
            print(f"  Current Price: ${stock['current_price']:.2f}")
            print(f"  Total Cost: ${stock['total_cost']:.2f}")
            print(f"  Current Value: ${stock['current_value']:.2f}")
            print(f"  Profit/Loss: ${stock['profit_or_loss']:.2f}")
            total_cost += stock['total_cost']
            total_value += stock['current_value']

        total_pl = total_value - total_cost
        print("\n=============================")
        print(f"Total Cost: ${total_cost:.2f}")
        print(f"Total Current Value: ${total_value:.2f}")
        print(f"Total Profit/Loss: ${total_pl:.2f}")
    else:
        print("No stocks were entered.")

main()
