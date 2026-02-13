# AITest_Calc

Python（tkinter）で作成した、四則演算対応のシンプルなデスクトップ電卓です。

## 主な機能

- 四則演算（`+`, `-`, `×`, `÷`）
- 小数入力（`.`）
- 符号反転（`+/-`）
- バックスペース（`⌫`）
- クリア（`C`）/ オールクリア（`AC`）
- エラー表示
  - 0除算: `Error: Division by zero`
  - 不正な式: `Error`
- エラー後に数字を入力すると新しい計算を開始
- キーボード入力対応

## 動作環境

- Python 3.10 以上
- tkinter が利用可能な環境（Windows / macOS / Linux）

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
```

依存ライブラリは標準ライブラリのみのため、追加インストールは不要です。

## 実行方法

```bash
python calculator.py
```

## テスト実行

```bash
python -m unittest -v
```

## キーボード操作

- `0`〜`9` / `.`: 数字・小数点入力
- `+`, `-`, `*`, `/`: 演算子入力（`*` は `×`、`/` は `÷` として扱われます）
- `Enter`: 計算実行
- `BackSpace`: 1文字削除
- `Escape`: オールクリア

## 主要ファイル

- `calculator.py`: UI（tkinter）と計算ロジック
- `test_calculator.py`: `CalculatorEngine` のユニットテスト
- `specs/calculator_spec.md`: 仕様書
- `specs/calculator_mockup.md`: 画面モック
