import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, Any, List

class UsersRepository:
    def __init__(self, cred_path: str = 'firebase-credentials.json'):
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.users_collection = self.db.collection('users')

    def user_exists(self, chat_id: int) -> bool:
        docs = self.users_collection.where('chat_id', '==', chat_id).get()
        return len(docs) > 0

    def save_user(self, chat_id: int, extra: Dict[str, Any] = None) -> None:
        if not self.user_exists(chat_id):
            data = {'chat_id': chat_id, 'feed': True}
            if extra:
                data.update(extra)
            self.users_collection.add(data)

    def sair_user(self, chat_id: int, extra: Dict[str, Any] = None) -> None:
        """Update the user with 'feed': False."""
        docs = self.users_collection.where('chat_id', '==', chat_id).get()
        for doc in docs:
            data = {'feed': False}
            if extra:
                data.update(extra)
            self.users_collection.document(doc.id).update(data)

    #def get_all_users(self) -> List[Dict]:
    #    """Get all registered users from Firebase."""
    #    docs = self.users_collection.get()
    #    return [self._add_id_to_doc(doc) for doc in docs]
    
    def get_all_chat_ids(self) -> List[int]:
        """Get all chat IDs of registered users where 'feed' is True."""
        docs = self.users_collection.where('feed', '==', True).get()
        return [doc.to_dict()['chat_id'] for doc in docs if 'chat_id' in doc.to_dict()]

