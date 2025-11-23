# main.py
import yaml
from scrapers.crypto_scraper import CryptoScraper
from scrapers.stock_scraper import StockScraper
from utils.exporter import save_data
from utils.scheduler import run_every
from utils.chart_generator import (
    create_crypto_price_chart,
    create_crypto_change_chart,
    create_stock_price_chart
)

def run_scrapers():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    # Crypto
    crypto = CryptoScraper()
    crypto_data = crypto.run(config["crypto_sources"][0]["url"])
    save_data(crypto_data, "data/crypto_prices.csv")

    # Generate crypto charts
    create_crypto_price_chart("data/crypto_prices.csv")
    create_crypto_change_chart("data/crypto_prices.csv")

    # Stocks
    stock = StockScraper()
    stock_results = []
    for symbol in config["stocks_sources"][0]["symbols"]:
        stock_results.append(stock.run_for_symbol(symbol))
    save_data(stock_results, "data/stock_prices.csv")

    # Generate stock charts
    create_stock_price_chart("data/stock_prices.csv")


if __name__ == "__main__":
    run_scrapers()
