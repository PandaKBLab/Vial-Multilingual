# SPDX-License-Identifier: GPL-2.0-or-later
"""Run upstream's simulated-device suite on the same Windows runtime as the ZIP."""
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, os.path.abspath("src/main/python"))
# Upstream GUI tests import the Linux backend by name. On Windows they must
# patch the backend actually used by hidproxy, with the same simulated device.
if sys.platform == "win32":
    from hidproxy import hid
    sys.modules["hidraw"] = hid

import pytest
sys.exit(pytest.main(["-q", "src/main/python/test", "tests", "--junitxml=build/tests.xml"]))
