import yfinance as yf
import pandas as pd
import numpy as np
from tabulate import tabulate
import mysql.connector
print(dir(yf))
def get_stock_data(symbol: str):
    try:
        stock = yf.Ticker(symbol)
        balance_sheet = stock.balance_sheet
        income_stmt = stock.financials
        df = stock.history(period="3mo")

        if df.empty:
            print("No stock data available. Check symbol or network.")
            return [None] * 28

        closing_prices = df["Close"].dropna().tolist()[-15:]
        current_price = closing_prices[-1] if closing_prices else None

        stock_info = stock.info
        eps = stock_info.get("trailingEps")
        bvps = stock_info.get("bookValue")
        revenue_ttm = stock_info.get("totalRevenue")
        market_cap = stock_info.get("marketCap")
        growth_rate = stock_info.get("earningsGrowth")
        ebitda = stock_info.get("ebitda")
        enterprise_value = stock_info.get("enterpriseValue")
        cogs = stock_info.get("costOfRevenue")
        operating_income = stock_info.get("operatingIncome")
        total_assets = stock_info.get("totalAssets")
        net_income = stock_info.get("netIncome")
        total_equity = stock_info.get("totalStockholderEquity")
        possible_assets = ["Total Current Assets", "Current Assets"]
        possible_liabilities = ["Total Current Liabilities", "Current Liabilities"]
        inventory_keys = ["Inventory"]
        assets_keys = ["Total Current Assets", "Current Assets"]
        inventory_keys = ["Inventory"]
        liabilities_keys = ["Total Current Liabilities", "Current Liabilities"]
        total_debt = balance_sheet.loc["Total Debt"].iloc[0]  # Most recent value
        equity = balance_sheet.loc["Ordinary Shares Number"].iloc[0]  # Total Shareholders' Equity
        ebit = income_stmt.loc["Operating Income"].iloc[0]  # Most recent EBIT
        interest_expense = income_stmt.loc["Interest Expense"].iloc[0]  # Most recent interest cost
        revenue = income_stmt.loc["Total Revenue"].iloc[0]  # Most recent revenue
        total_assets_current = balance_sheet.loc["Total Assets"].iloc[0]  # Most recent total assets
        total_assets_previous = balance_sheet.loc["Total Assets"].iloc[1]  # Previous period total assets (if available)
        cogs = income_stmt.loc["Cost Of Revenue"].iloc[0]  # Most recent COGS
        inventory_current = balance_sheet.loc["Inventory"].iloc[0]  # Most recent Inventory
        inventory_previous = balance_sheet.loc["Inventory"].iloc[1]  # Previous period Inventory (if available)
        net_income_keys = ["Net Income", "Net Income Applicable To Common Shares"]
        equity_keys = ["Total Stockholder Equity", "Common Stock Equity"]
        ar_keys = ["Net Receivables", "Accounts Receivable"]
        accounts_receivable = None
        inst_ownership = stock.info.get("heldPercentInstitutions", None)
        insider_ownership = stock.info.get("heldPercentInsiders", None)  # Insider ownership %
        cash_flow = stock.cashflow 


        
        # Fetch Total Assets
        if total_assets is None:
            try:
                total_assets = balance_sheet.loc["Total Assets"].iloc[0]
            except:
                total_assets = None
        
        if operating_income is None:
            try:
                operating_income = income_stmt.loc["Operating Income"].iloc[0]
            except:
                operating_income = None

        if net_income is None:
            try:
                net_income = income_stmt.loc["Net Income"].iloc[0]
            except:
                net_income = None

        if total_equity is None:
            try:
                total_equity = balance_sheet.loc["Total Stockholder Equity"].iloc[0]
            except:
                total_equity = None
        
        eps_previous = stock_info.get("forwardEps")
        eps_growth = ((eps - eps_previous) / eps_previous * 100) if eps and eps_previous else None
        eps_growth = f"{round(eps_growth, 2):.2f}"

        try:
            revenue_current = income_stmt.loc["Total Revenue"].iloc[0]
            revenue_previous = income_stmt.loc["Total Revenue"].iloc[1]
            yoy_growth = ((revenue_current - revenue_previous) / revenue_previous) * 100
            yoy_growth = f"{round(yoy_growth, 2):.2f}"
        except:
            yoy_growth = None
        for asset_key in possible_assets:
            if asset_key in balance_sheet.index:
                current_assets = balance_sheet.loc[asset_key].iloc[0]
                break
        
        for liability_key in possible_liabilities:
            if liability_key in balance_sheet.index:
                current_liabilities = balance_sheet.loc[liability_key].iloc[0]
                break
             # If any of the values are missing
        if current_assets is None or current_liabilities is None or current_liabilities == 0:
            return f"{symbol}: Current Ratio = Data Unavailable"

        # Calculate Current Ratio
        current_ratio = round(current_assets / current_liabilities,2)
        current_ratio = f"{round(current_ratio, 2):.2f}"

        
        # Extract values (use next() to get first available value)
        current_assets = next((balance_sheet.loc[key].iloc[0] for key in assets_keys if key in balance_sheet.index), None)
        inventory = next((balance_sheet.loc[key].iloc[0] for key in inventory_keys if key in balance_sheet.index), 0)  # Default to 0 if missing
        current_liabilities = next((balance_sheet.loc[key].iloc[0] for key in liabilities_keys if key in balance_sheet.index), None)

        quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities else None
        quick_ratio = f"{round(quick_ratio, 2):.2f}"
      
        
        # Calculate Debt-to-Equity Ratio
        if equity is None or equity == 0:
            return None  

        # Calculate Debt-to-Equity Ratio
        de_ratio = total_debt / equity
        de_ratio = f"{round(de_ratio, 2):.2f}"
        # Calculate Interest Coverage Ratio
        if interest_expense is None or interest_expense == 0:
            return None         
        icr = ebit / interest_expense
        icr = f"{round(icr, 2):.2f}"

        # Calculate Asset Turnover Ratio
        average_assets = (total_assets_current + total_assets_previous) / 2
        if average_assets is None or average_assets == 0:
            return None
        asset_turnover = revenue / average_assets
        asset_turnover = f"{round(asset_turnover, 2):.2f}"

        # Calculate Inventory Turnover Ratio
        average_inventory = (inventory_current + inventory_previous) / 2
        if average_inventory is None or average_inventory == 0:
            return None  
        inventory_turnover = cogs / average_inventory
        inventory_turnover = f"{round(inventory_turnover, 2):.2f}"

           # Calculate DSO
        for key in ar_keys:
            if key in balance_sheet.index:
                accounts_receivable = balance_sheet.loc[key].iloc[0]
                break  # Stop if a valid key is found
        if accounts_receivable is None:
            print(f"Warning: Accounts Receivable data not available for {stock_symbols}")
            return None  # Exit if AR is missing
        # Get Total Revenue
        revenue = income_stmt.loc["Total Revenue"].iloc[0]
        # Check for missing or zero revenue
        if revenue is None or revenue == 0:
            print(f"Warning: Revenue data not available for {stock_symbols}")
            return None  
        dso = (accounts_receivable * 365) / revenue
        dso = f"{round(dso, 2):.2f}"

        
        # Calculate ROE

        net_income = next((income_stmt.loc[key].iloc[0] for key in net_income_keys if key in income_stmt.index), None)
        total_equity = next((balance_sheet.loc[key].iloc[0] for key in equity_keys if key in balance_sheet.index), None)
        if net_income is None:
            print(f"Warning: Net Income data not available for {stock_symbols}")
            return None
        if total_equity is None or total_equity == 0:
            print(f"Warning: Shareholders' Equity data not available for {stock_symbols}")
            return None  
        roe = (net_income / total_equity) * 100  # Convert to percentage
        roe = f"{round(roe, 2):.2f}"


        
        if insider_ownership is not None:
          insider_ownership= insider_ownership * 100 
          insider_ownership = f"{round(insider_ownership, 2):.2f}%"
        


        if inst_ownership is not None:
            inst_ownership = inst_ownership * 100 
            inst_ownership = f"{round(inst_ownership, 2):.2f}%"



        operating_cash_flow = cash_flow.loc["Cash Flow From Continuing Operating Activities"].iloc[0] if "Cash Flow From Continuing Operating Activities" in cash_flow.index else None
        operating_cash_flow = f"{round(operating_cash_flow, 2):.2f}"







    
        return df, closing_prices, current_price, eps, bvps, revenue_ttm, market_cap, growth_rate, ebitda, enterprise_value, cogs, net_income, operating_income, total_assets, total_equity, roe,eps_growth, yoy_growth,operating_cash_flow,current_ratio,quick_ratio,de_ratio,icr,asset_turnover,inventory_turnover,dso,insider_ownership,inst_ownership
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return [None] * 28

