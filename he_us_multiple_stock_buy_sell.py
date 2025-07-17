import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from datetime import datetime
from pytz import timezone
import matplotlib.dates as mdates
from decimal import Decimal, ROUND_HALF_UP
from ib_insync import *

# === Constants and Globals ===
us_eastern = timezone("US/Eastern")
BUY_LEVELS = ['61.8%', '78.6%']
SELL_LEVELS = ['38.2%', '23.6%']
SYMBOLS = ['AAPL', 'MSFT', 'GOOGL', 'SPY', 'META', 'NVDA', 'AMZN','PLTR'] 
QUANTITY = 10
selected_symbol = 'PLTR'
buttons = []
contract = None
bought = False
sold = False
refresh_interval = 150

# === Simulated Prices ===


# === Connect to IBKR ===
ib = IB()
try:
    ib.connect('127.0.0.1', 7497, clientId=2)
except Exception as e:
    print(f"Connection failed: {e}")

ib.reqMarketDataType(1)

# === Utilities ===
def to_decimal(value, places=2):
    return float(Decimal(value).quantize(Decimal(f'1.{"0"*places}'), rounding=ROUND_HALF_UP))

    # === GET REAL-TIME PRICE USING YFINANCE ===
def get_live_price_from_yf():
    try:
        ticker = yf.Ticker(selected_symbol)
        live_data = ticker.history(period="1d", interval="1m")
        if not live_data.empty:
            live_price = live_data['Close'].iloc[-1]
            return float(live_price)
        else:
            print(" No live data available.")
            return None
    except Exception as e:
        print(f" Error fetching live price: {e}")
        return None
def place_order(action, quantity, price):
    order = MarketOrder(action, quantity)
    ib.placeOrder(contract, order)
    print(f"{action.capitalize()} order placed: {quantity} shares at ${price:.2f}")

# === Plotting Setup ===
fig, ax = plt.subplots(figsize=(11, 8))
plt.subplots_adjust(left=0.06, right=0.88, bottom=0.10)
plt.ion()

# === Fibonacci Chart ===
def plot_fib_chart(symbol):
    global selected_symbol, contract
    selected_symbol = symbol
    ax.clear()

    now_est = datetime.now(us_eastern)
    df = yf.download(symbol, period='1d', interval='1m', auto_adjust=True, progress=False)
    df.dropna(inplace=True)
    df.index = df.index.tz_convert('America/New_York')
    df = df.between_time("09:30", "16:00")

    if df.empty or len(df) < 10:
        ax.set_title(f"[{symbol}] Not enough data")
        plt.draw()
        return {}

    swing_high = to_decimal(df['High'].max().item())
    swing_low = to_decimal(df['Low'].min().item())
    latest_price = to_decimal(df['Close'].iloc[-1].item())
    diff = swing_high - swing_low

    fib_levels = {
        '23.6%': to_decimal(swing_high - 0.236 * diff),
        '38.2%': to_decimal(swing_high - 0.382 * diff),
        '61.8%': to_decimal(swing_high - 0.618 * diff),
        '78.6%': to_decimal(swing_high - 0.786 * diff),
    }

    ax.plot(df.index, df['Close'], label=f'{symbol} Close', color='skyblue')
    #ax.axhline(swing_high, color='green', linestyle='--', label=f'Swing High: ${swing_high:.2f}')
    #ax.axhline(swing_low, color='yellow', linestyle='--', label=f'Swing Low: ${swing_low:.2f}')
    ax.axhline(latest_price, color='blue', linestyle='--', linewidth=1.5, label=f'Current Price: ${latest_price:.2f}')

    for level, price in fib_levels.items():
        color = 'green' if level in BUY_LEVELS else 'red' if level in SELL_LEVELS else 'gray'
        ax.axhline(price, linestyle='--', linewidth=1.5, color=color, alpha=0.7, label=f'{level}: ${price:.2f}')
        ax.text(df.index[-1], price, f'{level} - ${price:.2f}', va='bottom', ha='right', fontsize=10)

    ax.set_title(f'{symbol} Intraday Fibonacci Levels (ET: {now_est.strftime("%H:%M:%S")})')
    ax.set_xlabel('Time (Eastern)')
    ax.set_ylabel('Price (USD)')
    ax.legend(loc='best')
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('[%m/%d]\n %I:%M', tz=us_eastern))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))

    fig.autofmt_xdate()
    plt.draw()

    # Update IBKR contract
    contract = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(contract)

    return fib_levels

# === Button System ===
visible_buttons = 12
current_page = [0]
button_width = 0.10
button_height = 0.05
spacing = 0.01
start_x = 0.89
start_y = 0.82

def render_buttons(page):
    for btn in buttons:
        btn.ax.remove()
    buttons.clear()

    start_index = page * visible_buttons
    end_index = start_index + visible_buttons
    visible_symbols = SYMBOLS[start_index:end_index]

    for i, symbol in enumerate(visible_symbols):
        y_pos = start_y - i * (button_height + spacing)
        ax_button = plt.axes([start_x, y_pos, button_width, button_height])
        btn = Button(ax_button, symbol)
        btn.on_clicked(lambda event, sym=symbol: plot_fib_chart(sym))
        buttons.append(btn)
    plt.draw()

def scroll_up(event):
    if current_page[0] > 0:
        current_page[0] -= 1
        render_buttons(current_page[0])

def scroll_down(event):
    if (current_page[0] + 1) * visible_buttons < len(SYMBOLS):
        current_page[0] += 1
        render_buttons(current_page[0])

ax_up = plt.axes([start_x, start_y + 0.07, button_width, button_height])
btn_up = Button(ax_up, "↑")
btn_up.on_clicked(scroll_up)

ax_down = plt.axes([start_x, start_y - visible_buttons * (button_height + spacing) - 0.06, button_width, button_height])
btn_down = Button(ax_down, "↓")
btn_down.on_clicked(scroll_down)

# === Init ===
render_buttons(current_page[0])
fib_levels = plot_fib_chart(selected_symbol)

# === Main Loop ===
while True:
    fib_levels = plot_fib_chart(selected_symbol)
    live_price = get_live_price_from_yf()
    if live_price is None:
        print("No more prices. Exiting.")
        break

    print(f"\nLive Price: ${live_price:.2f}")

    # === Buy Logic ===
    if not bought:
        for level in BUY_LEVELS:
            level_price = fib_levels.get(level)
            if level_price and live_price <= level_price:
                print(f"Buy triggered at {level} — Price: ${live_price:.2f}")
                place_order('BUY', QUANTITY, live_price)
                bought = True
                break
        else:
            print("No buy signal yet.")

    # === Sell Logic ===
    elif bought and not sold:
        for level in SELL_LEVELS:
            level_price = fib_levels.get(level)
            if level_price and live_price >= level_price:
                print(f"Sell triggered at {level} — Price: ${live_price:.2f}")
                place_order('SELL', QUANTITY, live_price)
                sold = True
                break
        else:
            print("No sell signal yet.")

    if bought and sold:
        print("Trade completed: bought and sold.")
        break

    plt.pause(refresh_interval)
