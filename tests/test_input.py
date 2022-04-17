import unittest
from unittest.mock import MagicMock

from input import InputState, InputReport


class TestState(unittest.TestCase):
    def test_init(self):
        keypad = InputState()
        assert keypad.dirty is False
        assert keypad.key_states == [False] * 12

    def test_dirty_keys(self):
        keypad = InputState()
        event = MagicMock()
        event.key_number = 0
        event.pressed = True

        keypad.blip_keys(event)
        assert keypad.dirty is True
        assert keypad.key_states[0] is True

    def test_not_dirty(self):
        keypad = InputState()
        event = {
            "rotary": 0
        }

        keypad.blip_states(**event)
        assert keypad.dirty is False
        assert keypad.misc_states['rotary'] == 0


class TestInputReport(unittest.TestCase):
    def test_basic(self):
        state = InputState()

        event = MagicMock()
        event.key_number = 0
        event.pressed = True

        state.blip_keys(event)
        state.blip_states(rotary=1)
        report_bytes = InputReport.update_input_report(state)
        assert report_bytes[1] == 1
        assert report_bytes[4] == 1

    def test_more_buttons(self):
        state = InputState()

        state.blip_states(rotary=1)
        state.key_states[11] = 1
        state.key_states[9] = 1
        state.key_states[7] = 1
        state.key_states[5] = 1
        state.key_states[3] = 1
        state.key_states[1] = 1

        report_bytes = InputReport.update_input_report(state)
        assert report_bytes[1] == 1
        assert report_bytes[3] == 0b00001010
        assert report_bytes[4] == 0b10101010

    def test_negative_rotary(self):
        state = InputState()

        state.blip_states(rotary=-1)

        report_bytes = InputReport.update_input_report(state)
        assert report_bytes[1] == 255