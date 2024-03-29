import netifaces as ni
from flask import request
from flask_restful import Resource
from server.db import Session
from server.db.models import Device, Script
from server.db.schemas import DeviceSchema, ScriptSchema
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

        if not raw_device:
            session.flush()
            session.close()
            return {"ok": False, "errors": ["DEVICE_NOT_FOUND"]}, 404
        else:

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


class SwitchDeviceRoute(Resource):
    def get(self, device_id):
        session = Session()
        device = session.query(Device).filter(Device.id == device_id).first()

        if device is None:
            return {"ok": False, "errors": ["DEVICE_NOT_FOUND"]}, 400
        else:
            device.active = not device.active
            session.commit()

            device_schema = DeviceSchema()
            device_json = device_schema.dump(device)

            return {"ok": True, "device": device_json}


class ScriptsRoute(Resource):
    def get(self):

        device_id = request.args.get('device_id')

        session = Session()

        if device_id is None:
            raw_scripts = session.query(Script).all()
        else:
            raw_scripts = session.query(Script).filter(
                Script.device_id == device_id).all()

        script_schema = ScriptSchema(many=True)
        scripts = script_schema.dump(raw_scripts)

        session.flush()
        session.close()

        return {"ok": True, "scripts": scripts}

    def post(self):
        data = request.get_json()

        errors = []

        if "command" not in data:
            errors.append("COMMAND_NOT_FOUND")
        if "device_id" not in data:
            errors.append("DEVICE_ID_NOT_FOUND")

        if not errors:
            session = Session()

            parent_device = session.query(Device).filter(
                Device.id == data["device_id"]).first()

            if parent_device is None:
                session.flush()
                session.close()
                return {"ok": False, "errors": ["PARENT_DEVICE_NOT_FOUND"]}, 400

            else:

                script = Script(command=data["command"],
                                device_id=data["device_id"])

                session.add(script)
                session.commit()

                script_schema = ScriptSchema()
                script_json = script_schema.dump(script)

                session.flush()
                session.close()

                return {"ok": True, "script": script_json}

        else:
            return {"ok": False, "errors": errors}, 400


class ScriptRoute(Resource):
    def get(self, script_id):
        session = Session()
        raw_script = session.query(Script).filter(
            Script.id == script_id).first()

        if not raw_script:
            session.flush()
            session.close()
            return {"ok": False, "errors": ["SCRIPT_NOT_FOUND"]}, 404
        else:

            script_schema = ScriptSchema()
            script = script_schema.dump(raw_script)

            session.flush()
            session.close()

            return {"ok": True, "script": script}

    def delete(self, script_id):
        session = Session()
        session.query(Script).filter(Script.id == script_id).delete()
        session.commit()

        session.flush()
        session.close()

        return {"ok": True}

    def put(self, script_id):
        data = request.get_json()

        if "command" not in data:
            return {"ok": False, "errors": ["COMMAND_NOT_FOUND"]}, 400

        else:
            session = Session()

            script = session.query(Script).filter(
                Script.id == script_id).first()

            if script is None:
                return {"ok": False, "errors": ["SCRIPT_NOT_FOUND"]}, 404

            else:
                script.command = data["command"]

                session.commit()

                script_schema = ScriptSchema()
                script_json = script_schema.dump(script)

                session.flush()
                session.close()

                return {"ok": True, "script": script_json}
