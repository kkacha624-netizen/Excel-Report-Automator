import pandas as pd

from src.validator import validate_data


def test_missing_required_columns_are_detected():
    df = pd.DataFrame({"date": ["2026-01-01"], "amount": [1000]})

    result = validate_data(df)
    required_check = result[result["check_name"] == "required_columns"].iloc[0]

    assert required_check["status"] == "ERROR"
    assert required_check["count"] > 0
