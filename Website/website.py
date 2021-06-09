from flask import Flask, render_template
app = Flask(__name__)

# index page for website
@app.route("/")
def index():
    return render_template("index.html")

# run flask site on port 3000
app.run(port="3000")

