import firebase_admin
from firebase_admin import credentials, firestore

class FeedProvider:
    def __init__(self, cred_path: str = 'firebase-credentials.json'):
        """Initialize the FeedProvider with Firebase connection."""
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.feed_collection = self.db.collection('feed')

    def get_feed_url(self, feed_name: str) -> str | None:
        """Get a specific feed URL by name from Firebase."""
        doc = self.feed_collection.document(feed_name).get()
        if doc.exists():
            data = doc.to_dict()
            return list(data.values())[0]  # Extract the URL value
        return None

    def get_all_feeds(self) -> dict:
        """Get all available feed URLs from Firebase."""
        feeds = {}
        docs = self.feed_collection.get()
        for doc in docs:
            data = doc.to_dict()
            feeds.update(data)  # Merge the feed title and URL into the result
        return feeds

    def add_feed(self, name: str, url: str) -> None:
        """Add a new feed to the Firebase collection."""
        self.feed_collection.document(name).set({name: url})

    def remove_feed(self, name: str) -> None:
        """Remove a feed from the Firebase collection."""
        self.feed_collection.document(name).delete()