# Financial Ratio Calculation Functions
def calculate_pe_ratio(price, eps):
    return round(price / eps, 2) if eps and eps > 0 else None

def calculate_pb_ratio(price, bvps):
    return round(price / bvps, 2) if bvps and bvps > 0 else None

def calculate_ps_ratio(market_cap, revenue_ttm):
    return round(market_cap / revenue_ttm, 2) if market_cap and revenue_ttm and revenue_ttm > 0 else None

def calculate_peg_ratio(pe_ratio, growth_rate):
    return round(pe_ratio / (growth_rate * 100), 2) if pe_ratio and growth_rate and growth_rate > 0 else None

def calculate_ev_ebitda(enterprise_value, ebitda):
    return round(enterprise_value / ebitda, 2) if enterprise_value and ebitda and ebitda > 0 else None

def calculate_gross_margin(revenue, cogs):
    if revenue is None or revenue <= 0:
        return "N/A"
    if cogs is None:
        estimated_cogs = revenue * 0.5  
        return round(((revenue - estimated_cogs) / revenue) * 100, 2)
    return round(((revenue - cogs) / revenue) * 100, 2)

def calculate_net_profit_margin(revenue, net_income):
    if revenue is None or revenue <= 0 or net_income is None:
        return "N/A"
    return round((net_income / revenue) * 100, 2)

