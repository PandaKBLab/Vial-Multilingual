# PandaKB Vial Multilingual · 日本語

[English](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/README.md) · [简体中文](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.zh-CN.md) · [繁體中文](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.zh-TW.md) · **日本語** · [Deutsch](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.de.md) · [Français](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.fr.md) · [Español](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.es.md) · [Português (Brasil)](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.pt-BR.md) · [한국어](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ko.md) · [Italiano](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.it.md) · [Русский](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ru.md) · [Polski](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.pl.md)

PandaKB が改変・保守するオープンソースの Vial キーボード設定ツールです。Windows x64 向けのポータブル版を提供します。UI は 12 言語に対応し、初回起動時は英語で表示されます。

[ダウンロード・リリース情報](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0) · [テスト結果](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/VALIDATION.md)

## 使い方

1. Windows x64 用の ZIP をすべて展開し、他のファイルと同じフォルダーにある `Vial.exe` を実行します。
2. **Settings → Language / 语言** で言語を選びます。選択した言語は保存されます。
3. 確認すると自動的に再起動します。未保存の編集がある場合は保存するか元に戻し、マクロの記録やファームウェア更新を終えてから再度選択してください。

## Windows の初回実行時の警告

ポータブル版は署名されていないため、SmartScreen に「発行元不明」と表示される場合があります。プロジェクトのリリースページから入手し、同ページの `SHA256SUMS.txt` で ZIP を確認してください。

## v0.1.0

安定版では、組み込みのメニュー、QMK の詳細設定、キーコードやツールチップの説明、照明効果名、デバイス情報、ファームウェア更新メッセージの翻訳がそろいました。標準のキー刻印、QMK 識別子、デバイスから取得した名前、例外の原文はそのまま表示されます。

各言語で組み込み UI の 767/767 項目を収録しています。67 件の自動テストと、パッケージ化した Windows アプリの全 12 言語での画面確認が完了しました。実機での書き込みとロック解除は未検証です。

[ダウンロード・リリース情報](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0)

## ライセンスとクレジット

「Vial について」には、元の開発者と GPL の情報に加え、**Modified by PandaKB** と表示されます。 [GPL-2.0-or-later](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/COPYING) · [NOTICE](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/NOTICE)

## v0.1.0-preview.1

最初の Windows x64 プレビュー版では、メニューと基本操作を 12 言語に対応させました。詳細説明や照明効果名の一部は英語で表示されます。言語の切り替え後は、アプリを手動で終了して起動し直します。

[ダウンロード・リリース情報](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0-preview.1)
