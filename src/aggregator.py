import pandas as pd


def normalize_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Convert key columns to practical dtypes for validation, aggregation, and output."""
    normalized = df.copy()
    # 集計やExcel出力で扱いやすいよう、日付と数値列を先に型変換する。
    if "date" in normalized.columns:
        normalized["date"] = pd.to_datetime(normalized["date"], errors="coerce")
    for column in ("quantity", "unit_price", "amount"):
        if column in normalized.columns:
            normalized[column] = pd.to_numeric(normalized[column], errors="coerce")
    return normalized


def aggregate_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    monthly = df.copy()
    # 月次レポート用に日付をYYYY-MM形式へ丸めて集計する。
    monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
    return (
        monthly.groupby("month", as_index=False)
        .agg(total_amount=("amount", "sum"), order_count=("amount", "count"))
        .sort_values("month")
    )


def aggregate_category_sales(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category", as_index=False)
        .agg(total_amount=("amount", "sum"), order_count=("amount", "count"))
        .sort_values("total_amount", ascending=False)
    )


def aggregate_item_sales(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("item", as_index=False)
        .agg(total_amount=("amount", "sum"), quantity=("quantity", "sum"), order_count=("amount", "count"))
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def build_summary_metrics(df: pd.DataFrame) -> pd.DataFrame:
    # Summaryシートでそのまま表示しやすいキー・バリュー形式にする。
    metrics = [
        ("総売上", df["amount"].sum()),
        ("注文件数", int(df["amount"].count())),
        ("平均売上", df["amount"].mean()),
        ("最大売上", df["amount"].max()),
        ("最小売上", df["amount"].min()),
        ("対象期間開始日", df["date"].min().date() if df["date"].notna().any() else ""),
        ("対象期間終了日", df["date"].max().date() if df["date"].notna().any() else ""),
    ]
    return pd.DataFrame(metrics, columns=["metric", "value"])
