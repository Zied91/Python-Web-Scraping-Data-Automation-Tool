# utils/chart_generator.py
import matplotlib.pyplot as plt
import pandas as pd

def create_crypto_price_chart(csv_file, output_file="charts/crypto_prices.png"):
    df = pd.read_csv(csv_file)

    df_top = df.head(10)  # top 10 cryptos

    plt.figure(figsize=(12, 6))
    plt.bar(df_top["name"], df_top["price"].str.replace("$", "").str.replace(",", "").astype(float))
    plt.xticks(rotation=45, ha='right')
    plt.title("Top 10 Crypto Prices")
    plt.ylabel("Price (USD)")
    plt.tight_layout()
    
    plt.savefig(output_file)
    plt.close()
    print(f"[CHART SAVED] {output_file}")


def create_crypto_change_chart(csv_file, output_file="charts/crypto_change.png"):
    df = pd.read_csv(csv_file)

    df_top = df.head(10)

    # Convert "% change" to float
    df_top["change_24h_float"] = df_top["change_24h"].str.replace("%", "").astype(float)

    colors = ["green" if x >= 0 else "red" for x in df_top["change_24h_float"]]

    plt.figure(figsize=(12, 6))
    plt.bar(df_top["name"], df_top["change_24h_float"], color=colors)
    plt.xticks(rotation=45, ha='right')
    plt.title("24h % Change of Top Cryptocurrencies")
    plt.ylabel("Change (%)")
    plt.tight_layout()
    
    plt.savefig(output_file)
    plt.close()
    print(f"[CHART SAVED] {output_file}")


def create_stock_price_chart(csv_file, output_file="charts/stock_prices.png"):
    df = pd.read_csv(csv_file)

    plt.figure(figsize=(10, 5))
    plt.bar(df["symbol"], df["price"].str.replace(",", "").astype(float))
    plt.title("Stock Price Comparison")
    plt.xlabel("Stock Symbol")
    plt.ylabel("Price (USD)")
    plt.tight_layout()

    plt.savefig(output_file)
    plt.close()
    print(f"[CHART SAVED] {output_file}")
