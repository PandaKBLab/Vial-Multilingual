# Preview validation — 2026-11-12

Published version: [v0.1.0-preview.1](https://github.com/PandaKBLab/Vial-Multilingual/releases/tag/v0.1.0-preview.1).

Application source: `f7941d1b348bb51bdbadb9ad5bcae89605088812`.

- [Pinned original upstream build](https://github.com/PandaKBLab/Vial-Multilingual/actions/runs/43184415105): successful.
- [PandaKB Windows build](https://github.com/PandaKBLab/Vial-Multilingual/actions/runs/43186272816): successful; 44 tests passed.
- Real frozen Vial.exe launched in all 12 languages using the native Windows Qt platform; startup text, About attribution, screenshots and exit status checked.
- ZIP structure, all application language resources, Qt Windows plugin and HID backend checked.
- [Preview publication](https://github.com/PandaKBLab/Vial-Multilingual/actions/runs/43187189844): verified and reused the exact tested ZIP; only the download filename and checksum sidecar line endings were normalized.
- ZIP SHA-256: `83a376556b7bf8b1d0d94eae1e43c45d309a478b4971388b202239c1e9ce2124`.

## Translation status

655 context/source entries are in the extracted inventory.

| Languages | Completed entries | Extracted coverage |
|---|---:|---:|
| English source | 655 | 100% |
| Simplified Chinese, Traditional Chinese, Japanese | 252 each | 38.5% each |
| German, French, Spanish, Brazilian Portuguese, Korean, Italian, Russian, Polish | 99 each | 15.1% each |

These figures cover the extracted inventory, not every visible upstream string.
Most remaining entries are advanced keycode descriptions, lighting effects and detailed settings.
Menus, main tabs and common controls have initial translations in all 12 languages.
Terminology still needs native-speaker review.

## Testing scope and outstanding checks

The GUI regression suite uses a simulated keyboard. Windows-specific test adapters isolate the OS notification source and use Qt 5.9-compatible mouse constants; protocol and UI assertions remain active.
The packaged EXE checks use the real Windows notifier in separate processes and do not access physical keyboards.
The Qt offscreen plugin crashed when opening About in a frozen build; native Windows platform checks pass. Offscreen execution is not a supported user mode.

Not yet verified: physical keyboard reads/writes, real macro/RGB/Tap Dance/Combo operation, clean Windows 10/11 installations and every language at every display scaling.
Language selection is persisted and applied on the next launch.
No production-readiness or complete translation claim is made for this preview.
