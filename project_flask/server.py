from flask import Flask, request, render_template
import datetime
import json
from summary import renderSummaryPlot
from individual import emptyPlot, renderIndividualPlots

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/post", methods = ["POST"])
#@app.route("/")
def post():
    if (request.get_json() is not None):
        d = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open("./DATA/" + d + ".json", "w+") as f:
           json.dump(request.get_json(force=True), f, indent=6) 

        return 'Success printing from flask'
    else:
        return 'Request not in json format'


@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/")
def index2():
    renderSummaryPlot()
    return render_template('index2.html')

@app.route("/individual-plots", methods = ["GET"])
def individual():
    if request.values.get('file') is not None:
        renderIndividualPlots(request.values.get('file'))
    else:
        emptyPlot()
    return render_template('index3.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')
