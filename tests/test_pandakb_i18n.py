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
    monkeypatch.setattr(QMessageBox, "question", lambda *args: (messages.append(args), QMessageBox.No)[1])
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

def test_fbs_missing_resource_exception_falls_back(qapp, tmp_path):
    class Missing:
        def get_resource(self, path):
            raise FileNotFoundError(path)
    settings = QSettings(str(tmp_path / "missing-fbs.ini"), QSettings.IniFormat)
    settings.setValue("language", "zh_CN")
    assert LanguageManager(Missing(), settings).language == "en"

def test_translated_category_survives_rebuild(qapp, qtbot, tmp_path):
    from tabbed_keycodes import FilteredTabbedKeycodes
    from util import KeycodeDisplay
    settings = QSettings(str(tmp_path / "category.ini"), QSettings.IniFormat)
    settings.setValue("language", "zh_CN")
    manager = LanguageManager(Context(), settings)
    tabs = FilteredTabbedKeycodes()
    qtbot.addWidget(tabs)
    try:
        tabs.setCurrentIndex(2)
        current = tabs.currentWidget()
        tabs.recreate_keycode_buttons()
        assert tabs.currentWidget() is current
    finally:
        KeycodeDisplay.unregister_keymap_override(tabs)
        manager.unload()

@pytest.mark.parametrize("frozen", [False, True])
def test_restart_command_supports_source_and_portable(monkeypatch, frozen):
    import sys
    import pandakb_i18n as i18n
    monkeypatch.setattr(sys, "frozen", frozen, raising=False)
    monkeypatch.setattr(sys, "argv", ["folder with spaces/main.py"])
    program, arguments = i18n.restart_command()
    assert program == sys.executable
    assert arguments[-1] == "--pandakb-wait-for-exit={}".format(os.getpid())
    assert len(arguments) == (1 if frozen else 2)
    if not frozen:
        assert arguments[0] == os.path.abspath(sys.argv[0])


def test_restart_failure_leaves_window_open(qapp, tmp_path, monkeypatch):
    import pandakb_i18n as i18n
    manager = LanguageManager(Context(), QSettings(str(tmp_path / "restart.ini"), QSettings.IniFormat))
    monkeypatch.setattr(i18n.QProcess, "startDetached", lambda *args: (False, 0))
    assert manager.restart(None) is False


def test_restart_checks_pending_macro_even_when_save_disabled():
    from types import SimpleNamespace
    from pandakb_i18n import restart_blocked
    editor = SimpleNamespace(valid=lambda: True, macro_tabs=[],
                             serialize=lambda: b"edited", keyboard=SimpleNamespace(macro=b"saved"))
    window = SimpleNamespace(ui_lock_count=0, editors=[(editor, "Macros")])
    assert restart_blocked(window)
    editor.serialize = lambda: b"saved"
    assert not restart_blocked(window)
    window.ui_lock_count = 1
    assert restart_blocked(window)


def test_restart_checks_recording_and_pending_settings():
    from types import SimpleNamespace
    from pandakb_i18n import restart_blocked
    tab = SimpleNamespace(btn_record_stop=SimpleNamespace(isHidden=lambda: False))
    macro = SimpleNamespace(valid=lambda: True, macro_tabs=[tab],
                            serialize=lambda: b"saved", keyboard=SimpleNamespace(macro=b"saved"))
    assert restart_blocked(SimpleNamespace(ui_lock_count=0, editors=[(macro, "Macros")]))
    setting = SimpleNamespace(valid=lambda: True, btn_save=SimpleNamespace(isEnabled=lambda: True))
    assert restart_blocked(SimpleNamespace(ui_lock_count=0, editors=[(setting, "Settings")]))


def test_language_change_never_launches_during_operation(qapp, tmp_path, monkeypatch):
    from PyQt5.QtWidgets import QWidget
    manager = LanguageManager(Context(), QSettings(str(tmp_path / "busy.ini"), QSettings.IniFormat))
    parent = QWidget()
    parent.ui_lock_count = 1
    calls = []
    monkeypatch.setattr(QMessageBox, "information", lambda *args: calls.append(args))
    monkeypatch.setattr(manager, "restart", lambda *args: pytest.fail("Restarted during operation"))
    manager.select("de", parent)
    assert calls
    assert manager.pending_language == "de"
    parent.close()


