# SPDX-License-Identifier: GPL-2.0-or-later
import ast
import hashlib
import os
import pathlib
import shutil
import zipfile

root = pathlib.Path(__file__).resolve().parents[1]
bundle = root / "target/Vial"
assert (bundle / "Vial.exe").is_file()
languages = ("en", "zh_CN", "zh_TW", "ja", "de", "fr", "es", "pt_BR", "ko", "it", "ru", "pl")
for language in languages:
    assert list(bundle.rglob("vial_{}.qm".format(language))), language
assert list(bundle.rglob("qwindows.dll")), "Qt platform plugin missing"
assert list(bundle.rglob("hid*.pyd")), "HID backend missing"
for filename in ("COPYING", "NOTICE", "README.md"):
    shutil.copy2(str(root / filename), str(bundle / filename))
shutil.copy2(str(root / "build/translation-coverage.md"), str(bundle / "translation-coverage.md"))
version = next(ast.literal_eval(n.value) for n in ast.parse((root / "src/main/python/pandakb_i18n.py").read_text(encoding="utf-8")).body
               if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PANDAKB_VERSION" for t in n.targets))
commit = os.environ.get("GITHUB_SHA", "development")
(bundle / "BUILD-INFO.txt").write_text(
    "PandaKB Vial Multilingual {}\nCommit: {}\nSource: https://github.com/PandaKBLab/Vial-Multilingual/tree/{}\n"
    "Upstream: aef8222a2d0429a183b2ed692d5f9efcfd383f08\n"
    "12 languages; complete built-in UI catalogs. Language changes offer a guarded automatic restart.\n"
    "Unsigned build: Windows SmartScreen may warn. Hardware acceptance testing is not included.\n".format(version, commit, commit),
    encoding="utf-8")
dist = root / "dist"
dist.mkdir(exist_ok=True)
base = "PandaKB-Vial-v{}-Windows-x64-portable".format(version)
archive = pathlib.Path(shutil.make_archive(str(dist / base), "zip", str(root / "target"), "Vial"))
checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
(dist / "SHA256SUMS.txt").write_text("{}  {}\n".format(checksum, archive.name), encoding="utf-8")
with zipfile.ZipFile(str(archive)) as zipped:
    assert "Vial/Vial.exe" in zipped.namelist()
    for language in languages:
        assert any(path.endswith("vial_{}.qm".format(language)) for path in zipped.namelist())
print(archive)
