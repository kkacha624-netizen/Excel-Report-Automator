import pandas as pd


def generate_summary_comments(
    summary_metrics: pd.DataFrame,
    category_summary: pd.DataFrame,
    item_summary: pd.DataFrame,
) -> list[str]:
    """Generate simple rule-based comments for the Summary sheet."""
    # 基本指標とランキング先頭行から、帳票向けの短い所見を作る。
    metrics = dict(zip(summary_metrics["metric"], summary_metrics["value"], strict=False))
    total_amount = metrics.get("総売上", 0)

    comments = [f"対象期間の総売上は {float(total_amount):,.0f} 円です。"]

    if not category_summary.empty:
        top_category = category_summary.iloc[0]["category"]
        comments.append(f"最も売上が高いカテゴリは「{top_category}」です。")

    if not item_summary.empty:
        top_item = item_summary.iloc[0]["item"]
        comments.append(f"最も売上が高い商品は「{top_item}」です。")

    return comments