def test_restart_waits_for_real_process():
    import subprocess
    import sys
    from pandakb_i18n import wait_for_previous_process
    process = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(0.5)"])
    try:
        assert wait_for_previous_process(process.pid)
        assert process.poll() is not None
    finally:
        if process.poll() is None:
            process.terminate()
        process.wait()


@pytest.mark.parametrize("language", [code for code, _ in LANGUAGES])
def test_all_catalog_entries_and_dynamic_tooltips(qapp, tmp_path, language):
    import json
    import xml.etree.ElementTree as ET
    from keycodes.keycodes import Keycode, KEYCODES_LAYERS, recreate_keyboard_keycodes
    from types import SimpleNamespace
    settings = QSettings(str(tmp_path / "complete.ini"), QSettings.IniFormat)
    settings.setValue("language", language)
    manager = LanguageManager(Context(), settings)
    mapping = {} if language == "en" else json.load(open("translations/{}.json".format(language), encoding="utf-8"))
    root = ET.parse("src/main/resources/base/translations/vial_{}.ts".format(language)).getroot()
    try:
        for context in root.findall("context"):
            for message in context.findall("message"):
                source = message.findtext("source")
                expected = source if language == "en" else mapping[source]
                assert QCoreApplication.translate(context.findtext("name"), source) == expected
        keyboard = SimpleNamespace(vial_protocol=6, layers=4, macro_count=2, tap_dance_count=2,
                                   custom_keycodes=None, midi="advanced",
                                   supported_features={"layer_lock", "persistent_default_layer", "repeat_key", "caps_word"})
        recreate_keyboard_keycodes(keyboard)
        expected = QCoreApplication.translate("KeycodeTooltip", "kc on tap, switch to layer {} while held").format(3)
        assert expected in Keycode.tooltip("LT3(KC_A)")
        assert "MIDI" in Keycode.tooltip("MI_C") or language == "en"
        assert Keycode.serialize(Keycode.deserialize("LT3(KC_A)")) == "LT3(KC_A)"
    finally:
        manager.unload()

def test_confirmed_restart_launches_before_closing(qapp, tmp_path, monkeypatch):
    import pandakb_i18n as i18n
    from types import SimpleNamespace
    events = []
    manager = LanguageManager(Context(), QSettings(str(tmp_path / "success.ini"), QSettings.IniFormat))
    parent = SimpleNamespace(ui_lock_count=0, editors=[], close=lambda: events.append("close"))
    monkeypatch.setattr(i18n.QProcess, "startDetached", lambda *args: (events.append("launch"), (True, 123))[1])
    monkeypatch.setattr(qapp, "quit", lambda: events.append("quit"))
    assert manager.restart(parent)
    assert events == ["launch", "close", "quit"]

def test_synthetic_keyboard_opens_all_editors(qtbot):
    from test.test_gui import prepare, FAKE_KEYBOARD
    from pandakb_preview import prepare as prepare_preview
    window, _ = prepare(qtbot, FAKE_KEYBOARD)
    prepare_preview(window)
    assert window.tabs.count() == 11
    assert window.tabs.isVisible()
    assert not window.lbl_no_devices.isVisible()
    assert window.qmk_settings.tabs_widget.count() == 7
    assert window.rgb_configurator.handler_vialrgb.rgb_effect.count() > 40
    assert window.key_override.valid()
    assert window.alt_repeat_key.valid()

@pytest.mark.parametrize("label, expected_bit", [
    ("Don't register the trigger key again after the override is deactivated", 4),
    ("Don't deactivate when another key is pressed down", 5),
])
def test_key_override_visible_option_matches_firmware_bit(qtbot, label, expected_bit):
    from PyQt5.QtWidgets import QCheckBox
    from editor.key_override import OptionsUI
    from protocol.key_override import KeyOverrideOptions
    options = OptionsUI()
    qtbot.addWidget(options)
    # Select by the instruction the user sees, then verify the firmware payload.
    checkbox = next(item for item in options.findChildren(QCheckBox) if item.text() == label)
    checkbox.setChecked(True)
    assert options.save().serialize() == 1 << expected_bit
    options.load(KeyOverrideOptions(1 << expected_bit))
    assert checkbox.isChecked()
