from pathlib import Path
from collections.abc import Sequence
from pyparsing import Suppress

from src.aggregator import (
    aggregate_category_sales,
    aggregate_item_sales,
    aggregate_monthly_sales,
    build_summary_metrics,
    normalize_sales_data,
)
from src.column_mapper import load_mapping, map_columns
from src.comment_generator import generate_summary_comments
from src.loader import get_fileNames, load_files, SupportedSuffix
from src.report_writer import write_report
from src.validator import validate_data


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
MAPPING_FILE = BASE_DIR / "config" / "default_mapping.yml"
OUTPUT_FILE = BASE_DIR / "outputs" / "report.xlsx"


def main() -> None:
    input_files = [DATA_DIR / fileName for fileName in get_fileNames(DATA_DIR, SupportedSuffix)]

    # 入力データを読み込み、外部設定に従って列名を標準化する。
    raw_df = load_files(input_files)
    mapping = load_mapping(MAPPING_FILE)
    mapped_df = map_columns(raw_df, mapping)
    normalized_df = normalize_sales_data(mapped_df)

    # 整形済みデータからチェック結果、集計表、Summary用コメントを作成する。
    data_check = validate_data(normalized_df)
    monthly_summary = aggregate_monthly_sales(normalized_df)
    category_summary = aggregate_category_sales(normalized_df)
    item_summary = aggregate_item_sales(normalized_df)
    summary_metrics = build_summary_metrics(normalized_df)
    comments = generate_summary_comments(summary_metrics, category_summary, item_summary)

    # Excel帳票として、各DataFrameを指定シートへ出力する。
    report_path = write_report(
        output_path=OUTPUT_FILE,
        input_files=input_files,
        summary_metrics=summary_metrics,
        comments=comments,
        monthly_summary=monthly_summary,
        category_summary=category_summary,
        item_summary=item_summary,
        data_check=data_check,
        raw_data=normalized_df,
    )

    print(f"レポートを生成しました: {report_path}")


if __name__ == "__main__":
    main()
