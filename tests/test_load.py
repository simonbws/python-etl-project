import pandas as pd
from pathlib import Path
from load.to_parquet import save_to_parquet
from unittest.mock import MagicMock

def test_save_to_parquet_mock(monkeypatch):
    df = pd.DataFrame({"a": [1, 2]})
    mock_to_parquet = MagicMock()
    monkeypatch.setattr(df, "to_parquet", mock_to_parquet)

    path = save_to_parquet(df, Path("output/test.parquet"))
    mock_to_parquet.assert_called_once()
    assert path.name == "test.parquet"