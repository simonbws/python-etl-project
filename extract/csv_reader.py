# extract/csv_reader.py
import pandas as pd
from pathlib import Path
import logging

def read_csv_files(input_folder: Path):
    logger = logging.getLogger(__name__)
    logger.info(f"📥 Wczytywanie danych z folderu: {input_folder}")

    customers = pd.read_csv(input_folder / "customers.csv")
    sales = pd.read_csv(input_folder / "sales.csv")
    returns = pd.read_csv(input_folder / "returns.csv")

    logger.info(f"Wczytano: customers={len(customers)}, sales={len(sales)}, returns={len(returns)}")

    return customers, sales, returns