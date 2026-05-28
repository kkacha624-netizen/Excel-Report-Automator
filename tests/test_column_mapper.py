import pandas as pd

from src.column_mapper import map_columns


def test_japanese_columns_are_mapped_to_standard_names():
    df = pd.DataFrame(
        {
            "注文日": ["2026-01-01"],
            "商品名": ["商品A"],
            "カテゴリ": ["食品"],
            "数量": [1],
            "単価": [100],
            "売上金額": [100],
            "都道府県": ["東京都"],
        }
    )
    mapping = {
        "date": ["注文日"],
        "item": ["商品名"],
        "category": ["カテゴリ"],
        "quantity": ["数量"],
        "unit_price": ["単価"],
        "amount": ["売上金額"],
        "region": ["都道府県"],
    }

    mapped = map_columns(df, mapping)

    assert list(mapped.columns) == [
        "date",
        "item",
        "category",
        "quantity",
        "unit_price",
        "amount",
        "region",
    ]
