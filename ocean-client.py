from flask import Flask
app = Flask(__name__)

state=Object()
state.currentString = ""


@app.route("/char")
def hello():
    return "fuck"

@app.route("/")
def hello():
    return "fuck"


if __name__ == "__main__":
    app.run()
