from flask import Flask
from flask import request
import datetime
import json

app = Flask(__name__)


@app.route("/", methods=["POST"])
def post():
    if request.get_json() is not None:
        with open("./DATA/" + str(datetime.datetime.now()) + ".json", "w+") as f:
            json.dump(request.get_json(force=True), f, indent=6)

        return 'Success printing from flask'
    else:
        return 'Request not in json format'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')
