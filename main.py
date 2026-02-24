import feedparser
import requests
from datetime import datetime

# --- CONFIGURATION ---
# This is the RSS link for your '2026-to-read' shelf
GOODREADS_RSS_URL = "https://www.goodreads.com/review/list_rss/176945722?shelf=2026-to-read"

# This is your unique notification name
NTFY_TOPIC_NAME = "danielle-book-alerts" 
# ---------------------

def get_release_date(title, author):
    # This asks Google for the book's publication date
    query = f"intitle:{title}+inauthor:{author}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    try:
        response = requests.get(url).json()
        if "items" in response:
            # We look for the YYYY-MM-DD date format
            return response["items"][0]["volumeInfo"].get("publishedDate", "")
    except:
        return None
    return None

def main():
    feed = feedparser.parse(GOODREADS_RSS_URL)
    # This gets today's date in YYYY-MM-DD format (e.g., 2026-02-24)
    today = datetime.now().strftime("%Y-%m-%d")
    
    print(f"Checking shelf for releases on: {today}")

    for entry in feed.entries:
        # entry.title usually looks like "Title (Series, #1)"
        book_title = entry.title
        # Extract author if available
        book_author = getattr(entry, 'author_name', '')
        
        release_date = get_release_date(book_title, book_author)
        
        print(f"Checking: {book_title} | Found Date: {release_date}")
        
        # If the book's release date is EXACTLY today's date
        if release_date == today:
            message = f"📖 '{book_title}' is out today! Check Libby or the library catalog! 🏛️"
            requests.post(f"https://ntfy.sh/{NTFY_TOPIC_NAME}", 
                          data=message.encode('utf-8'),
                          headers={"Title": "Book Release Day!"})
            print(f"!!! Success: Notification sent for {book_title}")

if __name__ == "__main__":
    main()
