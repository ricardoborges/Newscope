from llm.gemini_client import GeminiClient
from repository.firebase_news_repository import FirebaseNewsRepository
from datetime import datetime

class NewsProcessor:
    def __init__(self):
        """Initialize the NewsProcessorPipeline with all required components."""
        self.llm_client = GeminiClient()
        self.storage = FirebaseNewsRepository()

    def extract_structured_data(self, news_item):
        """Extract structured data from a news item."""
        prompt = f"""
        Extraia informações estruturadas desta notícia sobre facções criminosas.
        Procure por:
        - Nomes de pessoas mencionadas
        - Facções mencionadas
        - Localizações mencionadas

        Notícia:
        Título: {news_item['title']}
        URL: {news_item['url']}
        Resumo: {news_item.get('summary', 'N/A')}

        Responda em formato JSON com a seguinte estrutura, sem quebra de linha:
        {{
            "pessoas": [
                {{
                    "nome": "string",
                    "cargo": "string",
                    "relacao": "string"
                }}
            ],
            "faccoes": [
                {{
                    "nome": "string",
                    "sigla": "string"
                }}
            ],
            "localizacoes": [
                {{
                    "nome": "string",
                    "tipo": "string",
                    "contexto": "string"
                }}
            ]
        }}
        """

        response = self.llm_client.generate_response(prompt)
        response = self.llm_client.clean_response(response)
        return self.llm_client.parse_response(response)

    def process_news_item(self, news_item):
        """Process a single news item and extract structured data."""
        print(f"\nProcessing news item: {news_item['title']}")
        
        # Extract structured data
        structured_data = self.extract_structured_data(news_item)
        
        if structured_data:
            # Update the news item with structured data and mark as processed
            updates = {
                'structured_data': structured_data,
                'processed': True,
                'processed_at': datetime.now().isoformat()
            }
            self.storage.update_news(news_item['id'], updates)
        else:
            updates = {
                'processed': True,
                'processed_at': datetime.now().isoformat()
            }
            self.storage.update_news(news_item['id'], updates)
            print("Successfully processed and saved news item")
            return True
        
        return False

    def run(self):
        """Run the processing pipeline for all unprocessed news items."""
        unprocessed_news = self.storage.get_unprocessed_news()
        print(f"\nFound {len(unprocessed_news)} unprocessed news items")
        
        for news_item in unprocessed_news:
            self.process_news_item(news_item)
            
        # Print summary of processed items
        all_news = self.storage.get_all_news()
        processed_count = sum(1 for item in all_news if item.get('processed', False))
        print(f"\nProcessing complete. Total news items: {len(all_news)}, Processed: {processed_count}") 