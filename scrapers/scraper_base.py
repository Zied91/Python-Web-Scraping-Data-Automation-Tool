# scrapers/scraper_base.py
import requests
from bs4 import BeautifulSoup

class ScraperBase:
    headers = {"User-Agent": "Mozilla/5.0"}

    def fetch(self, url):
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        return response.text

    def parse(self, html):
        raise NotImplementedError

    def run(self, url):
        html = self.fetch(url)
        return self.parse(html)
