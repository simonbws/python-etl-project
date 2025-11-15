import argparse
import configparser
from pathlib import Path
from datetime import datetime

from utils.logging_setup import setup_logging
from extract.csv_reader import read_csv_files
from transform.clean_data import clean_and_merge
from load.to_parquet import save_to_parquet


def main():
    # --------------------
    # Argumenty CLI
    # --------------------
    parser = argparse.ArgumentParser(description="Mini ETL Pipeline")
    parser.add_argument("--input-folder", type=str, help="Folder z plikami CSV", default="data/raw")
    parser.add_argument("--output-file", type=str, help="Ścieżka do pliku wynikowego (nadpisze config)", default=None)
    parser.add_argument("--save-index", action="store_true", help="Zapisuj indeks w Parquet")
    args = parser.parse_args()

    # --------------------
    # Config
    # --------------------
    config = configparser.ConfigParser()
    config.read("config/settings.ini")

    # output z configu lub z CLI
    output_path = (
        Path(args.output_file)
        if args.output_file
        else Path(config["paths"]["output_file"])
    )

    # --------------------
    # Logowanie
    # --------------------
    logger, _ = setup_logging(Path("logs"))

    logger.info("🚀 Start MiniETL pipeline")
    start_time = datetime.now()

    try:
        # Extract
        customers, sales, returns = read_csv_files(Path(args.input_folder))

        # Transform
        df = clean_and_merge(customers, sales, returns)

        # Load
        save_to_parquet(df, output_path, save_index=args.save_index)

        logger.info("✅ Pipeline zakończony sukcesem")

    except Exception as e:
        logger.exception(f"❌ Błąd w pipeline: {e}")
        raise

    finally:
        logger.info(f"⏱️ Pipeline zakończony w: {datetime.now() - start_time}")


if __name__ == "__main__":
    main()