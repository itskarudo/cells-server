from threading import Thread
from server import reload_event


class Scanner(Thread):

    def run(self):
        reload_event.on("reload", self.reload_handler)

    def reload_handler(self, devices):

        print(devices)
