from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class NewsRepository(ABC):
    """Abstract base class for news persistence operations."""
    
    @abstractmethod
    def news_exists(self, url: str) -> bool:
        """Check if a news item with the given URL exists in the repository.
        
        Args:
            url: The URL of the news item to check
            
        Returns:
            bool: True if the news item exists, False otherwise
        """
        pass
    
    @abstractmethod
    def save_news(self, news_item: Dict) -> bool:
        """Save a news item to the repository.
        
        Args:
            news_item: Dictionary containing the news item data
            
        Returns:
            bool: True if the news item was saved successfully, False if it already exists
        """
        pass
    
    @abstractmethod
    def get_unprocessed_news(self) -> List[Dict]:
        """Get all unprocessed news items from the repository.
        
        Returns:
            List[Dict]: List of unprocessed news items
        """
        pass
    
    @abstractmethod
    def update_news(self, doc_id: str, updates: Dict) -> None:
        """Update a news item with new data.
        
        Args:
            doc_id: The document ID of the news item to update
            updates: Dictionary containing the fields to update
        """
        pass 