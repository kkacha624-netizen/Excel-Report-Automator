# src 関数リファレンス

このドキュメントは `src` フォルダ内のソースコードに定義されている関数の概要をまとめたものです。

## `src/__init__.py`

パッケージ説明用の docstring のみを持つファイルです。関数は定義されていません。

## `src/aggregator.py`

売上データの型変換、月別・カテゴリ別・商品別の集計、Summary シート向けの基本指標作成を担当します。

### `normalize_sales_data(df: pd.DataFrame) -> pd.DataFrame`

入力された売上データをコピーし、後続の検証・集計・Excel 出力で扱いやすい型へ変換します。

- `date` 列がある場合、`datetime` 型へ変換します。変換できない値は欠損値になります。
- `quantity`、`unit_price`、`amount` 列がある場合、数値型へ変換します。変換できない値は欠損値になります。
- 元の `DataFrame` は直接変更せず、変換後のコピーを返します。

### `aggregate_monthly_sales(df: pd.DataFrame) -> pd.DataFrame`

売上データを月単位で集計します。

- `date` 列から `YYYY-MM` 形式の `month` 列を作成します。
- 月ごとの売上合計を `total_amount` として集計します。
- 月ごとの注文件数を `order_count` として集計します。
- 月の昇順で並べた `DataFrame` を返します。

### `aggregate_category_sales(df: pd.DataFrame) -> pd.DataFrame`

カテゴリ別の売上集計を作成します。

- `category` 列でグループ化します。
- カテゴリごとの売上合計を `total_amount` として集計します。
- カテゴリごとの注文件数を `order_count` として集計します。
- 売上合計の降順で並べた `DataFrame` を返します。

### `aggregate_item_sales(df: pd.DataFrame) -> pd.DataFrame`

商品別の売上集計を作成します。

- `item` 列でグループ化します。
- 商品ごとの売上合計を `total_amount` として集計します。
- 商品ごとの販売数量合計を `quantity` として集計します。
- 商品ごとの注文件数を `order_count` として集計します。
- 売上合計の降順で並べ、インデックスを振り直した `DataFrame` を返します。

### `build_summary_metrics(df: pd.DataFrame) -> pd.DataFrame`

Summary シートに表示する基本指標をキー・バリュー形式で作成します。

- 総売上、注文件数、平均売上、最大売上、最小売上を算出します。
- `date` 列に有効な値がある場合、対象期間の開始日と終了日を算出します。
- `metric` と `value` の2列を持つ `DataFrame` を返します。

## `src/column_mapper.py`

入力ファイルの列名を標準列名へ変換する処理を担当します。

### `load_mapping(path: str | Path) -> dict[str, list[str]]`

YAML 形式の列名マッピングファイルを読み込みます。

- 指定されたパスの YAML ファイルを UTF-8 で開きます。
- YAML の内容が空の場合は空の辞書として扱います。
- 読み込んだ内容が辞書でない場合は `ValueError` を送出します。
- 標準列名と別名リストの対応を表す辞書を返します。

### `build_reverse_mapping(mapping: dict[str, list[str]]) -> dict[str, str]`

標準列名から別名リストへのマッピングを、入力列名から標準列名への逆引きマッピングに変換します。

- 標準列名自身も、同じ標準列名へ対応付けます。
- 各別名は前後の空白を除去してから標準列名へ対応付けます。
- `map_columns` で列名変換を行うための辞書を返します。

### `map_columns(df: pd.DataFrame, mapping: dict[str, list[str]]) -> pd.DataFrame`

入力データの列名を標準列名へ変換します。

- `build_reverse_mapping` で逆引きマッピングを作成します。
- マッピングに存在する列名は標準列名へ変更します。
- マッピングに存在しない列名は元の列名のまま残します。
- 列名を変更した `DataFrame` を返します。

## `src/comment_generator.py`

集計結果から Summary シート向けの短いコメントを生成します。

### `generate_summary_comments(summary_metrics: pd.DataFrame, category_summary: pd.DataFrame, item_summary: pd.DataFrame) -> list[str]`

基本指標、カテゴリ別集計、商品別集計から帳票用コメントを生成します。

- `summary_metrics` から総売上を取得し、総売上コメントを作成します。
- `category_summary` が空でなければ、先頭行のカテゴリを最も売上が高いカテゴリとしてコメント化します。
- `item_summary` が空でなければ、先頭行の商品を最も売上が高い商品としてコメント化します。
- 作成したコメント文字列のリストを返します。

## `src/loader.py`

