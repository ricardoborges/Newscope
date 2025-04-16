class PromptBuilder:
    def orcrim_news(self, feed_content):
        """Build a prompt for organized crime news analysis."""
        prompt = f"""
        Analise este feed de notícias e identifique apenas notícias relacionadas a:
        1. Facções criminosas (PCC, Comando Vermelho, etc.)
        2. Tráfico de drogas
        3. Guerra do tráfico
        
        Importante:
        - Não inclua outras notícias policiais não vinculados a facções criminosas ou tráfico de drogas
        - Use APENAS as informações contidas neste feed
        - NÃO navegue em links externos
        - Inclua APENAS notícias relevantes sobre os temas acima
        - Se não encontrar notícias relevantes, retorne uma lista vazia
        
        Para cada notícia relevante, forneça um JSON com a seguinte estrutura:
        {{
            "title": "Título completo da notícia",
            "url": "URL da notícia",
            "image": "URL da imagem principal (se disponível)",
            "summary": "Resumo conciso da notícia (se disponível)",
            "faccao": "Nome da facção mencionada (se identificável)"
        }}
        
        Retorne os resultados como uma lista de objetos JSON.
        
        Feed de notícias:
        {feed_content}
        """
        return prompt
