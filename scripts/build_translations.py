# SPDX-License-Identifier: GPL-2.0-or-later
"""Extract UI inventory, validate translations, produce Qt TS/QM and honest coverage."""
import ast
import collections
import json
import pathlib
import re
import shutil
import string
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src/main/python"
LANGUAGES = ("en", "zh_CN", "zh_TW", "ja", "de", "fr", "es", "pt_BR", "ko", "it", "ru", "pl")
inventory = collections.defaultdict(set)


def literal(node):
    return node.s if isinstance(node, ast.Str) else None


def add(context, source):
    if source and source.strip():
        inventory[context].add(source)


def strings(node):
    return [n.s for n in ast.walk(node) if isinstance(n, ast.Str)]


def extract():
    for path in sorted(SRC.rglob("*.py")):
        if "test" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                name = n.func.id if isinstance(n.func, ast.Name) else ""
                if name == "tr" and len(n.args) >= 2:
                    context, source = literal(n.args[0]), literal(n.args[1])
                    if context and source:
                        add(context, source)
                if path.name == "rgb_configurator.py" and name in ("QmkRgblightEffect", "VialRGBEffect"):
                    add("RGBEffects", literal(n.args[1]))
                if path.name == "keycodes.py" and name in ("K", "Keycode"):
                    if len(n.args) >= 3:
                        add("KeycodeTooltip", literal(n.args[2]))
                    for kw in n.keywords:
                        if kw.arg == "tooltip":
                            add("KeycodeTooltip", literal(kw.value))
                if path.name == "keycodes.py" and name == "generate_keycodes_for_mask":
                    add("KeycodeTooltip", literal(n.args[1]))
                if path.name == "tabbed_keycodes.py" and name in ("Tab", "SimpleTab"):
                    add("TabbedKeycodes", literal(n.args[1]))
            if isinstance(n, ast.Assign):
                if path.name == "main_window.py" and any(isinstance(t, ast.Attribute) and t.attr == "editors" for t in n.targets):
                    for value in strings(n.value):
                        add("MainWindow", value)
    keymaps = ast.parse((SRC / "keymaps.py").read_text(encoding="utf-8"))
    for node in ast.walk(keymaps):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "KEYMAPS" for t in node.targets):
            for entry in node.value.elts:
                add("KeyboardLayout", literal(entry.elts[0]))
    for value in ("Text", "Down", "Up", "Tap", "Delay (ms)"):
        add("MacroLine", value)
    for value in ("System", "Dark", "Light"):
        add("MenuTheme", value)
    data = json.loads((ROOT / "src/main/resources/base/qmk_settings.json").read_text(encoding="utf-8"))
    for tab in data["tabs"]:
        add("QmkSettings", tab["name"])
        for field in tab["fields"]:
            add("QmkSettings", field["title"])


def placeholders(text):
    return [(name, spec, conv) for _, name, spec, conv in string.Formatter().parse(text) if name is not None]


def main():
    extract()
    destination = ROOT / "src/main/resources/base/translations"
    destination.mkdir(parents=True, exist_ok=True)
    report = {}
    all_sources = set().union(*inventory.values())
    core = json.loads((ROOT / "translations/core.json").read_text(encoding="utf-8"))
    assert set(core) <= all_sources, "Core strings must be part of the actual UI inventory"
    for language in LANGUAGES:
        mapping = {} if language == "en" else json.loads((ROOT / "translations/{}.json".format(language)).read_text(encoding="utf-8"))
        if language != "en":
            missing_core = set(core) - set(mapping)
            assert not missing_core, (language, sorted(missing_core))
        for source, target in mapping.items():
            assert target.strip(), (language, source, "empty translation")
            assert placeholders(source) == placeholders(target), (language, source, "format placeholders changed")
            assert re.findall(r"</?[^>]+>", source) == re.findall(r"</?[^>]+>", target), (language, source, "HTML tags changed")
        root = ET.Element("TS", version="2.1", language=language, sourcelanguage="en")
        totals = {}
        for context, sources in sorted(inventory.items()):
            el = ET.SubElement(root, "context")
            ET.SubElement(el, "name").text = context
            translated = 0
            for source in sorted(sources):
                msg = ET.SubElement(el, "message")
                ET.SubElement(msg, "source").text = source
                target = source if language == "en" else mapping.get(source)
                translation = ET.SubElement(msg, "translation")
                if target is None:
                    translation.set("type", "unfinished")
                else:
                    translation.text = target
                    translated += 1
            totals[context] = {"translated": translated, "total": len(sources)}
        ts = destination / "vial_{}.ts".format(language)
        ET.ElementTree(root).write(str(ts), encoding="utf-8", xml_declaration=True)
        subprocess.check_call(["lrelease", "-nounfinished", str(ts), "-qm", str(ts.with_suffix(".qm"))])
        report[language] = {
            "contexts": totals,
            "translated": sum(v["translated"] for v in totals.values()),
            "total": sum(v["total"] for v in totals.values()),
            "missing": sorted(all_sources - set(mapping)) if language != "en" else [],
        }
    out = ROOT / "build"
    out.mkdir(exist_ok=True)
    (out / "translation-inventory.json").write_text(json.dumps({k: sorted(v) for k, v in inventory.items()}, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "translation-coverage.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Translation coverage", "", "Counts cover built-in interface text, settings, effect names, diagnostics and keycode descriptions.",
             "Firmware-supplied custom names, standard keycap legends, QMK identifiers and raw exception details remain as supplied.",
             "An explicitly retained technical term counts as translated; missing entries fall back to English.",
             "", "| Language | Translated | Extracted | Coverage |", "|---|---:|---:|---:|"]
    for language, data in report.items():
        lines.append("| {} | {} | {} | {:.1f}% |".format(language, data["translated"], data["total"], 100 * data["translated"] / data["total"]))
    (out / "translation-coverage.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    if "--strict" in sys.argv:
        assert all(not v["missing"] for v in report.values()), "Stable release blocked: translations are incomplete"


if __name__ == "__main__":
    main()
