import netifaces as ni
from flask import request
from flask_restful import Resource
from server.db import Session
from server.db.models import Device
from server.db.schemas import DeviceSchema
from server.web.utils import is_mac


class IFace(Resource):
    def get(self):
        ifaces = ni.interfaces()
        return ifaces


class Devices(Resource):
    def get(self):
        session = Session()
        raw_devices = session.query(Device).all()

        device_schema = DeviceSchema(many=True)
        devices = device_schema.dump(raw_devices)

        session.flush()
        session.close()

        return devices

    def post(self):
        """
        DATA_FORMAT = {
            name: str,
            mac: MAC(str),
            interface: str
        }
        """
        data = request.get_json()

        errors = []
        if "name" not in data:
            errors.append("NAME_NOT_FOUND")

        if "mac" not in data:
            errors.append("MAC_NOT_FOUND")
        elif not is_mac(data["mac"]):
            errors.append("MAC_NOT_VALID")

        if "interface" not in data:
            errors.append("INTERFACE_NOT_FOUND")

        if not errors:

            session = Session()

            device = Device(
                name=data["name"], mac=data["mac"], interface=data["interface"])
            session.add(device)
            session.commit()

            device_schema = DeviceSchema()
            json_device = device_schema.dump(device)

            session.flush()
            session.close()

            return json_device

        else:
            return errors, 400
