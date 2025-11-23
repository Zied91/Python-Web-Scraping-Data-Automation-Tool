# utils/history.py
import pandas as pd
import os
from datetime import datetime

def append_to_history(source_file, history_file, id_column):
    """
    Appends the latest scraped data to a historical file.
    
    id_column: 'name' for crypto, 'symbol' for stocks
    """
    # Load latest
    df = pd.read_csv(source_file)
    df["timestamp"] = datetime.now()

    # Create history file if missing
    if not os.path.exists(history_file):
        df.to_csv(history_file, index=False)
        print(f"[HISTORY CREATED] {history_file}")
        return

    # Append
    existing = pd.read_csv(history_file)
    updated = pd.concat([existing, df], ignore_index=True)
    updated.to_csv(history_file, index=False)

    print(f"[HISTORY UPDATED] {history_file}")
