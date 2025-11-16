import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from datetime import datetime
import logging



# Ustawienia logowania

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Parametry połączenia

server = "DESKTOP-C0TU3RB"
database = "MiniETL_DB"
driver = "ODBC Driver 18 for SQL Server"


# Połączenie z master (tworzenie bazy, jeśli nie istnieje)

master_conn_str = (
    f"mssql+pyodbc://@{server}/master"
    f"?driver={driver.replace(' ', '+')}"
    f"&trusted_connection=yes"
    f"&TrustServerCertificate=yes"
)
master_engine = create_engine(master_conn_str)

with master_engine.connect() as conn:
    conn.execution_options(isolation_level="AUTOCOMMIT").execute(
        text(f"IF DB_ID('{database}') IS NULL CREATE DATABASE {database}")
    )
logger.info(f"Baza danych '{database}' istnieje lub została utworzona.")


# Połączenie z bazą

db_conn_str = (
    f"mssql+pyodbc://@{server}/{database}"
    f"?driver={driver.replace(' ', '+')}"
    f"&trusted_connection=yes"
    f"&TrustServerCertificate=yes"
)
engine = create_engine(db_conn_str)


# Wczytanie przetworzonych danych z Parquet

project_root = Path(__file__).parent.parent
output_base = project_root / "output"

if not output_base.exists():
    raise FileNotFoundError(f"Folder 'output' nie istnieje pod ścieżką: {output_base}")
output_folder = sorted(output_base.iterdir())[-1]

sales_file = output_folder /  "sales_summary.parquet"


if not sales_file.exists():
    raise FileNotFoundError("Nie znaleziono plików Parquet w folderze output.")

logger.info(f"Wczytywanie Parquet: {sales_file}")
sales_df = pd.read_parquet(sales_file)


# Zapis do SQL Server

sales_df.to_sql("sales", engine, if_exists="replace", index=False)
logger.info("Dane zapisane do SQL Server: tabele 'sales' i 'customers'")


# zapytanie SQL z join i sumowaniem

query = """
SELECT region, SUM(total_value) AS total_sales
FROM sales
GROUP BY region
"""
df_summary = pd.read_sql(query, engine)


# Zapis wyniku do JSON

analysis_base = project_root / "analysis"
today_str = datetime.now().strftime("%Y-%m-%d")
analysis_folder = analysis_base / today_str
analysis_folder.mkdir(parents=True, exist_ok=True)

output_json = analysis_folder / "sales_summary_per_region.json"
df_summary.to_json(output_json, orient="records", indent=4)
logger.info(f" Podsumowanie zapisane do JSON: {output_json}")


print(df_summary)