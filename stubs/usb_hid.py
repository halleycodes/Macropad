from typing import Optional
from unittest.mock import MagicMock

_macropad_mock = MagicMock()
_macropad_mock.usage = 0x01
_macropad_mock.usage_page = 0x0C

devices = [
    _macropad_mock
]


class Device:
    def send_report(self, buf: bytes, report_id: Optional[int] = None) -> None:
        pass

    def get_last_received_report(self, report_id: Optional[int] = None) -> bytes:
        pass


enable = MagicMock()
