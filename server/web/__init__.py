import netifaces as ni
from flask_restful import Resource
from server.db import Session
from server.db.models import Device
from server.db.schemas import DeviceSchema


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