def get_operating_margin(revenue, operating_income):
    return round((operating_income / revenue) * 100, 2) if revenue and operating_income else None

def calculate_roa(net_income, total_assets):
    return round((net_income / total_assets) * 100, 2) if net_income and total_assets else None

# Technical Indicator Calculation Functions
def calculate_sma(stock_prices):
    return round(sum(stock_prices) / len(stock_prices), 2) if stock_prices else None

def calculate_macd(df):
    df["Short EMA"] = df["Close"].ewm(span=12, adjust=False).mean()
    df["Long EMA"] = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["Short EMA"] - df["Long EMA"]
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    return round(df["MACD"].iloc[-1], 2), round(df["Signal"].iloc[-1], 2)

def calculate_adx(df):
    if df.shape[0] < 28:
        return None

    df['tr'] = df['High'].combine(df['Close'].shift(), max) - df['Low'].combine(df['Close'].shift(), min)
    df['atr'] = df['tr'].rolling(window=14).mean()

    df['up_move'] = df['High'].diff()
    df['down_move'] = df['Low'].diff()
    df['plus_dm'] = np.where((df['up_move'] > df['down_move']) & (df['up_move'] > 0), df['up_move'], 0)
    df['minus_dm'] = np.where((df['down_move'] > df['up_move']) & (df['down_move'] > 0), df['down_move'], 0)
    
    df['plus_di'] = 100 * (df['plus_dm'].rolling(14).mean() / df['atr'])
    df['minus_di'] = 100 * (df['minus_dm'].rolling(14).mean() / df['atr'])
    df['dx'] = 100 * abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])
    adx = df['dx'].rolling(14).mean()
    
    return round(adx.dropna().iloc[-1], 2) if not adx.dropna().empty else None

