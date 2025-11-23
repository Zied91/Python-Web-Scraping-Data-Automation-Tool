# scrapers/crypto_scraper.py
from bs4 import BeautifulSoup
from .scraper_base import ScraperBase

class CryptoScraper(ScraperBase):
    def parse(self, html):
        soup = BeautifulSoup(html, "lxml")
        table = soup.select("table.cmc-table tbody tr")

        results = []

        for row in table[:14]:  # top 20 crypto
            name = row.select_one("p.coin-item-name").text + f" {row.select_one("p.coin-item-symbol").text}"
            price = row.select("td")[4].text
            change_24h = row.select("td")[5].text
            market_cap = row.select("td")[7].text

            results.append({
                "name": name,
                "price": price,
                "change_24h": change_24h,
                "market_cap": market_cap
            })

        return results
