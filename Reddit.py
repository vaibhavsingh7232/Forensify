import praw
import os
from datetime import datetime
import csv
# Reddit API credentials
reddit = praw.Reddit(
    client_id="XGSS5HXrKX-UsWRs9rY1LA",
    client_secret="rr8o99pMrm8f5QLz4wl0Nu_-VdhfQg",
    user_agent="forensify by Intruder997",
)

def ensure_data_directory():
    """Ensure the Data directory exists"""
    if not os.path.exists('Data'):
        os.makedirs('Data')

def fetch_reddit_data(subreddit_name, post_limit=500, comment_limit=30):
    """Fetch top posts and their comments from a subreddit and save to a text file in Data folder."""
    try:
        ensure_data_directory()
        subreddit = reddit.subreddit(subreddit_name)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Data/reddit_{subreddit_name}_{timestamp}.csv"
        
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"Reddit Data Collection - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Subreddit: r/{subreddit_name}\n")
            file.write(f"Posts: {post_limit}, Comments per post: {comment_limit}\n")
            file.write("="*50 + "\n\n")
            
            for post in subreddit.hot(limit=post_limit):
                file.write(f"Title: {post.title}\n")
                file.write(f"Author: {post.author.name if post.author else '[deleted]'}\n")
                file.write(f"Upvotes: {post.score}\n")
                file.write(f"Comments: {post.num_comments}\n")
                file.write(f"URL: {post.url}\n")
                file.write(f"Created: {datetime.fromtimestamp(post.created_utc)}\n\n")

                try:
                    post.comments.replace_more(limit=0)
                    comments = post.comments[:comment_limit]
                    
                    if comments:
                        file.write("Top Comments:\n")
                        for idx, comment in enumerate(comments, 1):
                            file.write(f"  {idx}. Author: {comment.author.name if comment.author else '[deleted]'}\n")
                            file.write(f"     Upvotes: {comment.score}\n")
                            file.write(f"     {comment.body[:200]}")
                            if len(comment.body) > 200:
                                file.write("... [truncated]")
                            file.write("\n\n")
                    else:
                        file.write("  No comments available.\n")
                except Exception as e:
                    file.write(f"  Error loading comments: {str(e)}\n")
                
                file.write("-"*70 + "\n\n")
        
        print(f"Data successfully saved to {filename}")
        return filename
    
    except Exception as e:
        print(f"Error fetching Reddit data: {str(e)}")
        raise

if __name__ == "__main__":
    subreddit_name = input("Enter subreddit name: ").strip()
    if subreddit_name:
        fetch_reddit_data(subreddit_name)
    else:
        print("Subreddit name cannot be empty")