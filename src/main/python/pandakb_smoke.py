# SPDX-License-Identifier: GPL-2.0-or-later
"""Opt-in CI smoke test for the frozen portable application."""
import faulthandler
import json
import os
import traceback
from PyQt5.QtCore import QSettings, QTimer, QCoreApplication
from PyQt5.QtWidgets import QMessageBox, QLabel, QAbstractButton, QScrollArea, QComboBox
from pandakb_i18n import LanguageManager


def run(appctx, language, directory):
    from hidproxy import hid
    hid.enumerate = lambda: []
    os.makedirs(directory, exist_ok=True)
    crash_log = open(os.path.join(directory, "native-crash.log"), "w")
    faulthandler.enable(file=crash_log)
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
            errors.append(traceback.format_exc())
        finally:
            for dialog in dialogs:
                dialog.accept()

    def capture():
        try:
            assert manager.language == language
            result["language"] = manager.language
            standard = QMessageBox(QMessageBox.Question, "", "", QMessageBox.Yes | QMessageBox.No)
            result["standard_yes"] = standard.button(QMessageBox.Yes).text()
            if language != "en":
                assert result["standard_yes"].replace("&", "") != "Yes", "Qt standard buttons not translated"
            standard.deleteLater()
            result["refresh"] = window.btn_refresh_devices.text()
            assert result["refresh"] == QCoreApplication.translate("MainWindow", "Refresh")
            if language != "en":
                assert result["refresh"] != "Refresh"
            assert window.grab().save(os.path.join(directory, "main-{}.png".format(language)))
            QTimer.singleShot(400, capture_about)
            window.about_vial()
            from pandakb_preview import prepare
            from keycodes.keycodes import Keycode
            prepare(window)
            window.resize(1180, 820)
            app.processEvents()
            result["window_size"] = [window.width(), window.height()]
            assert window.width() <= 1280 and window.height() <= 900, result["window_size"]
            result["pages"] = []
            result["layout_issues"] = []
            for index in range(window.tabs.count()):
                window.tabs.setCurrentIndex(index)
                app.processEvents()
                page = window.tabs.widget(index)
                assert page.isVisible(), "Editor page is hidden"
                assert not window.lbl_no_devices.isVisible(), "No-device page covers the editor"
                name = window.editors[[e[0] for e in window.editors].index(page.editor)][1]
                result["pages"].append(name)
                assert window.grab().save(os.path.join(directory, "page-{}-{}.png".format(language, index)))
                # Scroll containers intentionally allow content larger than the viewport.
                for label in page.findChildren(QLabel):
                    if not label.isVisible() or not label.text() or label.wordWrap():
                        continue
                    # Keycap legends use fixed squares by design; audit explanatory labels.
                    if label.parent() and label.parent().__class__.__name__ in ("SquareButton", "KeyWidget"):
                        continue
                    if label.sizeHint().width() > label.width() + 4:
                        result["layout_issues"].append({"page": name, "text": label.text(), "width": label.width(), "needed": label.sizeHint().width()})
            window.tabs.setCurrentIndex(0)
            app.processEvents()
            assert "LT3" in Keycode.tooltip("LT3(KC_A)")
            result["sample_tooltip"] = Keycode.tooltip("LT3(KC_A)")
            result["settings_tabs"] = window.qmk_settings.tabs_widget.count()
            result["rgb_effects"] = window.rgb_configurator.handler_vialrgb.rgb_effect.count()
            assert result["settings_tabs"] == 7
            assert result["rgb_effects"] > 40
            # Capture every advanced-settings subtab too.
            settings_index = next(i for i in range(window.tabs.count()) if window.tabs.widget(i).editor is window.qmk_settings)
            window.tabs.setCurrentIndex(settings_index)
            for index in range(window.qmk_settings.tabs_widget.count()):
                window.qmk_settings.tabs_widget.setCurrentIndex(index)
                app.processEvents()
                assert window.grab().save(os.path.join(directory, "settings-{}-{}.png".format(language, index)))
            assert not result["layout_issues"], result["layout_issues"]
        except Exception as error:
            errors.append(traceback.format_exc())
        finally:
            result["errors"] = errors
            with open(os.path.join(directory, "smoke-{}.json".format(language)), "w", encoding="utf-8") as out:
                json.dump(result, out, ensure_ascii=False, indent=2)
            app.exit(1 if errors else 0)

    QTimer.singleShot(600, capture)
    return app.exec_()
