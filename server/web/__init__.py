import netifaces as ni
from flask import request
from flask_restful import Resource
from server.db import Session
from server.db.models import Device
from server.db.schemas import DeviceSchema
from server.web.validation import device_validation


class InterfacesRoute(Resource):
    def get(self):
        ifaces = ni.interfaces()
        return ifaces


class DevicesRoute(Resource):
    def get(self):
        session = Session()
        raw_devices = session.query(Device).all()

        device_schema = DeviceSchema(many=True)
        devices = device_schema.dump(raw_devices)

        session.flush()
        session.close()

        return {"ok": True, "devices": devices}

    def post(self):
        """
        DATA_FORMAT = {
            name: str,
            mac: MAC(str),
            interface: str
        }
        """
        data = request.get_json()

        errors = device_validation(data)

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

            return {"ok": True, "device": json_device}

        else:
            return {"ok": False, "errors": errors}, 400


class DeviceRoute(Resource):
    def get(self, device_id):
        session = Session()
        raw_device = session.query(Device).filter(
            Device.id == device_id).first()

        device_schema = DeviceSchema()
        device = device_schema.dump(raw_device)

        session.flush()
        session.close()

        return {"ok": True, "device": device}

    def delete(self, device_id):
        session = Session()
        session.query(Device).filter(Device.id == device_id).delete()
        session.commit()

        session.flush()
        session.close()
        return {"ok": True}

    def put(self, device_id):
        data = request.get_json()
        errors = device_validation(data, active=True)

        if not errors:
            session = Session()
            device = session.query(Device).filter(
                Device.id == device_id).first()

            if device is None:
                return {"ok": False, "errors": ["DEVICE_NOT_FOUND"]}, 404
            else:
                device.name = data["name"]
                device.mac = data["mac"]
                device.interface = data["interface"]
                device.active = data["active"]

                session.commit()

                device_schema = DeviceSchema()
                device_json = device_schema.dump(device)
                session.flush()
                session.close()

                return {"ok": True, "device": device_json}
        else:
            return {"ok": False, "errors": errors}, 400
