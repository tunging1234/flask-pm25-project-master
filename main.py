from flask import Flask, render_template, jsonify
import database

app = Flask(__name__)


@app.route("/api/data/<county>")
def api_data_by_county(county):
    rows = database.get_data_by_county(county)["rows"]
    return jsonify(rows)


@app.route("/api/counties")
def api_counties():
    counties = database.get_counties()["rows"]
    counties = [c[0] for c in counties]

    return jsonify(counties)

@app.route("/api/data/six_counties")
def api_six_counties():
    six_counties = ["", "", "桃", "中", "南", ""]
    fields, datas = database.get_latest_data()
    result = {}
    if datas:
        df = pd.DataFrame(datas, columns=fields)
        for county in six_counties:
            avg = df[df["county"] == county]["pm25"].mean().round(2)
        result[county] = avg
    return jsonify(result)

@app.route("/")
def index():

    result = database.get_latest_data()
    counties = database.get_counties()["rows"]
    counties = [c[0] for c in counties]

    data = {}
    if result["success"]:
        datatime = result["rows"][0][4]
        datas = sorted(result["rows"],key=lambda x:x[3])
        min_value=datas[0]
        max_value=datas[-1]
        print(datatime, min_value, max_value)
    
        data["datatime"] = datatime
        data["min"] = [min_value[1], min_value[3]]
        data["max"] = [max_value[1], max_value[3]]

    return render_template("index.html", result=result, counties=counties, data=data)


if __name__ == "__main__":
    app.run(debug=True)
