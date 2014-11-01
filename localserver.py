from flask import Flask
from ocean import Plugin, OceanClient
app = Flask(__name__)
 
state=Object()
state.currentClientString = ""

initialized = False
oceanClient = OceanClient()


@app.route("/")
def rootRoute():
    return send_static_file("./client/client.html")


@app.route("/api/connect/<servername>/<nick>/<int:port>")
def handleConnectWithPort():
	return handleConnect(servername, port, nick)

@app.route("/api/connect/<servername>/<nick>")
def handeConnectWithoutPort(servername, nick):
	return handleConnect(servername, 6667, nick)

def handleConnect(servername, port, nick):
	if not connected:
		return oceanClient.connectAndInit(servername, port, nick)
	return "already connected..."


#handles a character being typed
@app.route("/api/chartyped")
def handletyped():
	return "unimplemented"

#string 
@app.route("/api/insertString")
def hello():
    return "unimplemented"

if __name__ == "__main__":
    app.run()
