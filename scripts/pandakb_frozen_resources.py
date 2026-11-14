# SPDX-License-Identifier: GPL-2.0-or-later
"""Provide the fbs resource interface in the PyInstaller 6 Unix builds."""
import json
import sys
from pathlib import Path

from fbs_runtime import _frozen

root = Path(sys._MEIPASS)
_frozen.BUILD_SETTINGS = json.loads((root / "base.json").read_text(encoding="utf-8"))
_frozen.get_resource_dirs = lambda: [str(root)]
