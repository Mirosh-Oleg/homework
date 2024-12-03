import geopandas as gpd
from flask_cors import CORS
from sqlalchemy import create_engine
from flask import Flask, jsonify, Response

app = Flask(__name__)
CORS(app)


def connect_to_database():
    user = input("Enter database username: ")

    password = input("Enter database password: ")

    host = input("Enter database host (default: localhost): ")

    port = input("Enter database port (default: 5432): ")

    database = input("Enter database name: ")

    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(connection_string)


engine = connect_to_database()


@app.route("/grid", methods=["GET"])
def get_grid():
    query = "SELECT * FROM ukraine_grid"
    grid = gpd.read_postgis(query, con=engine, geom_col="geometry")
    geojson = grid.to_json()
    return Response(geojson, mimetype="application/json")


@app.route("/border", methods=["GET"])
def get_border():
    query = "SELECT * FROM ukraine_border"
    border = gpd.read_postgis(query, con=engine, geom_col="geometry")
    geojson = border.to_json()
    return Response(geojson, mimetype="application/json")


@app.route("/sectors", methods=["GET"])
def get_sectors():
    query = "select * from sectors"
    sectors = gpd.read_postgis(query, con=engine, geom_col="geometry")
    geojson = sectors.to_json()
    return Response(geojson, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
