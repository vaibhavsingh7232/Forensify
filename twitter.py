import tweepy
import time
import json
import os
from datetime import datetime

# Twitter API credentials
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAEgZ0AEAAAAAsC4XY%2B%2F1pxtsRSb0my1w4lAwl8c%3DW2wt5oB1a4h4h6h5QiJipVmnwGztqV6pE8bQRKhbjdxqfFbMWc"
CONSUMER_KEY = "1bFn6maxoUcU96gLHMm8LS1lCjCAsyZh3XwDH8OZkeVTuOk9lw"
CONSUMER_SECRET = "1bFn6maxoUcU96gLHMm8LS1lCjCAsyZh3XwDH8OZkeVTuOk9lw"
ACCESS_TOKEN = "1902064516613222400-lKZrxenf0BwYl7VvH1wKuErU6smZrU"
ACCESS_TOKEN_SECRET = "02SorZQjKnPMqKQzZTgfg6IHbPhjF6gkXaAObB5qPxpm4"

def ensure_data_folder():
    """Ensure the Data folder exists"""
    if not os.path.exists('Data'):
        os.makedirs('Data')
    return 'Data'

def save_tweets_to_json(tweets, query):
    """Save tweets to a JSON file in the Data folder"""
    data_folder = ensure_data_folder()
    
    safe_query = ''.join(c for c in query if c.isalnum() or c in (' ', '_')).rstrip()
    if not safe_query:
        safe_query = "tweets"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{data_folder}/{safe_query[:50]}_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'metadata': {
                    'query': query,
                    'timestamp': timestamp,
                    'tweet_count': len(tweets)
                },
                'tweets': tweets
            }, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {len(tweets)} tweets to JSON file: {filename}")
        return filename
    except Exception as e:
        print(f"Error saving tweets to JSON file: {e}")
        return None

def save_tweets_to_text(tweets, query):
    """Save tweets to a readable text file in the Data folder"""
    data_folder = ensure_data_folder()
    
    safe_query = ''.join(c for c in query if c.isalnum() or c in (' ', '_')).rstrip()
    if not safe_query:
        safe_query = "tweets"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{data_folder}/{safe_query[:50]}_{timestamp}.txt"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Twitter Search Results\n")
            f.write(f"=====================\n\n")
            f.write(f"Search Query: {query}\n")
            f.write(f"Date Collected: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Tweets: {len(tweets)}\n\n")
            
            for i, tweet in enumerate(tweets, 1):
                f.write(f"\nTweet #{i}\n")
                f.write(f"----------\n")
                f.write(f"Author: @{tweet['author']['username']} ({tweet['author']['name']})")
                f.write(" ✅" if tweet['author']['verified'] else "")
                f.write("\n")
                f.write(f"Date: {tweet['created_at']}\n")
                f.write(f"URL: {tweet['url']}\n")
                f.write("\n")
                f.write(f"{tweet['text']}\n")
                f.write("\n")
                f.write(f"Likes: {tweet['metrics']['likes']} | ")
                f.write(f"Retweets: {tweet['metrics']['retweets']} | ")
                f.write(f"Replies: {tweet['metrics']['replies']}\n")
                f.write("-" * 50 + "\n")
                
        print(f"Saved {len(tweets)} tweets to text file: {filename}")
        return filename
    except Exception as e:
        print(f"Error saving tweets to text file: {e}")
        return None

def authenticate_twitter():
    """Authenticate with Twitter API with retry logic"""
    max_retries = 30
    retry_delay = 0.5
    
    for attempt in range(max_retries):
        try:
            client = tweepy.Client(
                bearer_token=BEARER_TOKEN,
                consumer_key=CONSUMER_KEY,
                consumer_secret=CONSUMER_SECRET,
                access_token=ACCESS_TOKEN,
                access_token_secret=ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            print("Twitter authentication successful!")
            return client
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Authentication failed (attempt {attempt + 1}), retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  
            else:
                print(f"Authentication failed after {max_retries} attempts: {e}")
                return None

def search_tweets(client, query, count=10):
    """Search recent tweets with enhanced error handling"""
    results = []
    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=min(count, 100),
            tweet_fields=['public_metrics', 'author_id', 'created_at'],
            user_fields=['username', 'verified', 'name'],
            expansions=['author_id']
        )
        
        if response.data:
            users = {u.id: u for u in response.includes['users']}
            for tweet in response.data:
                user = users[tweet.author_id]
                results.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'created_at': tweet.created_at.isoformat(),
                    'author': {
                        'username': user.username,
                        'name': user.name,
                        'verified': user.verified
                    },
                    'metrics': {
                        'likes': tweet.public_metrics['like_count'],
                        'retweets': tweet.public_metrics['retweet_count'],
                        'replies': tweet.public_metrics['reply_count'],
                        'impressions': tweet.public_metrics['impression_count']
                    },
                    'url': f"https://twitter.com/{user.username}/status/{tweet.id}"
                })
    
    except tweepy.TooManyRequests as e:
        print("Rate limit exceeded. Please wait before trying again.")
        print(f"Twitter API message: {e}")
    except tweepy.TweepyException as e:
        print(f"Twitter API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return results

def get_user_input():
    """Get search parameters from user"""
    print("\nTwitter Search Tool")
    print("------------------")
    query = input("Enter search query (or 'quit' to exit): ").strip()
    
    if query.lower() in ('quit', 'exit'):
        return None, None
    
    try:
        count = min(int(input("Number of tweets to fetch (1-100): ") or 10), 100)
        return query, count
    except ValueError:
        print("Please enter a valid number between 1-100")
        return get_user_input()

if __name__ == '__main__':
    client = authenticate_twitter()
    
    if client:
        while True:
            query, count = get_user_input()
            
            if query is None:  # User chose to quit
                break
                
            print(f"\nSearching for '{query}'...")
            tweets = search_tweets(client, query, count)
            
            if tweets:
                print(f"\nFound {len(tweets)} tweets:")
                for i, tweet in enumerate(tweets, 1):
                    print(f"\n{i}. @{tweet['author']['username']}{' ✅' if tweet['author']['verified'] else ''}")
                    print(tweet['text'])
                    print(f"👍 {tweet['metrics']['likes']} | 🔁 {tweet['metrics']['retweets']}")
                    print(tweet['url'])
                
                # Save the tweets to both formats
                json_file = save_tweets_to_json(tweets, query)
                text_file = save_tweets_to_text(tweets, query)
                
                if json_file and text_file:
                    print(f"\nSuccessfully saved data to:\n- {json_file}\n- {text_file}")
            else:
                print("No tweets found or there was an error.")