from feed.news_collector import NewsCollector
from repository.firebase_news_repository import FirebaseNewsRepository
from services.news_processor import NewsProcessor

def main():
    """Main entry point for the application."""
    # First phase: Collect and store news
    print("Starting news collection phase...")
    fbRepo = FirebaseNewsRepository()
    #sqliteRepo = SQLiteNewsRepository("news.db")
    collector = NewsCollector(fbRepo)
    collector.run()

    # Second phase: Process news and extract structured data
    #print("\nStarting news processing phase...")
    #processor = NewsProcessor()
    #processor.run()

if __name__ == "__main__":
    main()
