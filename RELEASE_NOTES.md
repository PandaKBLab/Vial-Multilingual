PandaKB's first Windows x64 multilingual preview, based on upstream Vial 0.7.5.

- About Vial explicitly identifies **Modified by PandaKB / 由 PandaKB 修改** and retains upstream attribution and GPL information.
- 12 selectable interface languages, English by default, with offline resources and a saved preference.
- Close and reopen Vial to apply the selected language; the application does not automatically close your current work.
- Initial translations cover menus, main tabs and common controls. Chinese (Simplified/Traditional) and Japanese also cover additional editor and QMK settings.
- **Translations are incomplete.** Advanced keycode tooltips, effect names and some diagnostics fall back to English. See the attached exact coverage report.
- The build runs upstream simulated-device regressions, language tests, packaging checks and the frozen EXE in all 12 languages. Real-keyboard and clean Windows 10/11 acceptance tests remain outstanding.

Download the Windows x64 ZIP, extract the complete folder and run **Vial/Vial.exe**. No Python or Qt installation is required.
Keep all files together. Save pending macro/settings edits before closing.
SHA256SUMS.txt identifies the ZIP checksum. Source and upstream history are available at the release tag.
