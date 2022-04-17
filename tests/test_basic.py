import unittest

from hid_helper import get_macropad_hid


class TestBasic(unittest.TestCase):
    def test_basic(self):
        macropad = get_macropad_hid()
        assert macropad
