# SPDX-License-Identifier: GPL-2.0-or-later
"""PandaKB interface language support. Device state is never touched here."""
import logging
import os
import sys

from PyQt5.QtCore import QObject, QCoreApplication, QSettings, QTranslator, QProcess
from PyQt5.QtWidgets import QApplication, QActionGroup, QMessageBox

tr = QCoreApplication.translate
PANDAKB_VERSION = "0.1.0"
LANGUAGES = (
    ("en", "English"), ("zh_CN", "简体中文"), ("zh_TW", "繁體中文"),
    ("ja", "日本語"), ("de", "Deutsch"), ("fr", "Français"),
    ("es", "Español"), ("pt_BR", "Português (Brasil)"), ("ko", "한국어"),
    ("it", "Italiano"), ("ru", "Русский"), ("pl", "Polski"),
)


class LanguageManager(QObject):
    def __init__(self, appctx, settings=None, parent=None):
        super().__init__(parent)
        self.settings = settings if settings is not None else QSettings("PandaKB", "Vial-Multilingual")
        self.translators = []
        self.language = "en"
        requested = self.settings.value("language", "en")
        supported = dict(LANGUAGES)
        if requested not in supported:
            requested = "en"
        if requested != "en":
            translator = QTranslator(self)
            try:
                path = appctx.get_resource("translations/vial_{}.qm".format(requested))
            except FileNotFoundError:
                path = ""

            if translator.load(path):
                qt = QTranslator(self)
                qt_path = os.path.join(os.path.dirname(path), "qtbase_{}.qm".format(requested))
                if qt.load(qt_path):
                    QApplication.instance().installTranslator(qt)
                    self.translators.append(qt)
                QApplication.instance().installTranslator(translator)
                self.translators.append(translator)
                self.language = requested
            else:
                logging.warning("Could not load interface language %s; using English", requested)
        self.pending_language = self.language

    def add_menu(self, menu_bar):
        settings_menu = menu_bar.addMenu(tr("PandaKB", "Settings"))
        # Native language names and the bilingual entry remain discoverable.
        language_menu = settings_menu.addMenu("Language / 语言")
        group = QActionGroup(language_menu)
        group.setExclusive(True)
        for code, name in LANGUAGES:
            action = language_menu.addAction(name)
            action.setData(code)
            action.setCheckable(True)
            action.setChecked(code == self.pending_language)
            group.addAction(action)
            action.triggered.connect(lambda checked, value=code: self.select(value, menu_bar.window()))
        self.action_group = group

    def select(self, code, parent=None):
        if code not in dict(LANGUAGES):
            raise ValueError("Unsupported interface language")
        old = self.pending_language
        self.settings.setValue("language", code)
        self.settings.sync()
        if self.settings.status() != QSettings.NoError:
            self.settings.setValue("language", old)
            self._check_action(old)
            QMessageBox.warning(parent, tr("PandaKB", "Interface language"),
                                tr("PandaKB", "Could not save the language setting. The application will stay open."))
            return
        self.pending_language = code
        self._check_action(code)
        if code == self.language:
            return
        if restart_blocked(parent):
            QMessageBox.information(parent, tr("PandaKB", "Interface language"),
                tr("PandaKB", "Language saved. Save or revert pending edits and finish the current operation before restarting. Select the language again when ready."))
            return
        if QMessageBox.question(parent, tr("PandaKB", "Interface language"),
                tr("PandaKB", "Restart Vial now to apply the selected language?"),
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) == QMessageBox.Yes:
            if not self.restart(parent):
                QMessageBox.warning(parent, tr("PandaKB", "Interface language"),
                    tr("PandaKB", "Automatic restart failed. Your work remains open. Close and reopen Vial manually to apply the language."))

    def _check_action(self, code):
        group = getattr(self, "action_group", None)
        if group:
            for action in group.actions():
                action.setChecked(action.data() == code)

    def restart(self, parent):
        if restart_blocked(parent):
            return False
        program, arguments = restart_command()
        started = QProcess.startDetached(program, arguments, os.getcwd())
        if isinstance(started, tuple):
            started = started[0]
        if not started:
            return False
        if parent is not None:
            parent.close()
        QApplication.instance().quit()
        return True

    def unload(self):
        for translator in reversed(self.translators):
            QApplication.instance().removeTranslator(translator)
        self.translators = []


def get_language_manager(appctx):
    app = QApplication.instance()
    manager = getattr(app, "_pandakb_language_manager", None)
    if manager is None:
        manager = LanguageManager(appctx, parent=app)
        app._pandakb_language_manager = manager
    return manager

def restart_command():
    # The child waits for this process to exit before opening the keyboard.
    arguments = [] if getattr(sys, "frozen", False) else [os.path.abspath(sys.argv[0])]
    arguments.append("--pandakb-wait-for-exit={}".format(os.getpid()))
    return sys.executable, arguments


def restart_blocked(window):
    if window is None:
        return False
    if getattr(window, "ui_lock_count", 0):
        return True
    for editor, _ in getattr(window, "editors", []):
        if not editor.valid():
            continue
        # Comparing bytes also detects a macro too large to enable its Save button.
        if hasattr(editor, "macro_tabs"):
            if any(not tab.btn_record_stop.isHidden() for tab in editor.macro_tabs):
                return True
            if editor.serialize() != editor.keyboard.macro:
                return True
        elif hasattr(editor, "btn_save") and editor.btn_save.isEnabled():
            return True
    return False


def wait_for_previous_process(pid):
    if pid <= 0 or pid == os.getpid():
        return False
    if sys.platform == "win32":
        import ctypes
        kernel = ctypes.windll.kernel32
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = kernel.OpenProcess(0x00100000, False, pid)
        if handle:
            try:
                return kernel.WaitForSingleObject(handle, 15000) == 0
            finally:
                kernel.CloseHandle(handle)
        return True
    import time
    for _ in range(150):
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        except PermissionError:
            return False
        time.sleep(0.1)
    return False
