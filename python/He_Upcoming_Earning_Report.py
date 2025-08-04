import requests
import time
import pandas as pd
import yfinance as yf
from tabulate import tabulate
from email.message import EmailMessage
import smtplib

from he_database_connect import get_connection
from he_error_logs import log_error_to_db  


API_KEY = 'd0a8q79r01qnh1rh09v0d0a8q79r01qnh1rh09vg'
start_date = '2025-06-01'
end_date = '2025-06-30'
calendar_url = f'https://finnhub.io/api/v1/calendar/earnings?from={start_date}&to={end_date}&token={API_KEY}'
company_cache = {}

EXCLUDE_KEYWORDS = ["fund", "trust", "etf", "reit", "insurance", "life", "portfolio"]


sender_email = "dhineshapihitman@gmail.com"
receiver_email = ",".join([
    "ila@shravtek.com",
    "avinashgabadatasharing@gmail.com",
    "bullseye.3578@gmail.com",
    "sujit@shravtek.com",
    "sukumar@shravtek.com",
    "shreeram@shravtek.com",
    "dharanidharan@shravtek.com"
])
subject = "Earnings Calendar Report"
app_password = "yiof ntnc xowc gpbp"

def convert_hour(hour_code):
    if not hour_code:
        return 'NULL'
    return {
        'bmo': 'Before Market Open',
        'amc': 'After Market Close',
        'dmt': 'During Market Trading'
    }.get(hour_code.lower(), 'NULL')

def get_company_name(symbol):
    if symbol in company_cache:
        return company_cache[symbol]
    url = f'https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}'
    while True:
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                name = res.json().get('name', 'N/A')
                company_cache[symbol] = name
                return name
            elif res.status_code == 429:
                time.sleep(60)
                continue
            else:
                return 'N/A'
        except Exception as e:
            log_error_to_db("he_upcoming_earning_report.py", str(e), created_by="get_company_name")
            return 'N/A'

def get_actual_eps(symbol, date):
    url = f'https://finnhub.io/api/v1/stock/earnings?symbol={symbol}&token={API_KEY}'
    while True:
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                for r in res.json():
                    if r.get("period", "").startswith(date):
                        return r.get("actual", None)
                return None
            elif res.status_code == 429:
                time.sleep(60)
                continue
            else:
                return None
        except Exception as e:
            log_error_to_db("he_upcoming_earning_report.py", str(e), created_by="get_actual_eps")
            return None

def get_last_year_eps(symbol, date):
    year = str(int(date[:4]) - 1)
    url = f'https://finnhub.io/api/v1/stock/earnings?symbol={symbol}&token={API_KEY}'
    while True:
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                for r in res.json():
                    if r.get("period", "").startswith(year):
                        return r.get("actual", None)
                return None
            elif res.status_code == 429:
                time.sleep(60)
                continue
            else:
                return None
        except Exception as e:
            log_error_to_db("he_upcoming_earning_report.py", str(e), created_by="get_last_year_eps")
            return None

def format_market_cap(value):
    try:
        return f"${value / 1e9:.2f}B" if value else 'NULL'
    except Exception as e:
        log_error_to_db("he_upcoming_earning_report.py", str(e), created_by="format_market_cap")
        return 'NULL'

def main():
    try:
        response = requests.get(calendar_url)
        response.raise_for_status()
        earnings = response.json().get('earningsCalendar', [])
        if not earnings:
            print(" No earnings data found.")
            return
    except Exception as e:
        print(" Error fetching earnings calendar:", e)
        log_error_to_db("he_upcoming_earning_report.py", str(e), created_by="main - fetch calendar")
        return

    results = []

    for i, e in enumerate(earnings, 1):
        symbol = e.get('symbol')
        if not symbol:
            continue

        try:
            ticker = yf.Ticker(symbol)
            market_cap = ticker.info.get("marketCap", 0)
            if not market_cap or market_cap < 1_000_000_000:
                print(f" Skipped {symbol}: Market cap < $1B")
                continue
        except Exception as ex:
            log_error_to_db("earnings_report.py", str(ex), created_by="main - get market cap")
            continue

        try:
            company_name = get_company_name(symbol)
            if any(k in company_name.lower() for k in EXCLUDE_KEYWORDS):
                print(f" Skipped {symbol}: {company_name} matched exclude keywords")
                continue

            earnings_date = e.get('date')
            eps_estimate = e.get('epsEstimate')
            actual_eps = get_actual_eps(symbol, earnings_date) if earnings_date else None
            last_year_eps = get_last_year_eps(symbol, earnings_date) if earnings_date else None
            time_str = convert_hour(e.get('hour'))

            try:
                hist = ticker.history(period='1mo')
                price = hist['Close'].iloc[-1] if not hist.empty else None
                vol = hist['Close'].pct_change().std() * (252**0.5) if not hist.empty else None
            except:
                price, vol = None, None

            results.append({
                "Company Name": company_name or "NULL",
                "Ticker Symbol": symbol,
                "Earnings Date": earnings_date,
                "Time": time_str,
                "EPS Estimate": eps_estimate or "NULL",
                "Actual EPS": actual_eps or "NULL",
                "Last Year EPS": last_year_eps or "NULL",
                "Market Cap": format_market_cap(market_cap),
                "Current Price": f"${price:.2f}" if price else "NULL",
                "Volatility": f"{vol:.2%}" if isinstance(vol, float) else "NULL"
            })

            print(f" {i}/{len(earnings)} - {symbol}")
            time.sleep(0.2)
        except Exception as e:
            log_error_to_db("he_upcoming_earning_report.py", str(e), created_by="main - process symbol")
            continue

    if not results:
        print(" No records to insert or email.")
        return

    df = pd.DataFrame(results)
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.executemany('''
            INSERT INTO upcoming_earning_report (
                company_name, ticker_symbol, earnings_date, time, eps_estimate,
                actual_eps, market_cap, current_price, volatility
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', [
            (r["Company Name"], r["Ticker Symbol"], r["Earnings Date"], r["Time"],
             r["EPS Estimate"], r["Actual EPS"], r["Market Cap"],
             r["Current Price"], r["Volatility"])
            for r in results
        ])
        conn.commit()
        print(f" Inserted {cursor.rowcount} rows to MySQL.")
    except Exception as e:
        print(" MySQL insert failed:", e)
        log_error_to_db("he_upcoming_earning_report.py", str(e), created_by="main - DB insert")
    finally:
        if 'conn' in locals(): conn.close()


    try:
        html = """
        <html><head><style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background: #f4f4f4; }
        </style></head><body><h2>Earnings Calendar Report</h2><table>
        <tr><th>Company</th><th>Symbol</th><th>Date</th><th>Time</th>
        <th>Est. EPS</th><th>Actual</th><th>Last Year</th>
        <th>Cap</th><th>Price</th><th>Volatility</th></tr>"""
        for r in results:
            html += f"<tr><td>{r['Company Name']}</td><td>{r['Ticker Symbol']}</td><td>{r['Earnings Date']}</td><td>{r['Time']}</td><td>{r['EPS Estimate']}</td><td>{r['Actual EPS']}</td><td>{r['Last Year EPS']}</td><td>{r['Market Cap']}</td><td>{r['Current Price']}</td><td>{r['Volatility']}</td></tr>"
        html += "</table></body></html>"

        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.set_content("Please open this email in an HTML-compatible viewer.")
        msg.add_alternative(html, subtype='html')

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        print(" Email sent.")
    except Exception as e:
        print(" Email send failed:", e)
        log_error_to_db("he_upcoming_earning_report.py", str(e), created_by="main - send_email")

if __name__ == "__main__":
    main()
