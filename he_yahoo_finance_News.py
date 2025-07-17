import requests
from datetime import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# --- Setup NLTK ---
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# --- Sentiment Analysis Function ---
def analyze_sentiment(text):
    scores = sid.polarity_scores(text)
    return scores

# --- API Key and URL for Alpha Vantage ---
url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey=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"

# Get the news data from Alpha Vantage
response = requests.get(url)
data = response.json()

# Check if "feed" exists in the API response
if "feed" not in data:
    print("No news feed found. API response:", data)
    exit()

# Loop through the articles in the feed
for article in data.get("feed", [])[:6]:
    raw_time = article.get("time_published", "")
    dt = datetime.strptime(raw_time, "%Y%m%dT%H%M%S")
    formatted_date = dt.strftime("%Y/%m/%d")

    # Get the summary of the article
    summary = article.get("summary", "")

    # Get ticker sentiment data
    ticker_data = article.get("ticker_sentiment", [])
    if not ticker_data:
        continue

    # Loop through each ticker sentiment data
    for item in ticker_data:
        ticker = item.get('ticker', 'N/A')
        relevance_score = item.get('relevance_score', 'N/A')
        ticker_sentiment_score_str = item.get('ticker_sentiment_score', '0')

        # Handle ticker sentiment score
        try:
            score = float(ticker_sentiment_score_str)
            sentiment_label = (
                "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
            )
        except ValueError:
            sentiment_label = "Unknown"

        # Perform sentiment analysis using NLTK (VADER)
        sentiment = analyze_sentiment(summary)

        # Print the extracted data
        print(f"Ticker: {ticker}")
        print(f"Relevance Score: {relevance_score}")
        print(f"Ticker Sentiment Score: {ticker_sentiment_score_str}")
        print(f"Inferred Sentiment: {sentiment_label}")
        print("Source:", article.get("source", "N/A"))
        print("Title:", article.get("title", "N/A"))
        print("Summary:", summary)
        print("Published At:", formatted_date)
        print("URL:", article.get("url", "N/A"))
        print(f"📊 NLTK Sentiment (VADER): {sentiment}")
        print()
