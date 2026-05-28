from pathlib import Path

import pandas as pd


ENCODINGS = ("utf-8", "utf-8-sig", "cp932")


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV file while trying common Japanese encodings."""
    csv_path = Path(path)
    errors: list[str] = []

    # 日本語業務CSVでよく使われる文字コードを順番に試す。
    for encoding in ENCODINGS:
        try:
            return pd.read_csv(csv_path, encoding=encoding)
        except UnicodeDecodeError as exc:
            errors.append(f"{encoding}: {exc}")

    raise ValueError(
        f"CSVファイルの文字コードを判定できませんでした: {csv_path}\n" + "\n".join(errors)
    )


def load_excel(path: str | Path, sheet_name: str | int | None = 0) -> pd.DataFrame:
    """Load an Excel file."""
    excel_path = Path(path)
    return pd.read_excel(excel_path, sheet_name=sheet_name)


def load_files(paths: list[str | Path]) -> pd.DataFrame:
    """Load multiple CSV/Excel files and combine them into one DataFrame."""
    frames: list[pd.DataFrame] = []

    # 拡張子ごとに読み込み関数を切り替え、最後に1つの表へ結合する。
    for path in paths:
        file_path = Path(path)
        suffix = file_path.suffix.lower()
        if suffix == ".csv":
            frames.append(load_csv(file_path))
        elif suffix in {".xlsx", ".xls"}:
            frames.append(load_excel(file_path))
        else:
            raise ValueError(f"未対応のファイル形式です: {file_path}")

    if not frames:
        raise ValueError("読み込むファイルが指定されていません。")

    return pd.concat(frames, ignore_index=True)
