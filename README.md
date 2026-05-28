# CSV/Excel Report Generator

日本語CSV/Excelに対応した、定型レポート自動生成ツールです。

## Features

- CSV / Excelファイルの読み込み
- 複数ファイルの一括結合
- 日本語列名の自動判定
- 欠損値・不正値チェック
- 月別・カテゴリ別・商品別集計
- グラフ付きExcelレポート出力
- Streamlitによる簡易UI

## Demo

EC売上データを読み込み、月次売上レポートを自動生成します。

## Output

生成されるExcelには以下のシートが含まれます。

- README
- Summary
- Monthly_Summary
- Category_Summary
- Item_Summary
- Charts
- Data_Check
- Raw_Data

## Use Cases

- EC売上レポート作成
- 月次報告書作成
- 研究データ集計
- 事務作業の自動化
- CSV/Excel整形作業の効率化

## Tech Stack

- Python
- pandas
- openpyxl
- matplotlib
- Streamlit
- YAML
