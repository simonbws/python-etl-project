import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from scripts.load_to_sql import run_load_to_sql


@pytest.fixture
def sample_parquet(tmp_path):
    df = pd.DataFrame({
        "customer_id": [1],
        "total_value": [100],
        "region": ["North"]
    })
    file = tmp_path / "sales_summary.parquet"
    df.to_parquet(file)
    return tmp_path


def test_run_load_to_sql_mocked(sample_parquet):
    """Test skrócony: zwraca DataFrame bez zapisu do SQL."""
    fake_engine = MagicMock()
    fake_conn = MagicMock()

    # Przygotowanie mockowanego df dla read_sql
    mock_summary_df = pd.DataFrame({"region": ["North"], "total_sales": [100]})

    with patch("scripts.load_to_sql.create_engine", return_value=fake_engine):
        fake_engine.connect.return_value.__enter__.return_value = fake_conn
        with patch("scripts.load_to_sql.Path.iterdir", return_value=[sample_parquet]), \
                patch("pandas.read_parquet", return_value=pd.DataFrame({
                    "customer_id": [1],
                    "total_value": [100],
                    "region": ["North"]
                })), \
                patch("pandas.read_sql", return_value=mock_summary_df), \
                patch("pathlib.Path.mkdir"), \
                patch("pandas.DataFrame.to_sql"), \
                patch("pandas.DataFrame.to_json"):
            df_summary = run_load_to_sql()

    # Sprawdzenie, że zwrócony DataFrame nie jest pusty i ma oczekiwane kolumny
    assert not df_summary.empty
    assert "region" in df_summary.columns
    assert "total_sales" in df_summary.columns
    assert df_summary["total_sales"].iloc[0] == 100