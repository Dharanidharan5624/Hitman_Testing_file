import feedparser
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Setup NLTK for sentiment analysis
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# Sentiment analysis function
def analyze_sentiment(text):
    return sid.polarity_scores(text)

# Sentiment label function
def sentiment_label(compound_score):
    if compound_score >= 0.05:
        return "Positive"
    elif compound_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Define the ticker symbol and construct the URL
symbol = "HIMS"
url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"

# Parse ticker from URL
parsed_url = urlparse(url)
symbols = parse_qs(parsed_url.query).get('s', ['Unknown'])[0].split(',')

# Parse RSS feed
feed = feedparser.parse(url)

# Number of articles you want to fetch
article_limit = 7
count = 0

# Iterate through feed entries
for entry in feed.entries:
    if count >= article_limit:
        break
    try:
        summary = entry.summary
        sentiment = analyze_sentiment(summary)
        print(f"Tickers: {', '.join(symbols)}")
        print("Published:", entry.published)
        print("Title:", entry.title)
        print("Summary:", summary)
        print("Link:", entry.link)
        print("Sentiment:", sentiment)
        
        # Get sentiment label
        label = sentiment_label(sentiment['compound'])
        print(f"Final Sentiment Label: {label}")
        print("-" * 50)
        
        count += 1
    except AttributeError:
        continue
