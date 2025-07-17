import requests
import time
import mysql.connector
import nltk
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# --- Setup NLTK ---
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# --- MySQL Database Setup ---
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123",         # Change this to your MySQL password
    database="hitman"       # Ensure this database exists
)
cursor = db_connection.cursor()
db_connection.commit()

# --- Sentiment Analysis Function ---
def analyze_sentiment(text):
    scores = sid.polarity_scores(text)
    return scores

# --- Save Article to MySQL ---
def store_article(symbols, title, summary, pub_time, link, sentiment_dict):
    try:
        cursor.execute("SELECT COUNT(*) FROM news_articles WHERE link = %s", (link,))
        article_count = cursor.fetchone()[0]
        if article_count == 0:
            sentiment_json = json.dumps(sentiment_dict)
            insert_query = """
                INSERT INTO news_articles (stock_symbol, title, summary, pub_time, link, sentiment)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            symbols_str = ','.join(symbols)
            cursor.execute(insert_query, (symbols_str, title, summary, pub_time, link, sentiment_json))
            db_connection.commit()
            print("✅ Stored:", title[:60])
        else:
            print(f"⚠️ Skipped (duplicate): {title[:60]} - Already exists.")
    except mysql.connector.Error as e:
        print("❌ DB Error:", e)

# --- Fetch Full Article Details ---
def fetch_article_details(article_id):
    url = f"https://seekingalpha.com/api/v3/news/{article_id}"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
     
        attributes = data.get("data", {}).get("attributes", {})
        page = data.get("meta", {}).get("page", {})
        title = attributes.get("title", "No title")
        summary = page.get("description", "No summary")
        pub_time = attributes.get("publishOn", "Unknown")
        link = f"https://seekingalpha.com/news/{article_id}"

        relationships = data.get("data", {}).get("relationships", {})
        symbols_data = relationships.get("primaryTickers", {}).get("data", [])
        symbols = [s.get("id", "UNKNOWN") for s in symbols_data]

        sentiment = analyze_sentiment(summary)
        print(f"💡 Symbols      : {symbols}")
        print(f"\n📰 Title        : {title}")
        print(f"📄 Summary      : {summary}")
        print(f"🕒 Published At : {pub_time}")
        print(f"🔗 Link         : {link}")
        print(f"📊 Sentiment    : {sentiment}")
        
        print("-" * 80)

        store_article(symbols, title, summary, pub_time, link, sentiment)
    else:
        print(f"❌ Failed to fetch article {article_id}. Status code: {res.status_code}")

# --- Fetch Latest News from Seeking Alpha ---
def fetch_latest_news(limit=5):
    url = "https://seekingalpha.com/api/v3/news?filter[category]=market-news&page[size]=5&page[number]=1"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9"
    }

    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        try:
            articles = res.json().get("data", [])[:limit]
            if not articles:
                print("⚠️ No articles found.")
                return

            for article in articles:
                article_id = article.get("id")
                if article_id:
                    fetch_article_details(article_id)
        except ValueError as e:
            print(f"❌ Error parsing response JSON: {e}")
    else:
        print(f"❌ Failed to fetch article list. Status code: {res.status_code}")

# --- Main Loop ---
if __name__ == "__main__":
    while True:
        try:
            print("\n🔄 Fetching latest news...\n")
            fetch_latest_news(limit=5)
            print("⏳ Sleeping for 10 minutes...\n")
            time.sleep(600)
        except Exception as e:
            print("❌ Runtime Error:", e)
            time.sleep(600)
