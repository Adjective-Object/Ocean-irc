from flask import Flask
from ocean import *
import unicodedata
app = Flask(__name__)

from twisted.internet import reactor, protocol, ssl

connected = False


def send_static_file(path):
    f = open(path, "r")
    content = ""
    for line in f:
        content += line
    f.close()
    return content


def nouni(str):
    return unicodedata.normalize('NFKD', str).encode('ascii','ignore')

@app.route("/")
def rootRoute():
    print
    return send_static_file("./static/client.html")

@app.route("/api/connect/<hostname>/<nick>/<int:port>")
@app.route("/api/connect/<hostname>/<nick>/")
def handleConnect(hostname, nick, port=6667):
    global connected
    if not connected:
        connected = True
        factory = OceanClientFactory( nouni(nick) )

        reactor.connectSSL(
            nouni(hostname), port, 
            factory, ssl.ClientContextFactory())

        reactor.run()

        return "connecting..."

    return "already connected..."


#handles a character being typed
@app.route("/api/chartyped/")
def handletyped():
    return "unimplemented"

#string 
@app.route("/api/pushString/")
def pushString():
    return "unimplemented"

@app.route("/api/getString/")
def getString():
    return "unimplemented"

if __name__ == "__main__":
    app.run(debug=True)
