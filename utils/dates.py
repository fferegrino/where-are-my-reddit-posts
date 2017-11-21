import math


def find_boundaries(timestamp):
    first = math.floor(timestamp / 86400) * 86400
    second = first + ((24 * 60 * 60) - 1)
    return first, second
