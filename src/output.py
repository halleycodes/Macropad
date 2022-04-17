from usb_hid import Device

from adafruit_macropad import MacroPad
from constants import report_id, output_report_size
from input import InputReport
from utils import map_range, null_byte, make_empty_bytes


class OutputProcessor:
    """
    Output format:
    [-1] reportId eaten by API
    [0] commandId
    [1] ackId
    [2:35] data

    commands:
    0 Ping
    1 set led brightness
    2 set led
    3 set text
    4 reflector
    """

    def __init__(self, macropad: MacroPad, macropad_hid: Device, keyboard_hid: Device):
        self.macropad = macropad
        self.macropad_hid = macropad_hid
        self.keyboard_hid = keyboard_hid
        self.text_lines = macropad.display_text()
        self.last_report = bytes([0] * output_report_size)
        self.display_mode = ""

    def blip(self):
        detected_report = self.macropad_hid.get_last_received_report(report_id)
        if self.last_report == detected_report:
            return
        self.last_report = detected_report

        command_id = detected_report[0]
        if command_id == 0:
            return self.ping(detected_report)

        if command_id == 1:
            return self.set_led_brightness(detected_report)

        if command_id == 2:
            return self.set_led(detected_report)

        if command_id == 3:
            return self.set_text(detected_report)

        if command_id == 4:
            return self.keyboard_reflector(detected_report)

        if command_id == 5:
            return self.set_picture(detected_report)

    def ping(self, output_report):
        """
        [0] 0 ping
        [1] ack_id
        :param output_report:
        :return:
        """
        input_report = InputReport.acknowledge_input_report(output_report[1])
        self.macropad_hid.send_report(input_report, report_id)

    def set_led_brightness(self, output_report):
        """
        [0] 1 set led brightness
        [1] ack_id
        [2] brightness (byte)
        :param output_report:
        :return:
        """
        brightness = round(map_range(output_report[2], 0, 255, 0, 1), 2)
        if self.macropad.pixels.brightness != brightness:
            self.macropad.pixels.brightness = brightness

        self.ping(output_report)

    def set_led(self, output_report):
        """
        [0] 2 set led
        [1] ack_id
        [2] count
        [3] first led index
        [4:7] RGB
        [7:10] RBG
        [10:13] RGB
        [13:16] RGB
        [16:19] RGB
        [19:22] RGB
        [22:25] RGB
        [25:28] RGB
        [28:31] RGB
        :param output_report:
        :return:
        """
        count = output_report[2]
        first_led_index = output_report[3]

        for led_index, start_index in [(first_led_index+item, 4 + (item * 3)) for item in range(0, count)]:
            rgb = output_report[start_index:start_index+3]

            if not 0 <= led_index <= 11:
                break

            if self.macropad.pixels[led_index] != rgb:
                self.macropad.pixels[led_index] = rgb[0], rgb[1], rgb[2]

        self.ping(output_report)

    def set_text(self, output_report):
        """
        [0] 3 set text
        [1] ack_id
        [2] row index
        [3:35] text
        :param output_report:
        :return:
        """
        row_index = output_report[2]
        end_index = output_report[3:35].find(null_byte)

        if end_index == -1:
            text = output_report[3:].decode("utf-8")
        else:
            text = output_report[3:3 + end_index].decode("utf-8")

        if self.text_lines[row_index].text != text or self.display_mode != "text":
            if text:
                self.text_lines[row_index].text = text
            else:
                self.text_lines[row_index].text = ""
            self.text_lines.show()

        self.display_mode = "text"
        self.ping(output_report)

    def keyboard_reflector(self, output_report):
        """
        [0] 4 keeb reflector
        [1] ack_id
        [2] modifier
        [3] mode
        [4:10] hid codes
        :param output_report:
        :return:
        """

        modifier = output_report[2]
        mode = output_report[3]
        hid_codes = output_report[4:10]

        self.keyboard_hid.send_report(
            bytes([modifier, 0x0]) + hid_codes
        )

        if mode == 0x1:
            self.keyboard_hid.send_report(make_empty_bytes(8))

        self.ping(output_report)

    def set_picture(self, output_report):
        """
        [0] 5 set picture
        [1] ack_id
        [2] count
        [3:whatever] string
        :param output_report:
        :return:
        """

        count = output_report[2]
        picture_string = output_report[3:3+count]

        try:
            self.macropad.display_image(picture_string)
        except:
            self.text_lines[0].text = "Bad image"
            self.text_lines.show()

        self.display_mode = "picture"
        self.ping(output_report)
