# SPDX-License-Identifier: GPL-2.0-or-later
"""PandaKB interface language support. Device state is never touched here."""
import logging
import os

from PyQt5.QtCore import QObject, QCoreApplication, QSettings, QTranslator
from PyQt5.QtWidgets import QApplication, QActionGroup, QMessageBox

tr = QCoreApplication.translate
PANDAKB_VERSION = "0.1.0-preview.1"
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
            action.setCheckable(True)
            action.setChecked(code == self.pending_language)
            group.addAction(action)
            action.triggered.connect(lambda checked, value=code: self.select(value, menu_bar.window()))
        self.action_group = group

    def select(self, code, parent=None):
        if code not in dict(LANGUAGES):
            raise ValueError("Unsupported interface language")
        self.settings.setValue("language", code)
        self.settings.sync()
        self.pending_language = code
        if code != self.language:
            QMessageBox.information(
                parent, tr("PandaKB", "Interface language"),
                tr("PandaKB", "Language saved. Close and reopen Vial when you are ready. Your current work stays open."))

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
