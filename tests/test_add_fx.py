import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from pathlib import Path
from scripts.add_fx import run_add_fx
from datetime import date, timedelta

def test_run_add_fx_mocked(tmp_path):
    today = date.today()
    yesterday = today - timedelta(days=1)

    # Tworzymy dwa foldery w tmp_path
    folder_old = tmp_path / yesterday.strftime("%Y-%m-%d")
    folder_new = tmp_path / today.strftime("%Y-%m-%d")
    folder_old.mkdir()
    folder_new.mkdir()

    # Mock odpowiedzi z API
    fake_response = MagicMock()
    fake_response.json.return_value = {"rates": [{"mid": 4.5}]}
    fake_response.raise_for_status = MagicMock()

    # Fake DataFrame sprzedaży
    fake_sales_df = pd.DataFrame({"total_value": [100], "region": ["North"]})

    with patch("scripts.add_fx.requests.get", return_value=fake_response), \
         patch("scripts.add_fx.Path.iterdir", return_value=[folder_old, folder_new]), \
         patch("pandas.read_parquet", return_value=fake_sales_df), \
         patch("pandas.DataFrame.to_parquet", MagicMock()), \
         patch("builtins.open", MagicMock()):
        df = run_add_fx()

    # Sprawdzenie wyników
    assert not df.empty
    assert "total_value_eur" in df.columns
    assert df["total_value_eur"].iloc[0] == 100 / 4.5