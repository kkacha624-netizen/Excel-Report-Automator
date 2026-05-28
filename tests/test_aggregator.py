import pandas as pd

from src.aggregator import aggregate_monthly_sales, normalize_sales_data


def test_monthly_sales_are_aggregated_correctly():
    df = pd.DataFrame(
        {
            "date": ["2026-01-01", "2026-01-15", "2026-02-01"],
            "amount": [1000, 2000, 3000],
        }
    )
    normalized = normalize_sales_data(df)

    result = aggregate_monthly_sales(normalized)

    january = result[result["month"] == "2026-01"].iloc[0]
    february = result[result["month"] == "2026-02"].iloc[0]
    assert january["total_amount"] == 3000
    assert january["order_count"] == 2
    assert february["total_amount"] == 3000
