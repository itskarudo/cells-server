from threading import Thread
from server import reload_event
from server.db import Session
from server.db.models import Device


class Scanner(Thread):

    def run(self):
        reload_event.on("init", self.init_handler)
        reload_event.on("reload", self.reload_handler)

    def init_handler(self):
        session = Session()
        devices = session.query(Device).all()
        session.flush()
        session.close()
        self.reload_handler(devices=devices)


    def reload_handler(self, devices):
        print(devices)