CSV・Excel ファイルの読み込みと、複数ファイルの結合を担当します。

### `load_csv(path: str | Path) -> pd.DataFrame`

CSV ファイルを読み込みます。

- `utf-8`、`utf-8-sig`、`cp932` の順に文字コードを試します。
- 読み込みに成功した時点で `DataFrame` を返します。
- すべての文字コードで失敗した場合は、試行結果を含む `ValueError` を送出します。

### `load_excel(path: str | Path, sheet_name: str | int | None = 0) -> pd.DataFrame`

Excel ファイルを読み込みます。

- 指定されたパスの Excel ファイルを `pandas.read_excel` で読み込みます。
- 既定では先頭シートを読み込みます。
- `sheet_name` を指定すると、対象シートを変更できます。
- 読み込んだ内容を `DataFrame` として返します。

### `load_files(paths: list[str | Path]) -> pd.DataFrame`

複数の CSV・Excel ファイルを読み込み、1つの `DataFrame` に結合します。

- 拡張子が `.csv` の場合は `load_csv` を使います。
- 拡張子が `.xlsx` または `.xls` の場合は `load_excel` を使います。
- 未対応の拡張子が指定された場合は `ValueError` を送出します。
- ファイル指定が空の場合も `ValueError` を送出します。
- 読み込んだ複数の表を縦方向に結合し、インデックスを振り直して返します。

## `src/report_writer.py`

集計結果、検証結果、元データを Excel レポートとして出力する処理を担当します。

### `_append_dataframe(ws, df: pd.DataFrame) -> None`

`DataFrame` の内容を openpyxl のワークシートへ追記する内部ヘルパー関数です。

- ヘッダー行を含めて `DataFrame` を行データへ変換します。
- 変換した各行をワークシートへ追加します。
- 戻り値はありません。

### `_style_sheet(ws) -> None`

ワークシートに共通の見た目を適用する内部ヘルパー関数です。

- 1行目をヘッダー行として太字にします。
- ヘッダー行に薄い青色の塗りつぶしを設定します。
- 各列の内容に応じて列幅を調整します。
- 金額系の列は桁区切りの数値形式に設定します。
- 戻り値はありません。

### `_write_key_value_rows(ws, rows: Iterable[tuple[str, object]]) -> None`

キー・バリュー形式の行をワークシートへ書き込む内部ヘルパー関数です。

- 先頭に `項目`、`内容` のヘッダー行を追加します。
- 渡された `(key, value)` の組を順にワークシートへ追加します。
- 戻り値はありません。

### `write_report(output_path: str | Path, input_files: list[str | Path], summary_metrics: pd.DataFrame, comments: list[str], monthly_summary: pd.DataFrame, category_summary: pd.DataFrame, item_summary: pd.DataFrame, data_check: pd.DataFrame, raw_data: pd.DataFrame) -> Path`

Excel レポートファイルを作成します。

- 出力先ディレクトリが存在しない場合は作成します。
- デフォルトシートを削除し、用途別のシートを作成します。
- `README` シートにツール説明、生成日時、入力ファイル一覧を書き込みます。
- `Summary` シートに基本指標と自動生成コメントを書き込みます。
- `Monthly_Summary`、`Category_Summary`、`Item_Summary`、`Data_Check`、`Raw_Data` シートに各 `DataFrame` を出力します。
- すべてのシートに共通スタイルを適用します。
- Excel ファイルを保存し、保存先の `Path` を返します。

## `src/validator.py`

標準化済みの売上データに対して、必須列・日付・金額・数量・欠損・重複の検証を行います。

### `_result(check_name: str, status: str, message: str, count: int) -> dict[str, object]`

検証結果1件分の辞書を作成する内部ヘルパー関数です。

- チェック名、ステータス、メッセージ、件数を受け取ります。
- `count` は整数に変換します。
- `validate_data` が最終的に `DataFrame` 化するための辞書を返します。

### `validate_data(df: pd.DataFrame, high_amount_threshold: float = 1_000_000) -> pd.DataFrame`

売上データの品質チェックを行い、検証結果を `DataFrame` として返します。

- 必須列が不足していないかを確認します。不足がある場合は `ERROR` とします。
- `date` 列がある場合、日付に変換できない値を確認します。
- `amount` 列がある場合、数値変換できない金額、マイナス売上、しきい値超過の売上を確認します。
- `quantity` 列がある場合、数値変換できない数量を確認します。
- 表全体の欠損値数と重複行数を確認します。
- 検証結果は `check_name`、`status`、`message`、`count` の4列で返します。
