from flask import Flask
from flask_restful import Api
from server.web import IFace, Devices

import event_emitter as events

reload_event = events.EventEmitter()

app = Flask(__name__)
api = Api(app)

api.add_resource(IFace, '/ifaces')
api.add_resource(Devices, '/devices')
