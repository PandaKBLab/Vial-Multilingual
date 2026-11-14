# SPDX-License-Identifier: GPL-2.0-or-later
"""Launch the packaged app in each interface language and check its report."""
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    command = sys.argv[1:]
    if not command:
        raise SystemExit("Usage: smoke_unix.py executable [options]")
    for language in ("en", "zh_CN", "zh_TW", "ja", "de", "fr", "es", "pt_BR", "ko", "it", "ru", "pl"):
        output = Path("build/smoke") / language
        output.mkdir(parents=True, exist_ok=True)
        print("Opening the package in " + language, flush=True)
        subprocess.run(
            command + ["--pandakb-smoke-test", language, str(output.resolve())],
            env={**os.environ, "LC_ALL": "en_US.UTF-8"}, check=True, timeout=90,
        )
        report = json.loads((output / ("smoke-" + language + ".json")).read_text(encoding="utf-8"))
        assert report["language"] == language and not report["errors"], report
        assert len(report["pages"]) == 11 and report["settings_tabs"] == 7, report


if __name__ == "__main__":
    main()
