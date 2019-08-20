from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello Wordl"


@app.route('/card')
def card():
    # processe
    #
    return 'retorno'
