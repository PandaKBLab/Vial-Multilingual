# Vial Multilingual — PandaKB Edition

A multilingual desktop edition of [Vial](https://github.com/vial-kb/vial-gui), modified by **PandaKB**.
The About Vial dialog keeps upstream attribution and identifies PandaKB's modifications.

**Status: v0.1.0-preview.1 released, with partial translations.** This is not yet a fully translated production release.
The published build passed 44 automated tests and frozen-EXE startup/About checks in all 12 languages. See [validation results](VALIDATION.md).

## Download and run

Download [PandaKB Vial v0.1.0-preview.1 for Windows x64](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.0-preview.1/PandaKB-Vial-v0.1.0-preview.1-Windows-x64.zip).
Extract the ZIP and run **Vial/Vial.exe**.
See the [release page](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0-preview.1) for the checksum, screenshots and translation report.
Development packages remain available from successful [Windows portable builds](https://github.com/PandaKBLab/Vial-Multilingual/actions/workflows/build.yml).
Keep the entire Vial folder together. Python and Qt do not need to be installed.
Tagged releases appear under [Releases](https://github.com/PandaKBLab/Vial-Multilingual/releases).

The ZIP includes the license, source commit information, a translation coverage report and a SHA-256 checksum alongside the archive.

## Languages

English (default), 简体中文, 繁體中文, 日本語, Deutsch, Français, Español, Português (Brasil), 한국어, Italiano, Русский, Polski.

Choose **Settings → Language / 语言**. The preference is saved; close and reopen Vial when convenient to apply it.
The application does not automatically close, reconnect a keyboard or discard editor state when choosing a language.
Save pending macro or settings edits before closing, just as in upstream Vial.

All language resources are included for offline use. Missing translations fall back to English.
Menus, main editor tabs and common actions have initial translations in every language.
Advanced settings, effect names, detailed keycode tooltips, diagnostics and device-supplied descriptions are still being completed.
Technical identifiers such as QMK keycodes, USB IDs, macro data and protocol fields keep their original values.
VIA definition downloads retain upstream's network requirement.

## Build and quality checks

Source import, editing, testing and Windows packaging can all be performed on GitHub without a local checkout.
The upstream application is pinned to `aef8222a2d0429a183b2ed692d5f9efcfd383f08`; its original commit history and COPYING are preserved.

One workflow validates translation placeholders, generates Qt Linguist TS/QM files, runs upstream simulated-device regressions and PandaKB language tests, freezes the application and launches the actual EXE in all 12 languages.
Validation artifacts include screenshots, test results, resolved dependency versions and an honest extracted-string coverage report.
The initial build keeps upstream Python 3.6.8 / PyQt5 5.9.2 / fbs 0.9.0 / PyInstaller 3.4, with compatible packaging-tool pins.
This legacy stack will require a separate, tested modernization effort.

Translations are maintained as readable `translations/<locale>.json` dictionaries.
The cloud build emits context-specific `.ts` and `.qm` files from the actual source inventory.
`translations/core.json` defines the first-preview gate; this is not a claim of full UI coverage.
Stable `v*` tags without a prerelease suffix require complete extracted translations; source extraction and real-device acceptance must also be reviewed before tagging.
Prerelease tags such as `v0.1.0-preview.1` publish a GitHub prerelease after all build checks pass.

See [the implementation plan](IMPLEMENTATION.md) and [translation notes](translations/README.md).

## Attribution and license

Original Vial: the Vial contributors. Multilingual modifications: PandaKB.
This project retains upstream's GNU GPL version 2 or later notices; see [COPYING](COPYING) and [NOTICE](NOTICE).
This is a PandaKB modification, not an official upstream Vial release.
