from pathlib import Path
from datetime import datetime
import logging


def save_to_parquet(df, output_path: Path, save_index=False, versioned=True):
    logger = logging.getLogger(__name__)

    # Tworzenie wersjonowania danych
    if versioned:
        today = datetime.now().strftime("%Y-%m-%d")
        output_path = Path(output_path.parent) / today / output_path.name

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(output_path, index=save_index, engine="pyarrow")

    logger.info(f"💾 Zapisano Parquet do: {output_path.resolve()} (rows={len(df)})")

    return output_path