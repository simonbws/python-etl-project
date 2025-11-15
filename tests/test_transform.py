import pandas as pd
from transform.clean_data import clean_and_merge

def test_clean_and_merge_simple():
    customers = pd.DataFrame({"customer_id": [1], "email": [None], "region": [None], "join_date": ["01-01-2020"]})
    sales = pd.DataFrame({"sale_id": [1], "customer_id": [1], "product": ["A"], "quantity": [2], "price": [10], "sale_date": ["01-01-2021"]})
    returns = pd.DataFrame({"return_id": [1], "sale_id": [1], "return_date": ["02-01-2021"], "reason": [None]})

    df = clean_and_merge(customers, sales, returns)
    assert "total_value" in df.columns
    assert df["total_value"].iloc[0] == 20
    assert df["email"].iloc[0] == "unknown@example.com"