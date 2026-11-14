# PandaKB Vial Multilingual

**English** · [简体中文](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.zh-CN.md) · [繁體中文](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.zh-TW.md) · [日本語](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ja.md) · [Deutsch](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.de.md) · [Français](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.fr.md) · [Español](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.es.md) · [Português (Brasil)](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.pt-BR.md) · [한국어](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ko.md) · [Italiano](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.it.md) · [Русский](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ru.md) · [Polski](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.pl.md)

PandaKB maintains this edition of the open-source [Vial](https://get.vial.today/) keyboard configurator for Windows, macOS and Linux. The interface supports 12 languages and starts in English by default.

## Downloads

- [Windows (installer, x64)](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/PandaKB-Vial-v0.1.1-Windows-x64-setup.exe)
- [Windows (portable, x64)](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/PandaKB-Vial-v0.1.1-Windows-x64-portable.zip)
- [macOS (DMG, Apple silicon)](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/PandaKB-Vial-v0.1.1-macOS-arm64.dmg)
- [macOS (DMG, Intel)](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/PandaKB-Vial-v0.1.1-macOS-x86_64.dmg)
- [Linux (AppImage, x86_64)](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/PandaKB-Vial-v0.1.1-Linux-x86_64.AppImage)
- [Source code](https://github.com/PandaKBLab/Vial-Multilingual/tree/v0.1.1)
- [SHA-256 checksums](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/SHA256SUMS.txt)

[Latest release notes](https://github.com/PandaKBLab/Vial-Multilingual/releases/latest) · [Validation report](VALIDATION.md) · [Build checks](https://github.com/PandaKBLab/Vial-Multilingual/actions/workflows/build.yml)

## Getting started

- **Windows:** Run the installer for a per-user installation with a Start menu shortcut, or fully extract the portable ZIP and open `Vial.exe`. The packages are unsigned, so SmartScreen may show “Unknown publisher”. [Microsoft SmartScreen guidance](https://learn.microsoft.com/windows/apps/package-and-deploy/smartscreen-reputation)
- **macOS:** Pick the DMG for your chip and drag **PandaKB Vial** into **Applications**. Apple has not notarized these builds, so macOS may block the first launch. [Apple security guidance](https://support.apple.com/en-us/102445). The macOS client can edit existing macros; live macro recording is unavailable.
- **Linux:** Mark the AppImage executable (for example, `chmod +x PandaKB-Vial-v0.1.1-Linux-x86_64.AppImage`). If no keyboard appears, follow the [Vial USB permissions guide](https://get.vial.today/manual/linux-udev.html). See the [AppImage FUSE guide](https://docs.appimage.org/user-guide/troubleshooting/fuse.html) if the file will not start.

Choose a language under **Settings → Language / 语言**. Save or undo pending edits and finish any recording or firmware update before confirming the automatic restart.

## v0.1.0

The stable release completes translations for built-in menus, advanced QMK settings, keycodes and tooltips, dynamic layers, MIDI, lighting effect names, device information, and firmware update messages. Standard keycap legends, QMK identifiers, device-provided names, and raw exception details retain their original values.

All 12 languages cover 767 of 767 catalogued interface entries. The build passed 67 automated tests and Windows application checks in all 12 languages. Physical keyboard flashing and unlocking still require hardware validation. [Release notes and downloads](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0)

## Development and license

This edition is based on [Vial upstream commit aef8222](https://github.com/vial-kb/vial-gui/commit/aef8222a2d0429a183b2ed692d5f9efcfd383f08) and keeps the legacy Python 3.6 and Qt 5.9 Windows build. Linux and macOS use Python 3.11 and Qt 5.15. GitHub Actions checks the translation catalogs, runs regression tests, and tests each platform's packages.

The translations live in [`translations/`](translations/). Run `python scripts/build_translations.py --strict` with Qt `lrelease` installed to validate the catalogs. Contributions that improve terminology are welcome.

About Vial credits the upstream contributors and displays **Modified by PandaKB**. See [COPYING](COPYING) and [NOTICE](NOTICE) for the GPL-2.0-or-later license and attribution.

## v0.1.0-preview.1

The first Windows x64 preview provides menus and common controls in 12 languages. Some advanced descriptions and lighting effect names fall back to English. Applying a language in this preview requires a manual restart. [Preview release](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0-preview.1)
