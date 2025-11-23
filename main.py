# main.py
import yaml
from scrapers.crypto_scraper import CryptoScraper
from scrapers.stock_scraper import StockScraper
from utils.exporter import save_data
from utils.scheduler import run_every
from time import sleep
from utils.history import append_to_history
from utils.chart_generator import (
    create_crypto_price_chart,
    create_crypto_change_chart,
    create_stock_price_chart,
    create_crypto_price_trend,
    create_stock_price_trend
)

def run_scrapers():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    # Crypto
    crypto = CryptoScraper()
    crypto_data = crypto.run(config["crypto_sources"][0]["url"])
    save_data(crypto_data, "data/crypto_prices.csv")

    # Append to history
    append_to_history("data/crypto_prices.csv", "data/crypto_history.csv", "name")

    # Generate crypto charts
    create_crypto_price_chart("data/crypto_prices.csv")
    create_crypto_change_chart("data/crypto_prices.csv")
    create_crypto_price_trend("data/crypto_history.csv")


    # Stocks
    stock = StockScraper()
    stock_results = []
    for symbol in config["stocks_sources"][0]["symbols"]:
        stock_results.append(stock.run_for_symbol(symbol))
    save_data(stock_results, "data/stock_prices.csv")

    # Generate stock charts
    create_stock_price_chart("data/stock_prices.csv")

    # Append to history
    append_to_history("data/stock_prices.csv", "data/stock_history.csv", "symbol")

    # Generate charts
    create_stock_price_chart("data/stock_prices.csv")
    create_stock_price_trend("data/stock_history.csv")


if __name__ == "__main__":
    for i in range(10):
        run_scrapers()
        sleep(5)
