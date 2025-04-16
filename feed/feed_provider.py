class FeedProvider:
    def __init__(self):
        """Initialize the FeedProvider with a default set of feeds."""
        self.feeds = {
            #'alojuca': 'https://alojuca.com.br/policia/feed/',
            #'bahia-noticias-municipios':'https://www.bahianoticias.com.br/municipios/rss.xml',
            'bahia-noticias-principal':'https://www.bahianoticias.com.br/principal/rss.xml'
            #'bnews': 'https://www.bnews.com.br/feed',
            #'correio24horas':'https://www.correio24horas.com.br/rss',
            #'jornalmassa':'https://jornalmassa.com.br/rss',
            #'ibahia':'https://www.ibahia.com/rss'

            # Add more feeds here as needed
        }

    def get_feed_url(self, feed_name):
        """Get a specific feed URL by name."""
        return self.feeds.get(feed_name)

    def get_all_feeds(self):
        """Get all available feed URLs."""
        return self.feeds

    def add_feed(self, name, url):
        """Add a new feed to the provider."""
        self.feeds[name] = url

    def remove_feed(self, name):
        """Remove a feed from the provider."""
        if name in self.feeds:
            del self.feeds[name]
