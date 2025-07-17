import pandas as pd
from datetime import datetime
from collections import deque, defaultdict
import yfinance as yf
from tabulate import tabulate
import mysql.connector

def fetch_fifo_data():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="123", database="hitman"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ticker, date, trade_type, quantity, price, platform
            FROM test_stock_transaction;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        print("\n📥 Fetched Transactions:")
        print(tabulate(rows, headers=["Ticker", "Date", "Type", "Qty", "Price", "Platform"], tablefmt="grid"))

        return rows

    except mysql.connector.Error as err:
        print(f"❌ Database Error: {err}")
        return []

# Group transactions by ticker
grouped = defaultdict(list)
platform_map = {}

for t in fetch_fifo_data():
    if len(t) != 6:
        print(f"⚠️ Skipping invalid row (length != 6): {t}")
        continue

    ticker, date_obj, action, qty, price, platform = t

    if not all([ticker, date_obj, action, qty, price, platform]):
        print(f"⚠️ Skipping row with missing values: {t}")
        continue

    try:
        date_str = date_obj.strftime("%Y-%m-%d")
        grouped[ticker].append((
            date_str,
            ticker,
            action.strip().lower(),
            float(qty),
            float(price),
            platform
        ))
        platform_map[ticker] = platform
    except Exception as e:
        print(f"⚠️ Error processing row {t}: {e}")
        continue

# Fetch benchmark index returns
def get_index_return(ticker):
    hist = yf.Ticker(ticker).history(period="1y")
    if hist.empty:
        return None
    start_price = hist['Close'].iloc[0]
    end_price = hist['Close'].iloc[-1]
    return round((end_price - start_price) / start_price * 100, 2)

sp500_return = get_index_return("^GSPC")
nasdaq_return = get_index_return("^IXIC")
russell1000_return = get_index_return("^RUI")

# Prepare final summary
summary_list = []

for ticker, txns in grouped.items():
    holdings = deque()
    cumulative_buy_cost = 0
    total_qty = 0
    realized_gain_loss = 0
    first_buy_date = None

    stock = yf.Ticker(ticker)
    hist = stock.history(period="260d")

    if hist.empty or 'Close' not in hist:
        print(f"⚠️ No price data for {ticker}")
        continue

    ema_50 = round(hist['Close'].ewm(span=50, adjust=False).mean().iloc[-1], 2)
    ema_100 = round(hist['Close'].ewm(span=100, adjust=False).mean().iloc[-1], 2)
    ema_200 = round(hist['Close'].ewm(span=200, adjust=False).mean().iloc[-1], 2)

    try:
        info = stock.info
        current_price = info.get('currentPrice', 0.0)
        category = info.get('sector', 'Unknown')
    except:
        info = {}
        current_price = 0.0
        category = "Unknown"

    for date_str, symbol, action, qty, price, platform in txns:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except Exception as e:
            print(f"⚠️ Invalid date format: {date_str} in {symbol} — {e}")
            continue

        if action == 'buy':
            if not first_buy_date:
                first_buy_date = date
            holdings.append([qty, price, date])
            total_qty += qty
            cumulative_buy_cost += qty * price

        elif action == 'sell':
            sell_qty = qty
            while sell_qty > 0 and holdings:
                h_qty, h_price, h_date = holdings[0]
                used_qty = min(sell_qty, h_qty)
                profit = (price - h_price) * used_qty
                realized_gain_loss += profit
                cumulative_buy_cost -= used_qty * h_price
                total_qty -= used_qty
                if used_qty == h_qty:
                    holdings.popleft()
                else:
                    holdings[0][0] -= used_qty
                sell_qty -= used_qty

    avg_cost = cumulative_buy_cost / total_qty if total_qty else 0
    total_cost = cumulative_buy_cost
    unrealized = (current_price - avg_cost) * total_qty if total_qty else 0

    today = datetime.today()
    first_buy_age = (today - first_buy_date).days if first_buy_date else "-"
    average_age = (
        sum((today - h[2]).days * h[0] for h in holdings) / total_qty
        if total_qty > 0 else "-"
    )

    summary_list.append({
        "Ticker": ticker,
        "Category": category,
        "Quantity": total_qty,
        "Average Cost p/u": round(avg_cost, 2),
        "Total Cost": round(total_cost, 2),
        "Current Price": round(current_price, 2),
        "Unrealized Gains/Loss": round(unrealized, 2),
        "Realized Gains/Loss": round(realized_gain_loss, 2),
        "First Buy Age (Days)": first_buy_age,
        "Average Age (Days)": round(average_age, 1) if isinstance(average_age, float) else average_age,
        "Platform": platform_map[ticker],
        'industry_pe': info.get('trailingPE'),
        'curent_pe': info.get('forwardPE'),
        'price_sales_ratio': info.get('priceToSalesTrailing12Months'),
        'price_book_ratio': info.get('priceToBook'),
        "50-day EMA": ema_50,
        "100-day EMA": ema_100,
        "200-day EMA": ema_200,
        'sp_500_ya': sp500_return,
        'nashdaq_ya': nasdaq_return,
        'russel_1000_ya': russell1000_return
    })

# Convert to DataFrame
df = pd.DataFrame(summary_list)

# Calculate position size
if not df.empty:
    df['position_size'] = (df['Total Cost'] / df['Total Cost'].sum()).round(2)

    # Reorder columns
    df = df[[ 
        "Ticker", "Category",  "Quantity", "Average Cost p/u","position_size", "Total Cost",
        "Current Price", "Unrealized Gains/Loss", "Realized Gains/Loss",
        "First Buy Age (Days)", "Average Age (Days)", "Platform", "industry_pe", "curent_pe",
        "price_sales_ratio", "price_book_ratio", "50-day EMA", "100-day EMA", "200-day EMA",
        'sp_500_ya', 'nashdaq_ya', 'russel_1000_ya'
    ]]

    print("\n📊 Portfolio Summary:")
    print(tabulate(df, headers="keys", tablefmt="grid"))

    # Insert into MySQL
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="123", database="hitman"
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO test_potfolio_master (
 `ticker`, `Category`, `quantity`, `avg_cost`, `position_size`, `total_cost`, `current_price`, `unrealized_gain_loss`, `relized_gain_loss`, `first_buy_age`, `avg_age_days`, `platform`, `industry_pe`, `curent_pe`, `price_sales_ratio`, `price_book_ratio`, `50_day_ema`, `100_day_ema`, `200_day_ema`, `sp_500_ya`, `nashdaq_ya`, `russel_1000_ya`
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data_to_insert = [tuple(row) for row in df.itertuples(index=False)]

        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Portfolio summary inserted into database.")

    except mysql.connector.Error as err:
        print(f"❌ MySQL Error during insertion: {err}")

else:
    print("⚠️ No data available to display or insert.")
