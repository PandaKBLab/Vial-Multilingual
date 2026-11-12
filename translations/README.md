# Translation catalogs

The 11 JSON catalogs plus the English source cover all 12 supported languages. Keys are exact English source messages. Contexts are extracted from Python and QMK setting definitions; generated layer/tooltips are translated before parameters are inserted.

Run `python scripts/build_translations.py --strict` with Qt `lrelease` installed. Missing entries, empty values, changed format arguments or changed HTML tags fail validation. Runtime tests compare every compiled catalog entry with its JSON value.

Standard keycap legends and QMK codes remain stable so users can match documentation and firmware. Device-supplied custom names and raw exception diagnostics are outside the built-in catalog. A retained technical term is explicitly recorded in the JSON and still counts as present.

Use natural terminology while preserving modifiers, keycode identifiers, numbers and units. Keep advanced option labels concise; the interface supports word wrapping and scrolling.
