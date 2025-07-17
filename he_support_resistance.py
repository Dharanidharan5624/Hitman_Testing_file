import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import Tk, Frame, Label, Entry, Button
from tkinter.ttk import Combobox
from pytz import timezone
import matplotlib.dates as mdates
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
import numpy as np
from datetime import datetime
from mplfinance.original_flavor import candlestick_ohlc

# Timezone setup
us_eastern = timezone("America/New_York")

# GUI Setup
root = Tk()
root.title("Stock Chart Viewer (US Eastern Time)")
root.geometry("1100x600")

# UI Frame
top_frame = Frame(root)
top_frame.pack(pady=10)

Label(top_frame, text="Enter Stock Symbol: ").pack(side='left')
symbol_entry = Entry(top_frame)
symbol_entry.pack(side='left')

fetch_button = Button(top_frame, text="Search")
fetch_button.pack(side='left', padx=5)

Label(top_frame, text="Select Duration:").pack(side='left', padx=5)
duration_box = Combobox(
    top_frame,
    values=["1 Day", "1 Week", "2 Weeks", "1 Month", "3 Months", "6 Months", "9 Months", "1 Year", "All Year"],
    state="readonly"
)
duration_box.set("1 Year")
duration_box.pack(side='left', padx=5)

Label(top_frame, text="Chart Type:").pack(side='left', padx=5)
chart_type_box = Combobox(top_frame, values=["Line", "Candlestick"], state="readonly")
chart_type_box.set("Line")
chart_type_box.pack(side='left', padx=5)

# Title label above chart
title_label = Label(root, text="", font=("Arial", 15, "bold"))
title_label.pack(pady=(5, 0))

