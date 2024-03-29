from flask import Flask
from flask_restful import Api
from server.web import InterfacesRoute, DevicesRoute, DeviceRoute, ScriptsRoute, ScriptRoute, SwitchDeviceRoute

import event_emitter as events

reload_event = events.EventEmitter()

app = Flask(__name__)
api = Api(app)

api.add_resource(InterfacesRoute, '/interfaces')
api.add_resource(DevicesRoute, '/devices')
api.add_resource(DeviceRoute, '/device/<device_id>')
api.add_resource(SwitchDeviceRoute, '/device/<device_id>/switch')
api.add_resource(ScriptsRoute, '/scripts')
api.add_resource(ScriptRoute, '/script/<script_id>')
