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
    # Tests create several MainWindows in one process; upstream's Windows
    # notifier registers a single fixed window class and cannot be repeated.
    # Simulated device reads/writes still go through the normal update path.
    # The actual notifier is exercised separately by each frozen EXE process.
    from autorefresh.autorefresh_thread_win import AutorefreshThreadWin
    AutorefreshThreadWin.run = lambda self: None

import pytest
sys.exit(pytest.main(["-vv", "--durations=15", "-o", "faulthandler_timeout=60", "src/main/python/test", "tests", "--junitxml=build/tests.xml"]))
