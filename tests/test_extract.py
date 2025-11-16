import pandas as pd
from pathlib import Path
from extract.csv_reader import read_csv_files

def test_read_csv_files_mock(monkeypatch):
    fake_df = pd.DataFrame({"customer_id": [1], "name": ["Alice"]})

    def fake_read_csv(path):
        return fake_df

    # podmiana pandas.read_csv na fake_read_csv
    monkeypatch.setattr("pandas.read_csv", fake_read_csv)

    customers, sales, returns = read_csv_files(Path("fake/folder"))
    assert len(customers) == 1
    assert customers["name"].iloc[0] == "Alice"