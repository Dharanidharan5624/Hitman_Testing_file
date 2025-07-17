import requests
from textblob import TextBlob
from datetime import date, timedelta
import time

API_KEY = '6a2e7b8388724ec7b7420c74d3bb2844'
symbol = 'AAPL' 

def get_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

# Define the interval in minutes (10 minutes)
interval_minutes = 10
interval_seconds = interval_minutes * 60  # Convert minutes to seconds

while True:  # Infinite loop to fetch data every 10 minutes
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Format the URL
    url = f'https://newsapi.org/v2/everything?q={symbol}&from={yesterday.isoformat()}&to={today.isoformat()}&apiKey={API_KEY}&language=en&sortBy=publishedAt'
  
    response = requests.get(url)
    data = response.json()

    print(f"\nTop news articles for: {symbol} from {yesterday} to {today}\n")

    if 'articles' in data and data['articles']:
        for article in data['articles'][:5]:  # Top 5 articles
            title = article.get('title', '')
            description = article.get('description', '')
            published_at = article.get('publishedAt', '')
            url = article.get('url', '')
            
            sentiment = get_sentiment(f"{title} {description}")
            
            print(f"Symbol: {symbol}")
            print(f"Title: {title}")
            print(f"Summary: {description}")
            print(f"Published At: {published_at}")
            print(f"URL: {url}")
            print(f"Sentiment: {sentiment}")
            print("-" * 100)
    else:
        print("No articles found for yesterday/today or an error occurred.")
    
    # Wait for the specified interval (in seconds)
    time.sleep(interval_seconds)  # Wait for 10 minutes before fetching again
