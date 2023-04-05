from flask import Flask, send_from_directory, request, jsonify
import logging
from Edistribucion import Edistribucion
from flask_cors import CORS
import requests
import json

app = Flask(__name__, static_url_path="", static_folder="client/dist")
CORS(app)  # comment this on deployment
edis = Edistribucion(debug_level=logging.ERROR)


@app.route("/", defaults={"path": ""})
def serve(path):
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/v1/cups", methods=["GET"])
def get_cups():
    return jsonify(edis.get_active_cups())


@app.route("/api/v1/cycles", methods=["GET"])
def get_cycles():
    cups = edis.get_active_cups()
    response = edis.get_list_cycles(cups["Id"])
    return jsonify(response)


@app.route("/api/v1/measures", methods=["GET"])
def get_measured_points():
    cycle = int(request.args.get("cycle") or 0)
    cups = edis.get_active_cups()
    cycles = edis.get_list_cycles(cups["Id"])
    response = edis.get_meas(cups["Id"], cycles[cycle])
    return jsonify(response)


@app.route("/api/v1/pvpc/today", methods=["GET"])
def get_pvpc_prices_today():
    response = requests.get("https://api.preciodelaluz.org/v1/prices/all?zone=PCB")
    # the response is a json, so we can return it directly
    # The problem is that it escapes the quotes, so we need to unescape them
    return jsonify(json.loads(response.text))


# get_meas_interval(self, cont, startDate, endDate):


def minified(x):
    return {"value": x["hourCCH"], "hour": x["valueDouble"]}


@app.route("/api/v1/measures/interval", methods=["GET"])
def get_measured_points_interval():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    cups = edis.get_active_cups()
    # response = edis.get_meas_interval(cups['Id'], start_date, end_date)
    # load json file from disk
    response = json.load(open("lastMonth-from-api.json"))

    # TODO: test if this works
    result = {d["date"]: {h["hour"]: h for h in d} for d in response}

    # dates = set([x['date'] for x in [y[0] for y in response]])

    # Response is a list of lists of dicts. Group by each dict's "date" key
    # and return a dict with the date as key and the list of dicts as value
    # response = {date: [x for x in y if x['date'] == date]
    #             for date in dates for y in response}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=False)
