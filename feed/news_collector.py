from feed.feed_reader import FeedReader
from feed.feed_provider import FeedProvider
from llm.gemini_client import GeminiClient
from repository.news_repository import NewsRepository

class NewsCollector:
    def __init__(self, news_repository: NewsRepository):
        """Initialize the NewsCollector with all required components.
        
        Args:
            news_repository: Implementation of the NewsRepository interface
        """
        self.feed_provider = FeedProvider()
        self.feed_reader = FeedReader()
        self.llm_client = GeminiClient()
        self.repository = news_repository

    def process_feed(self, feed_name, feed_url):
        """Process a single feed and store the results."""
        print(f"\nProcessing feed: {feed_name}")
        
        # Check if the URL already exists in the database
        if self.repository.news_exists(feed_url):
            print(f"URL already exists in database: {feed_url}")
            return
            
        feed_content = self.feed_reader.read_url(feed_url)

        if not feed_content:
            print(f"Failed to fetch feed content from {feed_name}")
            return

        # Generate and process response
        response = self.llm_client.generate_response(feed_content, prompt_type="criminal_news")
        response = self.llm_client.clean_response(response)
        
        # Parse the response
        parsed_response = self.llm_client.parse_response(response)
        
        if parsed_response is not None:
            if isinstance(parsed_response, list):
                for item in parsed_response:
                    if self.repository.save_news(item):
                        print(f"Saved new news item: {item['title']}")
            else:
                print("Response is not in the expected list format.")

    def run(self):
        """Run the collection pipeline for all available feeds."""
        # Get all available feeds
        feeds = self.feed_provider.get_all_feeds()
        print("Available feeds:")
        for name, url in feeds.items():
            print(f"- {name}: {url}")

        # Process each feed
        for feed_name, feed_url in feeds.items():
            self.process_feed(feed_name, feed_url) 