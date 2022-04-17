import unittest
from unittest.mock import MagicMock

from output import OutputProcessor


class TestOutput(unittest.TestCase):
    def test_set_line(self):
        macropad = MagicMock()
        macropad_hid = MagicMock()
        keyboard_hid = MagicMock()
        processor = OutputProcessor(macropad, macropad_hid, keyboard_hid)

        output_report = [0]*35
        output_report[0] = 3
        output_report[1] = 69
        output_report[2] = 1

        text = "This is a really long text that should get cropped properly"

        for index in range(3, 35):
            output_report[index] = ord(text[index-3])

        processor.set_text(bytes(output_report))
