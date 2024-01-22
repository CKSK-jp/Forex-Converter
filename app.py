from flask import Flask, render_template, request

APP_KEY = "4f2aa5fda843ef40ca348191b63de4ea"
BASE_URL = "http://api.exchangerate.host/convert"

app = Flask(__name__)


@app.route("/")
def converter_home():
    return render_template("index.html")


def input_params(api_key, input, output, amount):
    params = {"access_key": api_key, "from": input, "to": output, "amount": amount}
