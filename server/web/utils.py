import re


def is_mac(address: str):
    isMac = re.match(
        "[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", address.lower())
    return False if isMac is None else True
