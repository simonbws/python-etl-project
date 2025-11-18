import requests
import pandas as pd
from pathlib import Path
from datetime import date
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_add_fx():
    today_str = date.today().strftime("%Y-%m-%d")
    project_root = Path(__file__).parent.parent
    analysis_folder = project_root / "analysis" / today_str
    analysis_folder.mkdir(parents=True, exist_ok=True)

    nbp_url = "https://api.nbp.pl/api/exchangerates/rates/A/EUR?format=json"
    logger.info(f"Pobieram kurs EUR z NBP: {nbp_url}")
    response = requests.get(nbp_url)
    response.raise_for_status()
    eur_data = response.json()

    eur_json_file = analysis_folder / "eur_rate.json"
    with open(eur_json_file, "w") as f:
        json.dump(eur_data, f, indent=4)
    logger.info(f"Kurs EUR zapisany w {eur_json_file}")

    sales_folder = Path("output")
    latest_folder = sorted(sales_folder.iterdir())[-1]
    sales_file = latest_folder / "sales_summary.parquet"
    logger.info(f"Wczytywanie danych sprzedaży: {sales_file}")
    sales_df = pd.read_parquet(sales_file)

    eur_rate = eur_data["rates"][0]["mid"] # only and first list element is [0] and "mid" is in dictionary
    sales_df["total_value_eur"] = sales_df["total_value"] / eur_rate

    output_file = analysis_folder / "sales_with_fx.parquet"
    sales_df.to_parquet(output_file, index = False)
    logger.info(f"Dane sprzedaży z przeliczeniem na EUR zapisane w {output_file}")

    print(sales_df.head())
    return sales_df

if __name__ == "__main__":
    run_add_fx()