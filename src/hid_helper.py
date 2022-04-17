import usb_hid


def get_macropad_hid() -> usb_hid.Device:
    return next(item for item in usb_hid.devices if item.usage == 0x01 and item.usage_page == 0x0C)


def get_keyboard_hid() -> usb_hid.Device:
    return next(item for item in usb_hid.devices if item.usage == 0x06 and item.usage_page == 0x01)