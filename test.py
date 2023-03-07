from flask import Flask

app = Flask(__name__)


@app.route("/hello/<id>")
def hello_world(id):
    if id == str(1):
        return "xmx"
    elif id == str(2):
        return "XMX"
    else:
        return "<p>Hello, World!</p>"


if __name__ == '__main__':
    app.run()
