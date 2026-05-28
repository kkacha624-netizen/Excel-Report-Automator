import pandas as pd

from src.column_mapper import REQUIRED_COLUMNS


def _result(check_name: str, status: str, message: str, count: int) -> dict[str, object]:
    return {
        "check_name": check_name,
        "status": status,
        "message": message,
        "count": int(count),
    }


def validate_data(df: pd.DataFrame, high_amount_threshold: float = 1_000_000) -> pd.DataFrame:
    """Validate normalized sales data and return check results."""
    results: list[dict[str, object]] = []

    # 必須列不足は後続の集計に直結するためERRORとして扱う。
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    results.append(
        _result(
            "required_columns",
            "ERROR" if missing_columns else "OK",
            "不足列: " + ", ".join(missing_columns) if missing_columns else "必須列はすべて存在します。",
            len(missing_columns),
        )
    )

    if "date" in df.columns:
        # 変換できない日付だけを検出し、空欄は欠損値チェック側で数える。
        invalid_dates = pd.to_datetime(df["date"], errors="coerce").isna() & df["date"].notna()
        results.append(
            _result(
                "invalid_date",
                "ERROR" if invalid_dates.any() else "OK",
                "日付に変換できない値があります。" if invalid_dates.any() else "日付は正常です。",
                int(invalid_dates.sum()),
            )
        )

    if "amount" in df.columns:
        # 金額は不正値、マイナス値、しきい値超過を分けて報告する。
        amount = pd.to_numeric(df["amount"], errors="coerce")
        invalid_amount = amount.isna() & df["amount"].notna()
        negative_amount = amount < 0
        high_amount = amount > high_amount_threshold
        results.extend(
            [
                _result(
                    "invalid_amount",
                    "ERROR" if invalid_amount.any() else "OK",
                    "金額に数値変換できない値があります。" if invalid_amount.any() else "金額は正常です。",
                    int(invalid_amount.sum()),
                ),
                _result(
                    "negative_amount",
                    "WARNING" if negative_amount.any() else "OK",
                    "マイナス売上があります。" if negative_amount.any() else "マイナス売上はありません。",
                    int(negative_amount.sum()),
                ),
                _result(
                    "large_amount",
                    "WARNING" if high_amount.any() else "OK",
                    f"{high_amount_threshold:,.0f}円を超える売上があります。"
                    if high_amount.any()
                    else "異常に大きい売上はありません。",
                    int(high_amount.sum()),
                ),
            ]
        )

    if "quantity" in df.columns:
        quantity = pd.to_numeric(df["quantity"], errors="coerce")
        invalid_quantity = quantity.isna() & df["quantity"].notna()
        results.append(
            _result(
                "invalid_quantity",
                "ERROR" if invalid_quantity.any() else "OK",
                "数量に数値変換できない値があります。" if invalid_quantity.any() else "数量は正常です。",
                int(invalid_quantity.sum()),
            )
        )

    missing_values = int(df.isna().sum().sum())
    duplicated_rows = int(df.duplicated().sum())
    # 表全体で見たデータ品質の注意点をWARNINGとしてまとめる。
    results.extend(
        [
            _result(
                "missing_values",
                "WARNING" if missing_values else "OK",
                "欠損値があります。" if missing_values else "欠損値はありません。",
                missing_values,
            ),
            _result(
                "duplicated_rows",
                "WARNING" if duplicated_rows else "OK",
                "重複行があります。" if duplicated_rows else "重複行はありません。",
                duplicated_rows,
            ),
        ]
    )

    return pd.DataFrame(results, columns=["check_name", "status", "message", "count"])