# Store data in MySQL database
def store_data_in_db(data):
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="123", database="hitman")
        cursor = conn.cursor()

        sql = """INSERT INTO stocks (symbol, latest_price, sma, macd, signal_macd, adx, pe_ratio, pb_ratio, ps_ratio, peg_ratio, ev_ebitda, gross_margin, net_margin, op_margin, roa,roe,eps_growth,yoy_growth, operating_cash_flow,current_ratio,quick_ratio,de_ratio, icr,asset_turnover, inventory_turnover,dso,insider_ownership,inst_ownership) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                 ON DUPLICATE KEY UPDATE
        latest_price = VALUES(latest_price),
        sma = VALUES(sma),
        macd = VALUES(macd),
        signal_macd = VALUES(signal_macd),
        adx = VALUES(adx),
        pe_ratio = VALUES(pe_ratio),
        pb_ratio = VALUES(pb_ratio),
        ps_ratio = VALUES(ps_ratio),
        peg_ratio = VALUES(peg_ratio),
        ev_ebitda = VALUES(ev_ebitda),
        gross_margin = VALUES(gross_margin),
        net_margin = VALUES(net_margin),
        op_margin = VALUES(op_margin),
        roa = VALUES(roa),
        roe = VALUES(roe),
        eps_growth = VALUES(eps_growth),
        yoy_growth = VALUES(yoy_growth),
        operating_cash_flow = VALUES(operating_cash_flow),
        current_ratio = VALUES(current_ratio),
        quick_ratio = VALUES(quick_ratio),
        de_ratio = VALUES(de_ratio),
        icr = VALUES(icr),
        asset_turnover = VALUES(asset_turnover),
        inventory_turnover = VALUES(inventory_turnover),
        dso = VALUES(dso),
        insider_ownership = VALUES(insider_ownership),
        inst_ownership = VALUES(inst_ownership)"""

        # Convert NumPy values to native Python types
        converted_data = []
        for row in data:
            converted_row = tuple(float(x) if isinstance(x, (np.float64, np.float32)) else int(x) if isinstance(x, (np.int64, np.int32)) else x for x in row)
            converted_data.append(converted_row)

        cursor.executemany(sql, converted_data)
        conn.commit()
        cursor.close()
        conn.close()
        print("Data stored successfully!")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")

if __name__ == "__main__":
    stock_symbols = ["AAPL", "MSFT", "GOOGL", "CAVA", "AMZN","TSLA","TMDX"]
    results = []

   
    for symbol in stock_symbols:
        df, stock_prices, current_price, eps, bvps, revenue_ttm, market_cap, growth_rate, ebitda, enterprise_value, cogs, net_income, operating_income, total_assets, total_equity, roe,eps_growth,yoy_growth,operating_cash_flow,current_ratio,quick_ratio,de_ratio ,icr,asset_turnover,inventory_turnover,dso,insider_ownership,inst_ownership= get_stock_data(symbol)
        if df is not None and stock_prices and current_price:
            results.append((symbol, current_price, calculate_sma(stock_prices), *calculate_macd(df), calculate_adx(df), calculate_pe_ratio(current_price, eps), calculate_pb_ratio(current_price, bvps), calculate_ps_ratio(market_cap, revenue_ttm), calculate_peg_ratio(calculate_pe_ratio(current_price, eps), growth_rate), calculate_ev_ebitda(enterprise_value, ebitda), calculate_gross_margin(revenue_ttm, cogs), calculate_net_profit_margin(revenue_ttm, net_income), get_operating_margin(revenue_ttm, operating_income), calculate_roa(net_income, total_assets), roe,eps_growth,yoy_growth,operating_cash_flow,current_ratio,quick_ratio,de_ratio,icr,asset_turnover,inventory_turnover,dso,insider_ownership,inst_ownership))
    
    store_data_in_db(results)
    print(tabulate(results, headers=["Symbol", "Price", "SMA", "MACD", "Signal", "ADX", "P/E", "P/B", "P/S", "PEG", "EV/EBITDA", "Gross M", "Net M", "Op M", "ROA", "ROE","EPS Growth","yoy_growth","operating_cash_flow","current_ratio","quick_ratio","de_ratio","icr","asset_turnover","inventory_turnover","dso","insider_ownership_%","inst_ownership_%"], tablefmt="grid"))


