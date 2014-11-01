from flask import Flask
app = Flask(__name__)
 
state=Object()
state.currentClientString = ""

initialized = False

plugins = []
listeners = {}

oceanClient = OceanClient()

def registerListener(plugin, string):
	if string not in listeners.keys:
		listeners[string] = []
	listeners[string].append(plugin)

@app.route("/")
def rootRoute():
	if not initialized:
		init();
		initialized = True
    return send_static_file("./client/client.html")

#handles a character being typed
@app.route("/api/handletyped")
def handletyped():


#string 
@app.route("/api/insertString")
def hello():
    return "unimplemented"

if __name__ == "__main__":
    app.run()
