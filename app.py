from flask import Flask, render_template
import json
import plotly
import plots as plots


app = Flask(__name__)

graph1JSON = json.dumps(plots.fig1, cls=plotly.utils.PlotlyJSONEncoder)


@app.route("/")
def index():
    return render_template("index.html", title = "Home", graph1JSON = graph1JSON)
