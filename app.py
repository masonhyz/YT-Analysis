from flask import Flask, render_template
import json
import plotly
from plots import fig11, fig12, fig2, fig3, fig4

app = Flask(__name__)

g11 = json.dumps(fig11, cls=plotly.utils.PlotlyJSONEncoder)
g12 = json.dumps(fig12, cls=plotly.utils.PlotlyJSONEncoder)
g2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
g3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
g4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)


@app.route("/")
def index():
    return render_template("index.html", title = "Home",
                           graph11JSON = g11,
                           graph12JSON = g12,
                           graph2JSON = g2,
                           graph3JSON = g3,
                           graph4JSON = g4)


if __name__ == "__main__":
    app.run(debug=True)
