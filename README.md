# PandaKB Vial Multilingual

A Windows portable edition of [Vial](https://get.vial.today/) with 12 interface languages, maintained and modified by **PandaKB**.

[Download v0.1.0](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0) · [Source](https://github.com/PandaKBLab/Vial-Multilingual) · [Build checks](https://github.com/PandaKBLab/Vial-Multilingual/actions/workflows/build.yml)

## 使用方法

1. 从上方版本页面下载 Windows x64 ZIP，完整解压后打开文件夹中的 `Vial.exe`。不要只复制 EXE。
2. 在 **Settings → Language / 语言** 中选择语言。默认英语，选择会记住。
3. 选择后可确认立即自动重启。未保存的宏或设置、录制或固件更新期间会保留窗口；先保存或撤销编辑，完成操作后再次选择语言即可重启。

包含英语、简体中文、繁体中文、日语、德语、法语、西班牙语、巴西葡萄牙语、韩语、意大利语、俄语、波兰语。内置菜单、高级设置、键码悬停说明、灯效和常规状态提示都有对应翻译。QMK 标识符、标准键帽文字、设备自行提供的名称及原始异常信息保留原值。

**关于 Vial** 保留原作者与 GPL 信息，并显示 **Modified by PandaKB**。

## Windows 首次打开提示

本版未进行商业代码签名，因此 Windows 可能显示“发布者未知”或 SmartScreen 提示。请仅从本仓库版本页面下载，并核对同页的 SHA256 校验值。确认来源后，可以在提示的“更多信息”中选择“仍要运行”；无需关闭系统防护。企业管理策略可能不允许继续。

有效签名可以显示经过验证的发布者，但不能保证新版本立即不再提示。详情见 [Microsoft SmartScreen 说明](https://learn.microsoft.com/windows/apps/package-and-deploy/smartscreen-reputation)。

## Validation and scope

GitHub Actions requires complete extracted translation catalogs, checks format placeholders and HTML, runs the upstream regression tests plus language/restart tests, and opens the packaged Windows EXE in all 12 languages. The synthetic keyboard checks cover main editors, all advanced-settings tabs, lighting effects and About. Reports and screenshots are retained as build artifacts.

Hardware communication tests use simulated devices. Physical keyboard flashing, unlock sequences and manufacturer-specific firmware names require testing with the actual keyboard.

## Development and license

Upstream source: `vial-kb/vial-gui`, pinned at `aef8222a2d0429a183b2ed692d5f9efcfd383f08`. The compatible upstream Python 3.6 / Qt 5.9 build stack is retained for this release. Source edits, translation compilation and Windows packaging are performed in GitHub.

Translations: `translations/*.json`; extraction and validation: `scripts/build_translations.py --strict`. Missing translations block a release. Contributions correcting terminology are welcome.

Original copyright remains with the Vial contributors. Modifications by PandaKB. See [COPYING](COPYING) and [NOTICE](NOTICE) for GPL-2.0-or-later and attribution.
