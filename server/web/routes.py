import netifaces as ni
from flask_restful import Resource


class IFace(Resource):
    def get(self):
        ifaces = ni.interfaces()
        return ifaces
