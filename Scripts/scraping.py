import requests
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
import json

# --- Google Search ---
def google_search(query, api_key, cx, num=3):
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={cx}&num={num}"
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTP errors
        return [item['link'] for item in response.json().get('items', [])]
    except Exception as e:
        print(f"Google Search failed: {e}")
        return []

# --- Spider ---
class ContentSpider(Spider):
    name = "content_spider"
    
    def __init__(self, urls=None, query=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls or []
        self.query = query.lower()

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join([el.get_text() for el in soup.find_all(['p', 'div', 'article'])])
        
        # Debug: Print URL and snippet
        print(f"\nScraping: {response.url}")
        print("Text snippet:", text[:100].replace("\n", " ") + "...")
        
        # Check for ANY query keyword in text
        if any(word in text.lower() for word in self.query.split()):
            yield {
                "url": response.url,
                "content": text[:5000] + "..."  # Limit output size
            }
        else:
            print(f"No match for query '{self.query}' in {response.url}")

# --- Main ---
if __name__ == "__main__":
    query = input("Enter search query: ").strip()
    API_KEY = "YOUR_API_KEY"  # Replace with your key
    CX = "YOUR_CX"           # Replace with your CX
    
    print("\nFetching Google results...")
    urls = google_search(query, API_KEY, CX)
    print("URLs found:", urls)
    
    if not urls:
        print("No URLs found. Using fallback URLs.")
        urls = ["https://en.wikipedia.org", "https://www.nytimes.com"]  # Fallback
    
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0',
        'FEED_FORMAT': 'json',
        'FEED_URI': f'{query.replace(" ", "_")}_results.json',
        'LOG_LEVEL': 'DEBUG'  # Enable detailed logs
    })
    process.crawl(ContentSpider, urls=urls, query=query)
    process.start()
    print(f"\nResults saved to '{query.replace(' ', '_')}_results.json'.")