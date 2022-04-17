import usb_hid
from constants import input_report_size, output_report_size, report_id
import storage
import usb_midi
import usb_cdc

MACROPAD_REPORT_DESCRIPTOR = bytes((
    0x05, 0x0C,  # Usage Page (Consumer)
    0x09, 0x01,  # Usage (Consumer Control)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x04,  # Report ID (4)
    0x05, 0x0C,  # Usage Page (Consumer)
    0x09, 0x01,  # Usage (Consumer Control)
    0x15, 0x00,  # Logical Minimum (0)
    0x25, 0x00,  # Logical Maximum (0)
    0x35, 0x00,  # Physical Minimum (0)
    0x45, 0x00,  # Physical Maximum (0)
    0x65, 0x00,  # Unit (None)
    0x55, 0x00,  # Unit Exponent (0)
    0x75, 0x08,  # Report Size (8)
    0x95, 0x20,  # Report Count (32)
    0x81, 0x02,  # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05, 0x0C,  # Usage Page (Consumer)
    0x09, 0x01,  # Usage (Consumer Control)
    0x95, 0x23,  # Report Count (35)
    0x91, 0x02,  # Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
    0xC0,  # End Collection
))

macropad = usb_hid.Device(
    report_descriptor=MACROPAD_REPORT_DESCRIPTOR,
    usage_page=0x0C,
    usage=0x01,
    report_ids=(report_id,),
    in_report_lengths=(input_report_size,),
    out_report_lengths=(output_report_size,),
)

usb_hid.enable(
    (usb_hid.Device.KEYBOARD,
     macropad)
)

usb_midi.disable()
storage.disable_usb_drive()
usb_cdc.disable()
