# SPDX-License-Identifier: GPL-2.0-or-later
"""Opt-in CI smoke test for the frozen portable application."""
import json
import os
from PyQt5.QtCore import QSettings, QTimer, QCoreApplication
from PyQt5.QtWidgets import QMessageBox
from pandakb_i18n import LanguageManager


def run(appctx, language, directory):
    from hidproxy import hid
    hid.enumerate = lambda: []
    os.makedirs(directory, exist_ok=True)
    app = appctx.app
    settings = QSettings(os.path.join(directory, "smoke.ini"), QSettings.IniFormat)
    settings.setValue("language", language)
    manager = LanguageManager(appctx, settings, app)
    app._pandakb_language_manager = manager
    from main_window import MainWindow
    window = MainWindow(appctx)
    window.show()
    errors = []
    result = {}

    def capture_about():
        dialogs = [w for w in app.topLevelWidgets() if isinstance(w, QMessageBox) and w.isVisible()]
        try:
            assert dialogs, "About dialog did not open"
            dialog = dialogs[0]
            assert "Modified by PandaKB" in dialog.text()
            assert "GNU General Public License" in dialog.text()
            assert dialog.grab().save(os.path.join(directory, "about-{}.png".format(language)))
        except Exception as error:
            errors.append(str(error))
        finally:
            for dialog in dialogs:
                dialog.accept()

    def capture():
        try:
            assert manager.language == language
            result["language"] = manager.language
            result["refresh"] = window.btn_refresh_devices.text()
            assert result["refresh"] == QCoreApplication.translate("MainWindow", "Refresh")
            if language != "en":
                assert result["refresh"] != "Refresh"
            assert window.grab().save(os.path.join(directory, "main-{}.png".format(language)))
            QTimer.singleShot(400, capture_about)
            window.about_vial()
        except Exception as error:
            errors.append(str(error))
        finally:
            result["errors"] = errors
            with open(os.path.join(directory, "smoke-{}.json".format(language)), "w", encoding="utf-8") as out:
                json.dump(result, out, ensure_ascii=False, indent=2)
            app.exit(1 if errors else 0)

    QTimer.singleShot(600, capture)
    return app.exec_()
