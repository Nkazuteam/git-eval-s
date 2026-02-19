## 目的

Markdown ファイルから見出しを抽出し、目次 (Table of Contents) を自動生成する CLI ツール。
README を書くたびに手動で目次を管理する手間を省く。

## 技術選定

| 選択 | 理由 | 代替案 |
|---|---|---|
| Python 3.10+ | 文字列処理が得意。標準ライブラリだけで十分な規模 | Node.js — 同等だが正規表現の扱いが若干冗長 |
| argparse | 標準ライブラリ。サブコマンドもない単機能 CLI に click 等は不要 | click — 依存が増す割にメリットなし |
| dataclass | Heading の値オブジェクト。frozen で不変性を保証 | NamedTuple — ほぼ同等だが dataclass の方が拡張しやすい |
| pytest + pytest-cov | Python のテストデファクト。カバレッジ計測が容易 | unittest — 標準だが記述量が多い |
| flake8 | 軽量リンター。設定が少なく導入コストが低い | ruff — 高速だがここでは flake8 で十分 |

## 設計判断

- **3 モジュール分離** (`parser` / `generator` / `cli`):
  解析・生成・I/O の関心を分離。parser と generator は純粋関数で副作用がなく、テストが容易。
- **コードブロック除外**: fenced code block (```) 内の `#` 行は見出しとして誤検出しないようスキップ。
  完全な CommonMark パーサーを使う案もあるが、このユースケースでは過剰。
- **GitHub 互換 slug 生成**: アンカーリンクは GitHub の slug ルールに概ね準拠。
  完全再現は複雑になるため、ASCII + 基本的な Unicode に対応する範囲に留めた。

## 妥協点

- インデント付きコードブロックや HTML コメント内のヘッディングは検出してしまう可能性がある。
  正確に処理するには markdown-it 等のパーサーが必要だが、実用上ほぼ問題にならない。
- slug の日本語対応は簡易的。GitHub の実際の slug アルゴリズムを完全再現するには
  追加のライブラリが必要で、目的に対して過剰。
