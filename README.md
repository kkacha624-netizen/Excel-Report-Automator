# CSV/Excel Report Generator

日本語CSV/Excelに対応した、定型レポート自動生成ツールです。  
MVPではEC売上データを読み込み、データチェック、売上集計、Excel帳票出力までをCLIで自動化します。

## Features

- CSV / Excelファイルの読み込み
- 複数ファイルの一括結合
- 日本語列名の自動判定と標準列名への変換
- 欠損値、不正日付、不正数値、重複行、マイナス売上、異常値のチェック
- 月別、カテゴリ別、商品別の売上集計
- Summaryコメントのルールベース自動生成
- openpyxlによるExcelレポート出力

## Directory Structure

```text
csv-excel-report-generator/
├─ README.md
├─ app.py
├─ requirements.txt
├─ config/
│  └─ default_mapping.yml
├─ data/
│  └─ sample_sales.csv
├─ outputs/
├─ src/
│  ├─ __init__.py
│  ├─ loader.py
│  ├─ column_mapper.py
│  ├─ validator.py
│  ├─ aggregator.py
│  ├─ report_writer.py
│  └─ comment_generator.py
└─ tests/
   ├─ test_column_mapper.py
   ├─ test_validator.py
   └─ test_aggregator.py
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

実行後、以下のExcelファイルが生成されます。

```text
outputs/report.xlsx
```

## Output Sheets

- `README`: ツール説明、生成日時、入力ファイル情報
- `Summary`: 基本指標と自動生成コメント
- `Monthly_Summary`: 月別売上集計
- `Category_Summary`: カテゴリ別売上集計
- `Item_Summary`: 商品別売上ランキング
- `Data_Check`: データチェック結果
- `Raw_Data`: 標準列名に整形した元データ

## Tests

```bash
pytest
```

## Future Improvements

- Streamlit UIの追加
- 複数入力ファイルを画面から選択する機能
- Excel内グラフの追加
- 列名マッピング候補のユーザー編集
- 売上以外の業務データテンプレート対応
