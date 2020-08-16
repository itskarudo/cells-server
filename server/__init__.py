from flask import Flask
from flask_restful import Api
from server.web.routes import IFace

import event_emitter as events

reload_event = events.EventEmitter()

app = Flask(__name__)
api = Api(app)


api.add_resource(IFace, '/ifaces')
