# Translation maintenance

Each locale JSON maps an exact English source string to its translation.
Keep QMK identifiers, placeholders (including format specifications), HTML tags, URLs and file extensions unchanged.
Context-specific Qt TS files and binary QM files are generated in CI and included in the translations artifact.

English is the source and fallback language. A missing entry remains unfinished in TS and is omitted from QM.
Do not fill missing entries with English merely to improve coverage.
Established technical names (for example Tap Dance) may intentionally be retained.
The current dictionaries are initial translations and require native-speaker review.

The inventory includes literal tr() calls, main editor tabs, keycode category names, QMK option labels, RGB effect labels and static keycode tooltips.
It does not yet account for every formatted tooltip, firmware-provided label, platform dialog or diagnostic string.
The report explicitly states this limitation; full UI review remains required.

The initial gate requires every locale to contain all sources in core.json.
Stable release tags additionally run --strict against the full extracted inventory.
