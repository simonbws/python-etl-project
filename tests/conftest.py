import pandas as pd
import pytest

@pytest.fixture
def customers_df():
    return pd.DataFrame({
        "customer_id": [1, 2],
        "first_name": ["John", "Anna"],
        "last_name": ["Doe", "Smith"],
        "email": ["john@example.com", None],
        "join_date": ["01-01-2022", "05-03-2022"],
        "region": ["EU", None],
    })

@pytest.fixture
def sales_df():
    return pd.DataFrame({
        "sale_id": [10, 11],
        "customer_id": [1, 2],
        "product": ["Phone", "Laptop"],
        "quantity": [1, 2],
        "price": [500, 1200],
        "sale_date": ["12-01-2022", None],
    })

@pytest.fixture
def returns_df():
    return pd.DataFrame({
        "return_id": [99],
        "sale_id": [10],
        "return_date": ["15-01-2022"],
        "reason": [None],
    })