from pathlib import Path

import pandas as pd
import yaml


REQUIRED_COLUMNS = ["date", "item", "category", "quantity", "unit_price", "amount", "region"]


def load_mapping(path: str | Path) -> dict[str, list[str]]:
    """Load a YAML column mapping file."""
    mapping_path = Path(path)
    with mapping_path.open("r", encoding="utf-8") as file:
        mapping = yaml.safe_load(file) or {}

    if not isinstance(mapping, dict):
        raise ValueError(f"列名マッピングの形式が不正です: {mapping_path}")

    return mapping


def build_reverse_mapping(mapping: dict[str, list[str]]) -> dict[str, str]:
    """Build a lookup from source column names to standard column names."""
    reverse_mapping: dict[str, str] = {}
    # YAMLの標準列名 -> 別名リストを、入力列名 -> 標準列名へ反転する。
    for standard_name, aliases in mapping.items():
        reverse_mapping[standard_name] = standard_name
        for alias in aliases or []:
            reverse_mapping[str(alias).strip()] = standard_name
    return reverse_mapping


def map_columns(df: pd.DataFrame, mapping: dict[str, list[str]]) -> pd.DataFrame:
    """Rename Japanese columns to standard names and keep unknown columns as-is."""
    reverse_mapping = build_reverse_mapping(mapping)
    # 未対応の列は元の列名を維持し、後続処理で必要な列だけを標準名で扱う。
    rename_map = {
        column: reverse_mapping.get(str(column).strip(), column)
        for column in df.columns
    }
    return df.rename(columns=rename_map)
