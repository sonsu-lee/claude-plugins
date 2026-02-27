---
name: ja-polish
description: >
  This skill should be used when the user asks to "polish Japanese text",
  "日本語をチェックして", "敬語を直して", "ビジネス日本語に直して", "日本語を
  ポリッシュして", or needs Japanese polishing for workplace Slack, business email,
  internal documents, reports, or formal requests. Also activated when any command
  references "ja-polish skill".
---

# 日本語ポリッシュ — 職場コミュニケーション向け

職場で使う自然なビジネス日本語に整える。正しい敬語をプラットフォームと
相手に合わせて適用する。

## Register Decision

コマンドの指定に応じて体を決定する:

- **丁寧語** (ます/です体): デフォルト。Slack、標準メール、報告
- **格式体** (だ/である体): 仕様書、正式文書、指定された報告書
- **セミカジュアル丁寧語**: 親しい同僚へのDM

一つのメッセージ内で体を混在させない。混在している場合は支配的な体に統一する。

詳細は `references/keigo-guide.md` 参照。

## Korean L1 Interference Detection

韓国語話者に特有のパターンを検出する:

- は/が の混同 (韓国語の 은/이 からの転移)
- 〜させていただきます の過剰使用 (韓国語 드리다 パターン)
- 文末パターンの転移 (〜です+ね の重複)
- 助詞の直訳による不自然な表現
- 韓国語 존댓말 の直訳
- 日本語に必要なクッション言葉の欠落
- 接続詞の不自然な使用 (그래서 → だから の直接使用)

詳細は `references/non-native-patterns.md` 参照。

## Multi-Pass Workflow

### Pass 1: 敬語の正確性

他のすべてに先立ち、敬語の誤りを修正する。

- 敬語動詞の形 (いただく vs もらう vs くださる)
- お/ご の接頭辞 (和語 → お, 漢語 → ご)
- 〜させていただきます — 本当に必要な場面のみ
- 敬語レベルの混在

詳細は `references/keigo-guide.md` 参照。

### Pass 2: 自然さとプラットフォーム適合

- `references/workplace-conventions.md` のプラットフォーム規範を適用
- メール: 定型文の正確性を確認 (Slackでは使わない)
- Slack: メールのように長くないか確認
- Korean interference パターンの修正
- 過剰な前置き (〜のですが の連鎖) をトリミング

### Pass 3: 一貫性

- 全体で一つの体
- 文末の統一 (〜です と 〜ます/〜ております の不規則な混在を避ける)
- 同一人物/組織への敬称の統一

## Output Format

1. ポリッシュ済みテキスト (貼り付け可能な状態)
2. 主な変更点の簡潔なメモ — 重要な変更がある場合のみ

軽微な修正ではメモを省略する。スキルのプロセスを説明しない。
