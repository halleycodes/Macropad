import time
from adafruit_macropad import MacroPad
from hid_helper import get_macropad_hid, get_keyboard_hid
from input import InputState, InputProcessor
from output import OutputProcessor

macropad = MacroPad()
input_state = InputState()

macropad_hid = get_macropad_hid()

input_processor = InputProcessor(macropad=macropad, macropad_hid=get_macropad_hid())
output_processor = OutputProcessor(macropad=macropad, macropad_hid=get_macropad_hid(), keyboard_hid=get_keyboard_hid())

macropad.display_image("blinka.bmp")

while True:
    try:
        input_processor.blip(input_state)
    except:
        print("Oops, busy usb")
    output_processor.blip()

    time.sleep(.1)
