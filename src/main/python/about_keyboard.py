from util import tr

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QPlainTextEdit

from protocol.constants import VIAL_PROTOCOL_DYNAMIC, VIAL_PROTOCOL_KEY_OVERRIDE, VIAL_PROTOCOL_ADVANCED_MACROS, \
    VIAL_PROTOCOL_EXT_MACROS, VIAL_PROTOCOL_QMK_SETTINGS


class AboutKeyboard(QDialog):

    def want_min_vial_fw(self, ver):
        if self.keyboard.sideload:
            return tr("AboutKeyboard", "unsupported - sideloaded keyboard")
        if self.keyboard.vial_protocol < 0:
            return tr("AboutKeyboard", "unsupported - VIA keyboard")
        if self.keyboard.vial_protocol < ver:
            return tr("AboutKeyboard", "unsupported - Vial firmware too old")
        return tr("AboutKeyboard", "unsupported - disabled in firmware")

    def about_tap_dance(self):
        if self.keyboard.tap_dance_count > 0:
            return str(self.keyboard.tap_dance_count)
        return self.want_min_vial_fw(VIAL_PROTOCOL_DYNAMIC)

    def about_combo(self):
        if self.keyboard.combo_count > 0:
            return str(self.keyboard.combo_count)
        return self.want_min_vial_fw(VIAL_PROTOCOL_DYNAMIC)

    def about_key_override(self):
        if self.keyboard.key_override_count > 0:
            return str(self.keyboard.key_override_count)
        return self.want_min_vial_fw(VIAL_PROTOCOL_KEY_OVERRIDE)

    def about_alt_repeat_key(self):
        if self.keyboard.alt_repeat_key_count > 0:
            return str(self.keyboard.alt_repeat_key_count)
        return self.want_min_vial_fw(VIAL_PROTOCOL_KEY_OVERRIDE)

    def about_macro_delays(self):
        if self.keyboard.vial_protocol >= VIAL_PROTOCOL_ADVANCED_MACROS:
            return tr("AboutKeyboard", "yes")
        return self.want_min_vial_fw(VIAL_PROTOCOL_ADVANCED_MACROS)

    def about_macro_ext_keycodes(self):
        if self.keyboard.vial_protocol >= VIAL_PROTOCOL_EXT_MACROS:
            return tr("AboutKeyboard", "yes")
        return self.want_min_vial_fw(VIAL_PROTOCOL_EXT_MACROS)

    def about_qmk_settings(self):
        if self.keyboard.vial_protocol >= VIAL_PROTOCOL_QMK_SETTINGS:
            if len(self.keyboard.supported_settings) == 0:
                return tr("AboutKeyboard", "disabled in firmware")
            return tr("AboutKeyboard", "yes")
        return self.want_min_vial_fw(VIAL_PROTOCOL_QMK_SETTINGS)

    def about_feature(self, feature_name):
        if feature_name in self.keyboard.supported_features:
            return tr("AboutKeyboard", "yes")
        return self.want_min_vial_fw(VIAL_PROTOCOL_DYNAMIC)

    def __init__(self, device):
        super().__init__()

        self.keyboard = device.keyboard
        self.setWindowTitle(tr("AboutKeyboard", "About {}").format(device.title()))

        text = ""
        desc = device.desc
        text += tr("AboutKeyboard", "Manufacturer: {}\n").format(desc["manufacturer_string"])
        text += tr("AboutKeyboard", "Product: {}\n").format(desc["product_string"])
        text += tr("AboutKeyboard", "VID: {:04X}\n").format(desc["vendor_id"])
        text += tr("AboutKeyboard", "PID: {:04X}\n").format(desc["product_id"])
        text += tr("AboutKeyboard", "Device: {}\n").format(desc["path"])
        text += "\n"

        if self.keyboard.sideload:
            text += tr("AboutKeyboard", "Sideloaded JSON, Vial functionality is disabled\n\n")
        elif self.keyboard.vial_protocol < 0:
            text += tr("AboutKeyboard", "VIA keyboard, Vial functionality is disabled\n\n")

        text += tr("AboutKeyboard", "VIA protocol: {}\n").format(self.keyboard.via_protocol)
        text += tr("AboutKeyboard", "Vial protocol: {}\n").format(self.keyboard.vial_protocol)
        text += tr("AboutKeyboard", "Vial keyboard ID: {:08X}\n").format(self.keyboard.keyboard_id)
        text += "\n"

        text += tr("AboutKeyboard", "Macro entries: {}\n").format(self.keyboard.macro_count)
        text += tr("AboutKeyboard", "Macro memory: {} bytes\n").format(self.keyboard.macro_memory)
        text += tr("AboutKeyboard", "Macro delays: {}\n").format(self.about_macro_delays())
        text += tr("AboutKeyboard", "Complex (2-byte) macro keycodes: {}\n").format(self.about_macro_ext_keycodes())
        text += "\n"

        text += tr("AboutKeyboard", "Tap Dance entries: {}\n").format(self.about_tap_dance())
        text += tr("AboutKeyboard", "Combo entries: {}\n").format(self.about_combo())
        text += tr("AboutKeyboard", "Key Override entries: {}\n").format(self.about_key_override())
        text += tr("AboutKeyboard", "Alt Repeat Key entries: {}\n").format(self.about_alt_repeat_key())
        text += tr("AboutKeyboard", "Caps Word: {}\n").format(self.about_feature("caps_word"))
        text += tr("AboutKeyboard", "Layer Lock: {}\n").format(self.about_feature("layer_lock"))
        text += "\n"

        text += tr("AboutKeyboard", "QMK Settings: {}\n").format(self.about_qmk_settings())

        font = QFont("monospace")
        font.setStyleHint(QFont.TypeWriter)
        self.textarea = QPlainTextEdit()
        self.textarea.setReadOnly(True)
        self.textarea.setFont(font)

        self.textarea.setPlainText(text)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.textarea)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.resize(640, 540)
