# SPDX-License-Identifier: GPL-2.0-or-later
"""Verify all platform reports and expected packaging inputs before publication."""
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

version = sys.argv[1]
languages = ("en", "zh_CN", "zh_TW", "ja", "de", "fr", "es", "pt_BR", "ko", "it", "ru", "pl")
report = Path("validation")
coverage = json.loads((report / "translation-coverage.json").read_text())
assert set(coverage) == set(languages)
for data in coverage.values():
    assert data["translated"] == data["total"] and not data["missing"]
for folder in (report, report / "Linux-x86_64", report / "macOS-arm64", report / "macOS-x86_64"):
    tests = list(ET.parse(folder / "tests.xml").getroot().iter("testsuite"))
    passed = sum(int(suite.get("tests", 0)) - int(suite.get("skipped", 0)) for suite in tests)
    assert passed >= 67, (folder, passed)
    assert all(not int(suite.get("failures", 0)) and not int(suite.get("errors", 0)) for suite in tests)
    for code in languages:
        result = json.loads((folder / "smoke" / code / f"smoke-{code}.json").read_text())
        assert result["language"] == code and not result["errors"] and not result["layout_issues"], (folder, code)
        assert len(result["pages"]) == 11 and result["settings_tabs"] == 7, (folder, code)
installed = json.loads((report / "installed-smoke/smoke-en.json").read_text())
assert installed["language"] == "en" and not installed["errors"]
print(f"{version}: verified catalog coverage, unit tests and 49 packaged launches")
