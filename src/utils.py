def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def direction_to_byte(direction):
    if direction == 0:
        return 0

    if direction < 0:
        return 255

    return 1


def map_range(x, in_min, in_max, out_min, out_max):
    """
    Maps a number from one range to another.
    Note: This implementation handles values < in_min differently than arduino's map function does.
    :return: Returns value mapped to new range
    :rtype: float
    """
    mapped = (x-in_min) * (out_max - out_min) / (in_max-in_min) + out_min
    if out_min <= out_max:
        return max(min(mapped, out_max), out_min)
    return min(max(mapped, out_max), out_min)


null_byte = bytes([0x0])


def make_empty_bytes(count):
    return bytes([0] * count)
