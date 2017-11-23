import math


def find_boundaries(timestamp):
    """
    Given a unix timestamp calculate the start and the end of the day
    :param timestamp:
    :return: a tuple containing start and end dates in unix timestamp
    """
    first = math.floor(timestamp / 86400) * 86400
    second = first + ((24 * 60 * 60) - 1)
    return first, second
