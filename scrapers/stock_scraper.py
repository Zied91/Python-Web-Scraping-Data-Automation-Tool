# scrapers/stock_scraper.py
from bs4 import BeautifulSoup
from .scraper_base import ScraperBase

class StockScraper(ScraperBase):
    def run_for_symbol(self, symbol):
        url = f"https://finance.yahoo.com/quote/{symbol}"
        html = self.fetch(url)
        return self.parse(symbol, html)

    def parse(self, symbol, html):
        soup = BeautifulSoup(html, "lxml")

        price = soup.select_one("fin-streamer[data-field='regularMarketPrice']").text
        change = soup.select_one("fin-streamer[data-field='regularMarketChangePercent']").text
        volume = soup.select_one("fin-streamer[data-field='regularMarketVolume']").text

        return {
            "symbol": symbol,
            "price": price,
            "change": change,
            "volume": volume
        }
