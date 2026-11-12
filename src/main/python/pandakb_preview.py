# SPDX-License-Identifier: GPL-2.0-or-later
"""Synthetic keyboard for opt-in CI layout checks. Never enumerates real hardware."""
from vial_device import VialDummyKeyboard
from protocol.key_override import KeyOverrideEntry
from protocol.alt_repeat_key import AltRepeatKeyEntry
from keycodes.keycodes import recreate_keyboard_keycodes
from editor.qmk_settings import QmkSettings
from editor.rgb_configurator import VIALRGB_EFFECTS


def prepare(window):
    definition = {
        "matrix": {"rows": 2, "cols": 4},
        "layouts": {"labels": ["ISO"], "keymap": [
            ["0,0", "0,1", "0,2", "0,3"], ["1,0", "1,1", "1,2", "1,3"]]},
        "lighting": "vialrgb", "vial": {"midi": "advanced"},
    }
    device = VialDummyKeyboard()
    device.open(definition)
    device.desc.update(manufacturer_string="PandaKB", product_string="UI test fixture",
                       vendor_id=0, product_id=0)
    keyboard = device.keyboard
    keyboard.vial_protocol = 6
    keyboard.via_protocol = 9
    keyboard.keyboard_id = 0xF00DFACEDEADBEEF
    keyboard.sideload = False
    keyboard.vibl = True
    keyboard.supported_features = {"caps_word", "layer_lock", "repeat_key", "persistent_default_layer"}
    keyboard.tap_dance_count = keyboard.combo_count = 2
    keyboard.key_override_count = keyboard.alt_repeat_key_count = 2
    keyboard.tap_dance_entries = [("KC_A", "KC_LCTRL", "KC_B", "KC_LSHIFT", 200)] * 2
    keyboard.combo_entries = [("KC_A", "KC_B", "KC_NO", "KC_NO", "KC_C")] * 2
    keyboard.key_override_entries = [KeyOverrideEntry(), KeyOverrideEntry()]
    keyboard.alt_repeat_key_entries = [AltRepeatKeyEntry(), AltRepeatKeyEntry()]
    keyboard.supported_settings = set(QmkSettings.qsid_fields)
    keyboard.settings = {qsid: 0 for qsid in keyboard.supported_settings}
    keyboard.reload_settings = lambda: None
    keyboard.lighting_qmk_backlight = keyboard.lighting_qmk_rgblight = True
    keyboard.rgb_supported_effects = {effect.idx for effect in VIALRGB_EFFECTS}
    keyboard.get_unlock_status = lambda *args: 1
    keyboard.matrix_poll = lambda: bytes(32)
    keyboard.reload_rgb()
    recreate_keyboard_keycodes(keyboard)
    window.autorefresh._lock()
    window.autorefresh.current_device = device
    window.rebuild()
    window.refresh_tabs()
    return device
