import requests
import cloudscraper

class FeedReader:
    def __init__(self):
        """Initialize the FeedReader class."""
        pass

    def fetch_feed(self, url: str, headers: dict) -> str | None:
        try:
            # 1ª tentativa — requests “normal”
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.ok:                         # status‑code 2xx
                return resp.text

            # Fallback — cloudscraper (dribla 403/Cloudflare)
            print(f"requests devolveu {resp.status_code}; tentando cloudscraper…")
            scraper = cloudscraper.create_scraper()
            xml = scraper.get(url, headers=headers, timeout=10).text
            return xml                          # <- agora devolve o conteúdo!

        except Exception as e:
            print(f"Erro ao buscar feed: {e}")
            return None

    def read_url(self, url):
        """Read content from a given URL with headers to mimic a browser request."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': url
        }
        try:
            text = self.fetch_feed(url, headers=headers)
            return text
        except Exception as e:
            print(f"Error fetching feed: {e}")
            return None 


