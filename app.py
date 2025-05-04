# Add this to your existing app.py
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import Reddit
import twitter  # Add this import
import os
from datetime import datetime

app = Flask(__name__)

# Ensure Data directory exists
if not os.path.exists('Data'):
    os.makedirs('Data')

@app.route('/')
def index():
    return render_template('minor.html')

@app.route('/analyzer')
def analyzer():
    return render_template('upload.html')

@app.route('/reddit', methods=['GET', 'POST'])
def reddit():
    if request.method == 'POST':
        subreddit_name = request.form.get('subreddit_name', 'python').strip()
        if not subreddit_name:
            return render_template('reddit.html', error="Please enter a subreddit name")
        
        try:
            filename = Reddit.fetch_reddit_data(subreddit_name)
            return redirect(url_for('reddit_result', subreddit=subreddit_name, filename=os.path.basename(filename)))
        except Exception as e:
            return render_template('reddit.html', error=f"Error fetching data: {str(e)}")
    
    return render_template('reddit.html')

# Add these new routes for Twitter
@app.route('/twitter', methods=['GET', 'POST'])
def twitter_search():
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        count = request.form.get('count', '10').strip()
        
        if not query:
            return render_template('twitter.html', error="Please enter a search query")
        
        try:
            count = min(int(count), 100)
            client = twitter.authenticate_twitter()
            if client:
                tweets = twitter.search_tweets(client, query, count)
                if tweets:
                    filename = twitter.save_tweets_to_text(tweets, query)
                    return redirect(url_for('twitter_result', query=query, filename=os.path.basename(filename)))
                else:
                    return render_template('twitter.html', error="No tweets found or there was an error")
            else:
                return render_template('twitter.html', error="Failed to authenticate with Twitter")
        except Exception as e:
            return render_template('twitter.html', error=f"Error fetching tweets: {str(e)}")
    
    return render_template('twitter.html')

@app.route('/twitter_result/<query>/<filename>')
def twitter_result(query, filename):
    try:
        with open(f"Data/{filename}", 'r', encoding='utf-8') as file:
            content = file.read()
        return render_template('twitter_result.html', 
                             content=content, 
                             query=query,
                             filename=filename)
    except FileNotFoundError:
        return render_template('twitter_result.html', 
                             content="No data found", 
                             query=query,
                             filename=None)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('Data', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)