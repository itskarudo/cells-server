from server.web.utils import is_mac


def device_validation(data, active=False):
    errors = []
    if "name" not in data:
        errors.append("NAME_NOT_FOUND")

    if "mac" not in data:
        errors.append("MAC_NOT_FOUND")
    elif not is_mac(data["mac"]):
        errors.append("MAC_NOT_VALID")

    if "interface" not in data:
        errors.append("INTERFACE_NOT_FOUND")

    if active and "active" not in data:
        errors.append("ACTIVE_NOT_FOUND")

    return errors
