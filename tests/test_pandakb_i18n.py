# SPDX-License-Identifier: GPL-2.0-or-later
import os
import pytest
from PyQt5.QtCore import QCoreApplication, QSettings
from PyQt5.QtWidgets import QMessageBox
from pandakb_i18n import LanguageManager, LANGUAGES


class Context:
    def get_resource(self, path):
        return os.path.abspath(os.path.join("src/main/resources/base", path))


@pytest.mark.parametrize("language", [code for code, _ in LANGUAGES])
def test_language_load_fallback_and_format(qapp, tmp_path, language):
    settings = QSettings(str(tmp_path / "language.ini"), QSettings.IniFormat)
    settings.setValue("language", language)
    manager = LanguageManager(Context(), settings)
    try:
        assert manager.language == language
        text = QCoreApplication.translate("MainWindow", "Refresh")
        assert text == "Refresh" if language == "en" else text != "Refresh"
        # An unknown message must preserve the English source.
        assert QCoreApplication.translate("Missing", "Unknown UI string") == "Unknown UI string"
        template = QCoreApplication.translate("MacroRecorder", "Memory used by macros: {}/{}")
        assert "12" in template.format(12, 512)
        assert "PandaKB" in QCoreApplication.translate("PandaKB", "Modified by PandaKB")
    finally:
        manager.unload()


def test_default_english_and_invalid_language(qapp, tmp_path):
    settings = QSettings(str(tmp_path / "new.ini"), QSettings.IniFormat)
    manager = LanguageManager(Context(), settings)
    assert manager.language == "en"
    settings.setValue("language", "not-a-language")
    assert LanguageManager(Context(), settings).language == "en"


def test_selection_persists_without_rebuilding_or_retranslating(qapp, tmp_path, monkeypatch):
    settings = QSettings(str(tmp_path / "remember.ini"), QSettings.IniFormat)
    manager = LanguageManager(Context(), settings)
    messages = []
    monkeypatch.setattr(QMessageBox, "information", lambda *args: messages.append(args))
    manager.select("zh_CN")
    assert manager.language == "en"
    assert manager.pending_language == "zh_CN"
    assert QCoreApplication.translate("MainWindow", "Refresh") == "Refresh"
    assert len(messages) == 1
    reopened_settings = QSettings(str(tmp_path / "remember.ini"), QSettings.IniFormat)
    reopened = LanguageManager(Context(), reopened_settings)
    try:
        assert reopened.language == "zh_CN"
        assert QCoreApplication.translate("MainWindow", "Refresh") == "刷新"
    finally:
        reopened.unload()


def test_missing_catalog_falls_back_to_english(qapp, tmp_path):
    class Missing:
        def get_resource(self, path):
            return str(tmp_path / path)
    settings = QSettings(str(tmp_path / "missing.ini"), QSettings.IniFormat)
    settings.setValue("language", "ja")
    manager = LanguageManager(Missing(), settings)
    assert manager.language == "en"


def test_about_keeps_upstream_and_pandakb_attribution(qtbot, monkeypatch):
    from test.test_gui import prepare, FAKE_KEYBOARD
    window, _ = prepare(qtbot, FAKE_KEYBOARD)
    captured = []
    monkeypatch.setattr(QMessageBox, "about", lambda *args: captured.append(args))
    window.about_vial()
    title, body = captured[0][1:]
    assert "PandaKB" in title
    assert "Modified by PandaKB" in body
    assert "get.vial.today" in body
    assert "GNU General Public License" in body