# Chart setup
fig, ax = plt.subplots(figsize=(10, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(expand=True, fill='both')
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
toolbar.pack(side="bottom", fill="x")

# Helpers
def to_decimal(val, places=2):
    if isinstance(val, (pd.Series, np.ndarray)):
        val = val.item()
    return float(Decimal(str(val)).quantize(Decimal(f'1.{"0"*places}'), rounding=ROUND_HALF_UP))

def localize(df):
    return df.tz_convert(us_eastern) if df.index.tzinfo else df.tz_localize("UTC").tz_convert(us_eastern)

# Zoom functionality
def zoom(event):
    base_scale = 1.1
    if event.inaxes != ax:
        return
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    xdata, ydata = event.xdata, event.ydata
    scale_factor = 1 / base_scale if event.button == 'up' else base_scale
    ax.set_xlim([xdata - (xdata - xlim[0]) * scale_factor, xdata + (xlim[1] - xdata) * scale_factor])
    ax.set_ylim([ydata - (ydata - ylim[0]) * scale_factor, ydata + (ylim[1] - ydata) * scale_factor])
    canvas.draw()

canvas.mpl_connect("scroll_event", zoom)

prev_xlim, prev_ylim = None, None

def fetch_and_plot(preserve_zoom=True):
    global prev_xlim, prev_ylim
    symbol = symbol_entry.get().upper().strip()
    if not symbol:
        ax.set_title("Please enter a stock symbol.", fontsize=12)
        canvas.draw()
        return

    if preserve_zoom:
        prev_xlim, prev_ylim = ax.get_xlim(), ax.get_ylim()
        
    ax.clear()

    duration = duration_box.get()
    chart_type = chart_type_box.get()
    if not duration or not chart_type:
        ax.set_title("Please select duration and chart type.", fontsize=12)
        canvas.draw()
        return

    current_time = datetime.now(us_eastern).strftime('%H:%M:%S')
    

    duration_map = {
        "1 Day":     ("1d", "5m", 100),
        "1 Week":    ("7d", "1d", 100),
        "2 Weeks":   ("14d", "1d", 150),
        "1 Month":   ("1mo", "1d", 25),
        "3 Months":  ("3mo", "1mo", 100),
        "6 Months":  ("6mo", "1mo", 150),
        "9 Months":  ("9mo", "1mo", 200),
        "1 Year":    ("1y", "1mo", 100),
        "All Year":  ("max", "1mo", 200)
    }

    period, interval, visible_window = duration_map.get(duration, ("1mo", "1d", 30))

    df = yf.download(symbol, period=period, interval=interval, auto_adjust=True)
    if df.empty or 'Close' not in df:
        ax.set_title("No data found", fontsize=12)
        canvas.draw()
        return

    df = localize(df[['Open', 'High', 'Low', 'Close']].dropna())
    df['Date'] = mdates.date2num(df.index.to_pydatetime())
    df_visible = df.iloc[-visible_window:]
    close = df_visible['Close']

    support = to_decimal(close.rolling(min(20, len(df_visible))).min().dropna().iloc[-1])
    resistance = to_decimal(close.rolling(min(20, len(df_visible))).max().dropna().iloc[-1])
    last_price = to_decimal(close.iloc[-1])
    last_time = df_visible.index[-1]
    lower_10 = to_decimal(last_price * 0.90)
    lower_15 = to_decimal(last_price * 0.85)

    if interval == "1m":
        candle_width = 0.0005
    elif interval == "5m":
        candle_width = 0.001
    elif interval == "1h":
        candle_width = 0.005
    elif interval == "1d":
        candle_width = 0.2
    elif interval == "1wk":
        candle_width = 0.5
    elif interval == "1mo":
        candle_width = 1.0
    elif interval == "1y":
        candle_width = 2.0
    elif interval == "max":
        candle_width = 10.0
    elif interval == "3mo":
        candle_width = 1.5
    elif interval == "6mo":
        candle_width = 2.0
    else:
        candle_width = 0.5

    if chart_type == "Line":
        ax.plot(df_visible.index, close, label=f"{symbol} Close", color='skyblue')
    else:
        ohlc = df_visible[['Date', 'Open', 'High', 'Low', 'Close']].values
        candlestick_ohlc(ax, ohlc, width=candle_width, colorup='green', colordown='red')

    ax.axhline(last_price, color='blue', linestyle='--', label=f'Current: ${last_price:.2f}')
    ax.axhline(resistance, color='darkred', linestyle='-.', label=f'Resistance: ${resistance:.2f}')
    ax.axhline(support, color='darkgreen', linestyle='-.', label=f'Support: ${support:.2f}')
    ax.axhline(lower_10, color='orange', linestyle='--', label=f'-10% Drop: ₹{lower_10:.2f}')
    ax.axhline(lower_15, color='purple', linestyle='--', label=f'-15% Drop: ₹{lower_15:.2f}')

    ax.text(last_time, resistance, f'Resistance - ${resistance:.2f}', va='bottom', ha='right', fontsize=9, color='darkred')
    ax.text(last_time, support, f'Support - ${support:.2f}', va='top', ha='right', fontsize=9, color='darkgreen')
    ax.text(last_time, last_price, f'${last_price:.2f}', va='center', ha='left', fontsize=9, color='blue')
    ax.text(last_time, lower_10, f'-10%↓ ₹{lower_10:.2f}', color='orange', va='bottom', ha='right', fontsize=8)
    ax.text(last_time, lower_15, f'-15%↓ ₹{lower_15:.2f}', color='purple', va='bottom', ha='right', fontsize=8)

    formatter_map = {
        "1 Day": mdates.DateFormatter('%b %d\n%H:%M', tz=us_eastern),
        "1 Month": mdates.DateFormatter('%d %b %Y'),
        "3 Months": mdates.DateFormatter('%d %b %Y'),
        "6 Months": mdates.DateFormatter('%b %Y'),
        "9 Months": mdates.DateFormatter('%b %Y'),
        "1 Year": mdates.DateFormatter('%b %Y'),
        "All Year": mdates.DateFormatter('%Y'),
        "default": mdates.DateFormatter('%d %b')
    }

    ax.xaxis.set_major_formatter(formatter_map.get(duration, formatter_map["default"]))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    ax.set_ylabel("Price (USD)")
    plt.xticks(rotation=45)
    ax.grid(True)

    if duration == "1 Day":
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    elif duration == "1 Year":
        ax.xaxis.set_major_locator(mdates.MonthLocator())
    elif duration == "All Year":
        ax.xaxis.set_major_locator(mdates.YearLocator())
    elif duration == "1 Month":
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    elif duration == "3 Months":
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    elif duration == "6 Months":
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    elif duration == "9 Months":
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    elif duration == "2 Weeks":
        ax.xaxis.set_major_locator(mdates.DayLocator())
    else:
        ax.xaxis.set_major_locator(mdates.DayLocator())

    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()

    title_text = f"{symbol} - {duration} US Eastern Time - {current_time} "
    ax.set_title("")  # optional
    title_label.config(text=title_text)

    if preserve_zoom and prev_xlim and prev_ylim:
        ax.set_xlim(prev_xlim)
        ax.set_ylim(prev_ylim)
    else:
        ax.set_xlim(df_visible.index[0], df_visible.index[-1])

    canvas.draw()

# Pan left/right
def pan_left(event=None):
    xlim = ax.get_xlim()
    delta = (xlim[1] - xlim[0]) * 0.1
    ax.set_xlim(xlim[0] - delta, xlim[1] - delta)
    canvas.draw()

def pan_right(event=None):
    xlim = ax.get_xlim()
    delta = (xlim[1] - xlim[0]) * 0.1
    ax.set_xlim(xlim[0] + delta, xlim[1] + delta)
    canvas.draw()

# Bindings
fetch_button.config(command=lambda: fetch_and_plot(preserve_zoom=False))
duration_box.bind("<<ComboboxSelected>>", lambda event: fetch_and_plot(preserve_zoom=False))
chart_type_box.bind("<<ComboboxSelected>>", lambda event: fetch_and_plot(preserve_zoom=False))
root.bind("<Left>", pan_left)
root.bind("<Right>", pan_right)

# Live refresh every 1 second
def live_updater():
    fetch_and_plot()
    root.after(100, live_updater)

fetch_and_plot(preserve_zoom=False)
live_updater()
root.mainloop()
