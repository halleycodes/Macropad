import unittest


class TestLed(unittest.TestCase):
    def test_number_generator(self):
        report = [
            2,
            69,
            2,
            0,
            1, 2, 3,
            4, 5, 6,
            7, 8, 9,
            10, 11, 12,
            13, 14, 15,
            16, 17, 18,
            19, 20, 21,
            22, 23, 24,
            25, 26, 27
        ]

        ack_id = report[1]
        count = report[2]
        first_led_index = report[3]

        for led_num, start_index in [(first_led_index+item, 4 + (item * 3)) for item in range(0, count)]:
            rgb = report[start_index:start_index+3]
            print(f"#{led_num},{rgb}")
