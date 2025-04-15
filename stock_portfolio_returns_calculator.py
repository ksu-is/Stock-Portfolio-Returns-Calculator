import yfinance as yf

def get_stock_data(ticker, shares, buy_price):
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        current_price = info["currentPrice"]
        sector = info.get("sector", "N/A")
        market_cap = info.get("marketCap", None)

        total_cost = shares * buy_price
        current_value = shares * current_price
        profit_or_loss = current_value - total_cost
        return_pct = (profit_or_loss / total_cost) * 100 if total_cost != 0 else 0

        return {
            "ticker": ticker,
            "shares": shares,
            "buy_price": buy_price,
            "current_price": current_price,
            "total_cost": total_cost,
            "current_value": current_value,
            "profit_or_loss": profit_or_loss,
            "return_pct": return_pct,
            "sector": sector,
            "market_cap": market_cap
        }

    except KeyError:
        print(f"Unable to retrieve data for {ticker}. Skipping.")
        return None
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

def show_moving_average_and_volume(ticker, ma_choice):
    stock = yf.Ticker(ticker)

    # Moving average
    ma = None
    if ma_choice == "50":
        ma = stock.info.get("fiftyDayAverage", None)
        if ma:
            print(f"50-Day Moving Average for {ticker}: ${ma:.2f}")
        else:
            print("50-Day Moving Average data not available.")
    elif ma_choice == "200":
        ma = stock.info.get("twoHundredDayAverage", None)
        if ma:
            print(f"200-Day Moving Average for {ticker}: ${ma:.2f}")
        else:
            print("200-Day Moving Average data not available.")

    # Volume
    volume = stock.info.get("volume", None)
    if volume:
        print(f"Current Share Volume for {ticker}: {volume:,}")
    else:
        print("Volume data not available.")

def main():
    portfolio = []

    while True:
        ticker = input("\nEnter a stock ticker (or type 'done' to finish): ").upper()
        if ticker == "DONE":
            break

        try:
            shares = float(input(f"How many shares of {ticker} do you own? "))
            buy_price = float(input(f"What price did you buy {ticker} at? "))

            # Ask for moving average choice
            ma_choice = input(
                f"Would you like to view a moving average for {ticker}?\n"
                "Type '50' for 50-day, '200' for 200-day, or press Enter to skip: "
            ).strip()
            if ma_choice in ["50", "200"]:
                show_moving_average_and_volume(ticker, ma_choice)

            # Get and store stock data
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
            print(f"  Sector: {stock['sector']}")
            print(f"  Market Cap: {stock['market_cap']:,}" if stock['market_cap'] else "  Market Cap: N/A")
            print(f"  Shares Owned: {stock['shares']}")
            print(f"  Buy Price: ${stock['buy_price']:.2f}")
            print(f"  Current Price: ${stock['current_price']:.2f}")
            print(f"  Total Cost: ${stock['total_cost']:.2f}")
            print(f"  Current Value: ${stock['current_value']:.2f}")
            print(f"  Profit/Loss: ${stock['profit_or_loss']:.2f}")
            print(f"  Return: {stock['return_pct']:.2f}%")
            total_cost += stock['total_cost']
            total_value += stock['current_value']

        total_pl = total_value - total_cost
        total_return_pct = (total_pl / total_cost) * 100 if total_cost != 0 else 0
        print("\n=============================")
        print(f"Total Cost: ${total_cost:.2f}")
        print(f"Total Current Value: ${total_value:.2f}")
        print(f"Total Profit/Loss: ${total_pl:.2f}")
        print(f"Total Return: {total_return_pct:.2f}%")
    else:
        print("No valid stocks were entered.")

main()
