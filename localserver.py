from flask import Flask, request
import logging
from ocean import *
import unicodedata
import json, random
import threading
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


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
    return send_static_file("./static/client.html")

@app.route("/api/connect/<hostname>/<username>/<nick>/<int:port>")
@app.route("/api/connect/<hostname>/<username>/<nick>/<realname>/<int:port>")
@app.route("/api/connect/<hostname>/<username>/<nick>/")
def handleConnect(hostname, username, nick, realname="Shia Labeouf", port=6667):
    """
    global connected
    if not connected:
        connected = True
        client.connect( nouni(hostname), nouni(nick), port)
        return "opening connection..."

    return "already connected..."
    """
    print "handling connect..."
    # Run IRC client in a separate thread
    client.register(username, realname, nick)
    client.connect(hostname)
    client_thread = threading.Thread(target=client.run)
    client_thread.daemon = True
    client_thread.start()
    print "client thread started. %s %s %s" % (username, realname, nick)
    #information about the user you just logged in as
    return json.dumps({
        "username": username,
        "realname": realname,
        "nick": nick})

imgs = ["./static/imgdump/user-icon-09.svg",
        "./static/imgdump/user-icon-10.svg",
        "./static/imgdump/user-icon-11.svg"]

@app.route("/api/join/<channel>/")
def getUserList(channel):
    channel = '#' + channel
    client.send('JOIN %s' % channel)
    while not channel in client.get_channels():
        continue
    chandata = client.get_channels()[channel]
    for user in chandata['users']:
        # Scrubbing chanops @ because it's messing with message icons
        if user['nick'][0] == '@':
            user['nick'] = user['nick'][1:]
        user['icon'] = random.choice(imgs)
    print chandata
    #return json.dumps(client.get_channels()[channel])
    return json.dumps(chandata)

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
@app.route("/api/pushMessage/<channel>", methods=['POST'])
def pushMessage(channel):
    print channel, request.form["message"]
    client.send_message('#' + channel, request.form["message"])
    return "{}"

triggered = False
@app.route("/api/getMessages/")
def getMessages():
    out = client.read_outbuf()
    if len(out) > 0:
        print out
    client.clear_outbuf()
    for msg in out:
        msg['timestamp'] = float(msg['timestamp']) * 1000
    return json.dumps(out)
    """
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
    """

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
