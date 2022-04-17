from usb_hid import Device

from adafruit_macropad import MacroPad
from constants import input_report_size, report_id
from utils import chunks, direction_to_byte


class InputState:
    def __init__(self):
        self.key_states = [False] * 12
        self.misc_states = {
            "rotary": 0,
            "rotary_switch": 0
        }
        self.dirty = False

    def blip_keys(self, event):
        if not event:
            return self

        self.key_states[event.key_number] = event.pressed
        self.dirty = True

    def blip_states(self, **kwargs):
        for key, value in kwargs.items():
            old_val = self.misc_states.get(key)
            self.misc_states[key] = value
            if old_val != value:
                self.dirty = True

    def clean(self):
        self.misc_states["rotary"] = 0
        self.dirty = False


class InputProcessor:
    def __init__(self, macropad: MacroPad, macropad_hid: Device):
        self.macropad = macropad
        self.macropad_hid = macropad_hid
        self.previous_rotary = 0

    def blip(self, state: InputState):
        state.blip_states(
            rotary=self.macropad.encoder - self.previous_rotary,
            rotary_switch=self.macropad.encoder_switch
        )

        reports = []

        def create_report():
            if state.dirty:
                reports.append(InputReport.update_input_report(state))
                state.clean()

                self.previous_rotary = self.macropad.encoder

        create_report()

        key_event = self.macropad.keys.events.get()
        while key_event is not None:
            state.blip_keys(key_event)
            key_event = self.macropad.keys.events.get()

            create_report()

        for report in reports:
            self.macropad_hid.send_report(report, report_id)


class InputReport(object):
    @staticmethod
    def update_input_report(state: InputState):
        report_bytes = bytearray([0] * input_report_size)
        report_bytes[0] = 1  # standard update
        report_bytes[1] = direction_to_byte(state.misc_states['rotary'])
        report_bytes[2] = state.misc_states['rotary_switch']

        key_chunks = list(reversed(list(chunks(state.key_states, 8))))

        for index, chunk in enumerate(key_chunks, start=3):
            report_bytes[index] = sum(v << i for i, v in enumerate(chunk))

        return report_bytes

    @staticmethod
    def acknowledge_input_report(ack_id: int):
        report_bytes = bytearray([0] * input_report_size)
        report_bytes[0] = 0  # ACK
        report_bytes[1] = ack_id

        return report_bytes
