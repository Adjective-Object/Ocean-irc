from flask import Flask
from ocean import *
import unicodedata
import json, random
app = Flask(__name__)

connected = False
client = OceanClient()

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
    """
    global connected
    if not connected:
        connected = True
        client.connect( nouni(hostname), nouni(nick), port)
        return "opening connection..."

    return "already connected..."
    """
    return "not implemented"


@app.route("/api/join/<channel>/")
def getUserList(channel):
    #fake user list
    return json.dumps(
        {   "public": True,
            "topic": "WHERE WIFI GOES TO DIE",
            "users": [
                {   "realname": "PJ Rosa",
                    "nick": "de-mote"
                },
                {   "realname": "Jeff Tao",
                    "nick": "jtao"
                },
                {   "realname": "Nolan Lum",
                    "nick": "nolm"
                },
                {   "realname": "God Damn Billy",
                    "nick": "insectMechanics"
                },
                {   "realname": "insectMechanics",
                    "nick": "God Damn Billy"
                },
                {   "realname": "PRo Koder",
                    "nick": "PRoKoder"
                }
            ]})

#handles a character being typed
@app.route("/api/autocompletes/")
def getAutoCompletes():
    return json.dumps([
        {   "open": "/",
            "close": " ",
            "completes": {
                "join": "join"
            }
        },
        {   "open": ":",
            "close": ":",
            "completes": {
                "fuck": u'(\uFF61 \u2256 \u0E34 \u203F \u2256 \u0E34)'
            }
        }
    ])

#string 
@app.route("/api/pushMessage/", methods=['PUSH'])
def pushMessage():
    return "unimplemented"

triggered = False
@app.route("/api/getMessages/")
def getMessages():
    if random.random() < 0.5:
        return "[]"
    else:
        return json.dumps([
            {   "channel": "#general",
                "timestamp": 0,
                "usr": "fakeman",
                "msg": "TEMP MESSAGE"
            }
        ])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
