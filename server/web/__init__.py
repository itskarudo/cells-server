from flask_restful import Resource
from server.db import Session
from server.db.models import Device


class IFace(Resource):
    def get(self):
        ifaces = ni.interfaces()
        return ifaces


class Devices(Resource):
    def get(self):
        session = Session()
        raw_devices = session.query(Device).all()
        devices = []
        for device in raw_devices:
            e = {
                "name": device.name,
                "mac": device.mac,
                "interface": device.interface,
                "active": device.active
            }
            devices.append(e)

        session.flush()
        session.close()
        return devices
