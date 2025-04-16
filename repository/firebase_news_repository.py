import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from typing import Dict, List
from datetime import datetime, time as dt_time
from google.cloud.firestore_v1.base_query import FieldFilter

from repository.news_repository import NewsRepository

class FirebaseNewsRepository(NewsRepository):
    
    def __init__(self, cred_path: str = 'firebase-credentials.json'):
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.news_collection = self.db.collection('news')
    
    def news_exists(self, url: str) -> bool:
        """Check if a news item already exists in the database."""
        docs = self.news_collection.where('url', '==', url).get()
        return len(docs) > 0
    
    def save_news(self, news_item: Dict) -> bool:
        """Save a news item to the database if it doesn't exist."""
        if not self.news_exists(news_item['url']):
            news_item['collected_at'] = datetime.now()  # Use datetime object directly
            news_item['processed'] = False
            news_item['sent'] = False
            # Store the document reference
            doc_ref = self.news_collection.add(news_item)
            # Add the document ID to the news item
            news_item['id'] = doc_ref[1].id
            return True
        return False
    
    def get_unprocessed_news(self) -> List[Dict]:
        """Get all unprocessed news items."""
        docs = self.news_collection.where('processed', '==', False).get()
        return [self._add_id_to_doc(doc) for doc in docs]
    
    def update_news(self, doc_id: str, updates: Dict) -> None:
        """Update a news item with new data."""
        try:
            doc_ref = self.news_collection.document(doc_id)
            doc_ref.update(updates)
        except Exception as e:
            print(f"Error updating document {doc_id}: {str(e)}")
    
    def get_all_news(self) -> List[Dict]:
        """Get all news items from the database."""
        docs = self.news_collection.get()
        return [self._add_id_to_doc(doc) for doc in docs]
    
    def get_today_news(self) -> List[Dict]:
        """Get all news items collected today using a Firestore timestamp query."""
        today = datetime.now().date()
        start = datetime.combine(today, dt_time.min)
        end = datetime.combine(today, dt_time.max)
        
        # Use where() method for Firebase query
        docs = self.news_collection.where("collected_at", ">=", start).where("collected_at", "<=", end).get()
        return [self._add_id_to_doc(doc) for doc in docs]
    
    def _add_id_to_doc(self, doc) -> Dict:
        """Helper method to add document ID to the data dictionary."""
        data = doc.to_dict()
        data['id'] = doc.id
        return data
