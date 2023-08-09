import flask
from threading import Thread
from waitress import serve

app = flask.Flask(__name__)


@app.route('/')
def home():
    return "I'm alive"


def runApp():
  
  # serve(app, host="0.0.0.0", port=8080)
  app.run(host='0.0.0.0',port=8080)

def run():
  Thread(target=runApp).start()