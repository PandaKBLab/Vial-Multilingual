# Desktop package validation — 2026-11-14

Published version: [v0.1.1](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.1). Windows binaries: [tested source 288f517](https://github.com/PandaKBLab/Vial-Multilingual/commit/288f51724b05ec34bab5f076e3bf04b7c30a5a12) · [Windows build 43603042120](https://github.com/PandaKBLab/Vial-Multilingual/actions/runs/43603042120). macOS and Linux binaries: [tested source 56cb7d9](https://github.com/PandaKBLab/Vial-Multilingual/commit/56cb7d919086860dcecdf93586c0a9ff90dbc359) · [native builds 43602452992](https://github.com/PandaKBLab/Vial-Multilingual/actions/runs/43602452992). The source changes between the builds affect only Windows installer packaging and its test, plus the CI branch selection.

- Windows x64: frozen executable checked in all 12 languages. The per-user installer was installed, launched and uninstalled; an unrelated file in its folder survived removal.
- macOS: separate Apple silicon and Intel DMGs, mounted and launched in all 12 languages on macOS 15. The executable architecture and ad-hoc bundle signature were verified.
- Linux x86_64: AppImage launched in all 12 languages on Ubuntu 22.04, using an X11 test display and the runtime's extraction mode. The HID backend loaded and enumerated without a physical keyboard.
- For each packaged interface, the simulated keyboard exposed 11 editor pages and all 7 advanced settings tabs. Checks include localizing standard buttons, RGB labels, keycode hints and explanatory label widths. All 12 translation catalogs passed the strict check.
- Language restart tests cover the process handoff and reopening an AppImage. Physical keyboard detection, remapping, unlocking, recording and flashing on the new platforms still require hardware testing. Windows packages are unsigned; the macOS packages are not notarized by Apple.

The release provides [SHA-256 checksums](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.1/SHA256SUMS.txt) for all five binaries and ZIPs.

---

# Full-release validation — 2026-11-12

Published version: [v0.1.0](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0).

Application source: [`ec3a11a5bc862092d294074afa768afe10e29d38`](https://github.com/PandaKBLab/Vial-Multilingual/commit/ec3a11a5bc862092d294074afa768afe10e29d38).
Upstream: `vial-kb/vial-gui` at `aef8222a2d0429a183b2ed692d5f9efcfd383f08`.

## Reproducible checks

- [Windows build and tests](https://github.com/PandaKBLab/Vial-Multilingual/actions/runs/43195978331): complete catalogs, Python compilation, upstream regressions and PandaKB language/restart tests.
- 67 automated tests passed, including all compiled translation entries, dynamic keycode descriptions, restart failure handling, pending-edit/recording guards, process handoff, and key-override option-to-firmware correspondence.
- The actual frozen `Vial.exe` ran successfully in all 12 languages on the native Windows Qt platform.
- Each language opened 11 editor pages and all 7 advanced-settings tabs using a synthetic keyboard; all pages were explicitly required to be visible. The fixture exposes 45 Vial RGB effects.
- Automated checks reported no explanatory-label width overflow. Screenshots of Chinese settings, Japanese lighting, Korean key mapping, German key overrides, Polish alternative repeat, Russian mouse settings and Traditional Chinese About were visually reviewed.
- Standard Qt confirmation buttons were localized. About retains upstream attribution, GPL and the fixed credit **Modified by PandaKB**.
- ZIP contents include all language catalogs, the Qt Windows platform plugin, HID backend, GPL license, notice, README and the tested source commit.
- Publication reuses the exact tested ZIP; only the public filename and checksum-sidecar line endings are normalized.

## Translation coverage

Every language has **767 / 767** extracted context/source entries (100%): English, Simplified Chinese, Traditional Chinese, Japanese, German, French, Spanish, Brazilian Portuguese, Korean, Italian, Russian and Polish.

The inventory includes built-in menus, advanced settings, keycode and MIDI descriptions, dynamic-layer tooltips, 81 lighting-effect names, firmware-updater messages and device information. Standard keycap legends, QMK identifiers, firmware-provided custom names and raw exception diagnostics retain their supplied values. Catalog coverage establishes that translations are supplied and loaded, not a native-speaker linguistic certification.

## Restart and limitations

Language selection is persisted. Confirming restart starts the replacement process, closes the old window and waits for the old process to exit before opening hardware in the new process. Pending macro/settings edits, recording and locked operations prevent restart. Tests exercise the launch command and failure paths with controlled process launching; they are not a physical-device reconnect endurance test.

Physical keyboard reads/writes, actual flashing and unlock sequences, manufacturer-specific firmware behavior, clean Windows 10/11 installations and every display scale have not been verified. Simulated protocol tests and packaged Windows UI checks do not replace hardware acceptance testing.

This release is **unsigned** at the owner's request. Windows SmartScreen may still show “unknown publisher”; no security settings are disabled.

Reports and selected screenshots are attached to the release. Complete screenshots and diagnostics are available in the build's `validation-report` artifact.

## Published artifact

- [Exact-artifact publication](https://github.com/PandaKBLab/Vial-Multilingual/actions/runs/43197207128): successful.
- ZIP: [PandaKB-Vial-v0.1.0-Windows-x64.zip](https://github.com/PandaKBLab/Vial-Multilingual/releases/download/v0.1.0/PandaKB-Vial-v0.1.0-Windows-x64.zip) (26,673,728 bytes).
- SHA-256: `19c63b407739a5ed984c73dc55f1ee1d3e2fdf247695508cba4967e27355e836`.
- [Selected review screenshots](https://github.com/PandaKBLab/Vial-Multilingual/tree/validation/run-43195978331/validation/screenshots).
