from server.core.scanner import Scanner
from server import app, reload_event

if __name__ == "__main__":
    scanner = Scanner()
    scanner.start()
    reload_event.emit("reload", devices=[])
    app.run(debug=True)
