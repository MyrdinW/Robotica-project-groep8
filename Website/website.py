from flask import Flask, render_template
import os
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def execfile(param):
    pass


@app.route("/API")
def api():
    os.system('python Main.py')
    return render_template("index.html")


app.run(port="3000")

