import pandas as pd
import pytest
from pathlib import Path
from extract.csv_reader import read_csv_files
from transform.clean_data import clean_and_merge
from load.to_parquet import save_to_parquet

@pytest.fixture
def sample_csv(tmp_path):
    """Tworzy przykładowe pliki CSV w tmp_path z kolumnami potrzebnymi do transformacji."""
    # customers
    customers_csv = tmp_path / "customers.csv"
    customers_csv.write_text(
        "customer_id,first_name,last_name,email,join_date,region\n"
        "1,John,Doe,john@example.com,2022-01-01,North\n"
        "2,Jane,Smith,,2022-02-01,South\n"
    )

    # sales
    sales_csv = tmp_path / "sales.csv"
    sales_csv.write_text(
        "sale_id,customer_id,product,quantity,price,sale_date\n"
        "10,1,Widget,5,100,2022-03-01\n"
        "11,2,Gadget,2,50,\n"
    )

    # returns
    returns_csv = tmp_path / "returns.csv"
    returns_csv.write_text(
        "return_id,sale_id,return_date,reason\n"
        "100,10,2022-03-05,\n"
        "101,11,,Late delivery\n"
    )

    return tmp_path

def test_pipeline_e2e(tmp_path, sample_csv):
    # Extract
    customers, sales, returns = read_csv_files(sample_csv)

    #Transform
    df = clean_and_merge(customers, sales, returns)

    # Sprawdzenie transformacji
    assert "total_value" in df.columns
    assert df["quantity"].notna().all()
    assert df["customer_id"].notna().all()

    # Load
    output_file = tmp_path / "output.parquet"
    saved_path = save_to_parquet(df, output_file, save_index=False, versioned=True)

    # Sprawdzenie zapisu
    assert saved_path.exists()
    # Plik powinien być w folderze z dzisiejszą datą
    today = pd.Timestamp.now().strftime("%Y-%m-%d")
    assert today in str(saved_path)