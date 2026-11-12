# PandaKB Vial Multilingual

**English** · [简体中文](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.zh-CN.md) · [繁體中文](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.zh-TW.md) · [日本語](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ja.md) · [Deutsch](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.de.md) · [Français](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.fr.md) · [Español](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.es.md) · [Português (Brasil)](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.pt-BR.md) · [한국어](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ko.md) · [Italiano](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.it.md) · [Русский](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ru.md) · [Polski](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.pl.md)

PandaKB maintains this portable Windows x64 edition of the open-source [Vial](https://get.vial.today/) keyboard configurator. It supports 12 interface languages and starts in English by default.

[Download v0.1.0](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0) · [Validation report](VALIDATION.md) · [Build checks](https://github.com/PandaKBLab/Vial-Multilingual/actions/workflows/build.yml)

## Getting started

1. Download the Windows x64 ZIP, extract it completely, and run `Vial.exe` from the extracted folder. Keep the accompanying files together.
2. Choose a language in **Settings → Language / 语言**. Vial remembers your choice.
3. Confirm to restart Vial automatically. Save or undo pending edits and finish any recording or firmware update before retrying.

## Windows first-run prompt

The portable build is unsigned. Windows SmartScreen may report an unknown publisher. Download the ZIP from the project’s release page and verify it against the `SHA256SUMS.txt` file on that page. [Microsoft SmartScreen documentation](https://learn.microsoft.com/windows/apps/package-and-deploy/smartscreen-reputation)

## v0.1.0

The stable release completes translations for built-in menus, advanced QMK settings, keycodes and tooltips, dynamic layers, MIDI, lighting effect names, device information, and firmware update messages. Standard keycap legends, QMK identifiers, device-provided names, and raw exception details retain their original values.

All 12 languages cover 767 of 767 catalogued interface entries. The build passed 67 automated tests and Windows application checks in all 12 languages. Physical keyboard flashing and unlocking still require hardware validation. [Release notes and downloads](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0)

## Development and license

This edition is based on [Vial upstream commit aef8222](https://github.com/vial-kb/vial-gui/commit/aef8222a2d0429a183b2ed692d5f9efcfd383f08) and uses the compatible Python 3.6 and Qt 5.9 build stack. GitHub Actions compiles the catalogs, checks placeholders and markup, runs regression tests, and packages the portable Windows app.

The translations live in [`translations/`](translations/). Run `python scripts/build_translations.py --strict` with Qt `lrelease` installed to validate the catalogs. Contributions that improve terminology are welcome.

About Vial credits the upstream contributors and displays **Modified by PandaKB**. See [COPYING](COPYING) and [NOTICE](NOTICE) for the GPL-2.0-or-later license and attribution.

## v0.1.0-preview.1

The first Windows x64 preview provides menus and common controls in 12 languages. Some advanced descriptions and lighting effect names fall back to English. Applying a language in this preview requires a manual restart. [Preview release](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0-preview.1)
