# AI use notice. ChatGPT was used to assist with the code.
import yfinance as yf

def get_stock_data(ticker, shares, buy_price):
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        current_price = info["currentPrice"]
        sector = info.get("sector", "N/A")
        market_cap = info.get("marketCap", None)
        beta = info.get("beta", None)

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
            "market_cap": market_cap,
            "beta": beta
        }

    except KeyError:
        print(f"Unable to retrieve data for {ticker}. Skipping.")
        return None
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


def show_moving_average_and_volume(ticker, ma_choice):
    stock = yf.Ticker(ticker)

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

    volume = stock.info.get("volume", None)
    if volume:
        print(f"Current Share Volume for {ticker}: {volume:,}")
    else:
        print("Volume data not available.")

def assess_market_condition():
    try:
        dow = yf.Ticker("^DJI")
        hist = dow.history(period="2d")
        if len(hist) < 2:
            return "Unable to assess the market today."
        yesterday_close = hist["Close"].iloc[-2]
        today_close = hist["Close"].iloc[-1]
        pct_change = ((today_close - yesterday_close) / yesterday_close) * 100

        if pct_change > 0.5:
            return f"Market Status: Good 📈 (DJIA change: {pct_change:.2f}%)"
        elif pct_change < -0.5:
            return f"Market Status: Bad 📉 (DJIA change: {pct_change:.2f}%)"
        else:
            return f"Market Status: Mediocre ⚖️ (DJIA change: {pct_change:.2f}%)"
    except Exception as e:
        return f"Could not retrieve market data: {e}"

def main():
    print("\n===== STOCK MARKET CHECK =====")
    print(assess_market_condition())

    portfolio = []

    while True:
        ticker = input("\nEnter a stock ticker (or type 'done' to finish): ").upper()
        if ticker == "DONE":
            break

        try:
            shares = float(input(f"How many shares of {ticker} do you own? "))
            buy_price = float(input(f"What price did you buy {ticker} at? "))

            ma_choice = input(
                f"Would you like to view a moving average for {ticker}?\n"
                "Type '50' for 50-day, '200' for 200-day, or press Enter to skip: "
            ).strip()
            if ma_choice in ["50", "200"]:
                show_moving_average_and_volume(ticker, ma_choice)

            stock_data = get_stock_data(ticker, shares, buy_price)
            if stock_data:
                portfolio.append(stock_data)
        except ValueError:
            print("Invalid input. Try again.")

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
            print(f"  Beta: {stock['beta']:.2f}" if stock['beta'] is not None else "  Beta: N/A")
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
