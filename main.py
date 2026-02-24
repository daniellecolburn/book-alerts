import feedparser
import requests
from datetime import datetime

# --- CONFIGURATION (CHANGE THESE TWO) ---
GOODREADS_RSS_URL = "https://www.goodreads.com/review/list_rss/176945722?shelf=2026-to-read"
NTFY_TOPIC_NAME = "danielle-library-alerts-2026" 
# ---------------------------------------

def get_release_date(title, author):
    # This asks Google for the book info
    query = f"intitle:{title}+inauthor:{author}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    try:
        response = requests.get(url).json()
        if "items" in response:
            return response["items"][0]["volumeInfo"].get("publishedDate", "")
    except:
        return None

def main():
    feed = feedparser.parse(GOODREADS_RSS_URL)
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"Checking shelf for: {today}")

    for entry in feed.entries:
        title = entry.title
        author = getattr(entry, 'author_name', 'Unknown Author')
        release_date = get_release_date(title, author)
        
        # If the release date matches today (YYYY-MM-DD)
        if release_date == today:
            message = f"📖 '{title}' by {author} is out today! Time to check Libby or the library! 🏛️"
            requests.post(f"https://ntfy.sh/{NTFY_TOPIC_NAME}", data=message.encode('utf-8'))
            print(f"Alert sent for {title}")

if __name__ == "__main__":
    main()
