---
description: 丁寧語を格式体に変換する
argument-hint: テキスト
---

Apply the ja-polish skill to the following text.

Context: register conversion (丁寧語 → 格式体)
Register: 格式体 output

Hard rules:
- です/ます → だ/である に変換する
- 敬語表現を除去する（格式体は中立的な文体）
- 専門用語はそのまま保持する

Text to polish:
$ARGUMENTS
