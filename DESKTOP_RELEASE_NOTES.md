**English** · [简体中文](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.zh-CN.md) · [繁體中文](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.zh-TW.md) · [日本語](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ja.md) · [Deutsch](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.de.md) · [Français](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.fr.md) · [Español](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.es.md) · [Português (Brasil)](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.pt-BR.md) · [한국어](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ko.md) · [Italiano](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.it.md) · [Русский](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.ru.md) · [Polski](https://github.com/PandaKBLab/Vial-Multilingual/blob/main/docs/languages/README.pl.md)

PandaKB Vial is now available for Windows, macOS and Linux. All editions include the same 12 interface languages, default to English, and can restart automatically when you confirm a language change. **About Vial** credits the original contributors and PandaKB.

## Downloads

- [Windows (installer, x64)](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/PandaKB-Vial-v0.1.1-Windows-x64-setup.exe)
- [Windows (portable, x64)](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/PandaKB-Vial-v0.1.1-Windows-x64-portable.zip)
- [macOS (DMG, Apple silicon)](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/PandaKB-Vial-v0.1.1-macOS-arm64.dmg)
- [macOS (DMG, Intel)](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/PandaKB-Vial-v0.1.1-macOS-x86_64.dmg)
- [Linux (AppImage, x86_64)](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/PandaKB-Vial-v0.1.1-Linux-x86_64.AppImage)
- [Source code](https://github.com/PandaKBLab/Vial-Multilingual/tree/v0.1.1)
- [SHA-256 checksums](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/SHA256SUMS.txt)

## Installation

- **Windows:** Run the installer for a per-user installation with a Start menu shortcut, or fully extract the portable ZIP and open `Vial.exe`. The packages are unsigned, so SmartScreen may show “Unknown publisher”. [Microsoft SmartScreen guidance](https://learn.microsoft.com/windows/apps/package-and-deploy/smartscreen-reputation)
- **macOS:** Pick the DMG for your chip and drag **PandaKB Vial** into **Applications**. Apple has not notarized these builds, so macOS may block the first launch. [Apple security guidance](https://support.apple.com/en-us/102445). The macOS client can edit existing macros; live macro recording is unavailable.
- **Linux:** Mark the AppImage executable (for example, `chmod +x PandaKB-Vial-v0.1.1-Linux-x86_64.AppImage`). If no keyboard appears, follow the [Vial USB permissions guide](https://get.vial.today/manual/linux-udev.html). See the [AppImage FUSE guide](https://docs.appimage.org/user-guide/troubleshooting/fuse.html) if the file will not start.

## Validation

This release uses the packages from successful [macOS and Linux builds](https://github.com/PandaKBLab/Vial-Multilingual/actions/runs/43602452992) and the [Windows installer verification](https://github.com/PandaKBLab/Vial-Multilingual/actions/runs/43603042120). Automated checks opened the packaged interface in all 12 languages on Windows x64, macOS 15 for Apple silicon and Intel, and Ubuntu 22.04 x86_64. The Windows installer also passed installation, startup and uninstall checks. Physical keyboard detection, remapping and firmware flashing on macOS and Linux still need hardware testing.
