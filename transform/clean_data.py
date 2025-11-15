# transform/clean_data.py
import pandas as pd
import logging

def clean_and_merge(customers, sales, returns):
    logger = logging.getLogger(__name__)
    logger.info("🧹 Rozpoczynam czyszczenie i transformację danych")

    # ------------------------------
    # 1️⃣ Konwersja typów
    # ------------------------------
    customers["customer_id"] = customers["customer_id"].astype("Int64")
    sales["customer_id"] = sales["customer_id"].astype("Int64")
    sales["sale_id"] = sales["sale_id"].astype("Int64")
    returns["sale_id"] = returns["sale_id"].astype("Int64")

    customers["join_date"] = pd.to_datetime(customers["join_date"], errors="coerce", dayfirst=True)
    sales["sale_date"] = pd.to_datetime(sales["sale_date"], errors="coerce", dayfirst=True)
    returns["return_date"] = pd.to_datetime(returns["return_date"], errors="coerce", dayfirst=True)

    # ------------------------------
    # 2️⃣ Czyszczenie braków
    # ------------------------------
    customers["email"] = customers["email"].fillna("unknown@example.com")
    customers["region"] = customers["region"].fillna("Unknown")
    returns["reason"] = returns["reason"].fillna("unknown")

    # Usuwanie wierszy z brakującymi lub niepoprawnymi wartościami
    sales = sales.dropna(subset=["quantity", "price"])
    sales = sales[(sales["quantity"] > 0) & (sales["price"] >= 0)]

    # Opcjonalnie wypełnienie brakujących dat sprzedaży domyślną
    sales["sale_date"] = sales["sale_date"].fillna(pd.Timestamp("2022-01-01"))

    # ------------------------------
    # 3️⃣ Walidacja
    # ------------------------------
    if not customers["customer_id"].is_unique:
        logger.warning("⚠️ Duplikaty w customer_id w customers")
        customers = customers.drop_duplicates(subset=["customer_id"])
    if not sales["sale_id"].is_unique:
        logger.warning("⚠️ Duplikaty w sale_id w sales")
        sales = sales.drop_duplicates(subset=["sale_id"])

    if sales["customer_id"].isna().any():
        logger.warning("⚠️ Braki w customer_id w sales")
        sales = sales.dropna(subset=["customer_id"])
    if returns["sale_id"].isna().any():
        logger.warning("⚠️ Braki w sale_id w returns")
        returns = returns.dropna(subset=["sale_id"])

    # ------------------------------
    # 4️⃣ Merge
    # ------------------------------
    df = sales.merge(customers, on="customer_id", how="left") \
              .merge(returns, on="sale_id", how="left")

    # ------------------------------
    # 5️⃣ Kalkulacje
    # ------------------------------
    df["total_value"] = df["price"] * df["quantity"]

    logger.info(f"✅ Transformacja zakończona: {len(df)} wierszy, kolumny={list(df.columns)}")
    return df