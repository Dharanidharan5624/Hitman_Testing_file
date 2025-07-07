import requests
import time
import schedule
import mysql.connector
import datetime
import openai

# Your OpenAI API Key
openai.api_key = "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"

# List of stock symbols you want news for
stocks = ["AAPL", "TSLA", "SPY"]

# MySQL database connection
db_connection = mysql.connector.connect(
    host="localhost", user="root", password="123", database="hitman"
)
cursor = db_connection.cursor()
db_connection.commit()

def fetch_stock_news(stock_symbol):
    url = f"https://query2.finance.yahoo.com/v1/finance/search"
    params = {
        "q": stock_symbol,
        "quotesCount": 0,
        "newsCount": 5,  # Fetch 5 news per stock
    }
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("news", [])
        else:
            print(f"Failed to fetch news for {stock_symbol}: {response.status_code}")
    except Exception as e:
        print(f"Error fetching news for {stock_symbol}: {e}")
    return []

def generate_summary(title, link):
    prompt = f"""
You are a financial news summarizer.
Given the following news headline and link, create a short 2-3 line summary.

Title: {title}
Link: {link}

Summary:
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.5,
        )
        summary = response['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary not available."

def store_news_in_db(stock_symbol, title, summary, link, pub_time):
    try:
        cursor.execute("""
            INSERT INTO news_articles (stock_symbol, title, summary, link, pub_time)
            VALUES (%s, %s, %s, %s, %s)
        """, (stock_symbol, title, summary, link, pub_time))
        db_connection.commit()
    except Exception as e:
        print(f"Database error: {e}")

def job():
    print(f"\nFetching news at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    for stock in stocks:
        print(f"\nFetching news for {stock}")
        news_list = fetch_stock_news(stock)

        if news_list:
            for news in news_list:
                title = news.get('title', 'No Title')
                link = news.get('link', 'No Link')

                pub_time = news.get('providerPublishTime', None)
                if pub_time:
                    pub_time = datetime.datetime.utcfromtimestamp(pub_time).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    pub_time = None

                # Generate summary using GPT
                summary = generate_summary(title, link)

                # Save to DB
                store_news_in_db(stock, title, summary, link, pub_time)

                # Print
                print(f"\nTitle: {title}")
                print(f"Summary: {summary}")
                print(f"Published at: {pub_time}")
                print(f"Link: {link}\n")
        else:
            print(f"No news found for {stock}")

# Schedule to run every 10 minutes
schedule.every(10).minutes.do(job)

# Run immediately at start
job()

# Keep running
while True:
    schedule.run_pending()
    time.sleep(1)
