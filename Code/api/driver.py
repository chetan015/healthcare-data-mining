from os import path
import sys
sys.path.append(path.abspath('../services'))
from search_service import SearchService
from sympgraph_service import SympgraphService

from flask import Flask, request, send_file, jsonify, redirect
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

search_service = SearchService()
sympgraph_service = SympgraphService()

@app.route("/")
def home():
    app.logger.info("[api-home]")
    return "Home"

@app.route("/api/v1/search", methods=["GET"])
@cross_origin()
def search():
    global search_service

    q_term = request.args.get("query_term")
    q_type = request.args.get("query_type")
    q_site = request.args.get("query_site")

    query_object = {
        "query_term": q_term,
        "query_type": q_type,
        "query_site": q_site
    }
    temp = search_service.search(query_object)
    return jsonify(temp)

@app.route("/api/v1/sympgraph", methods=["GET"])
@cross_origin()
def getRankedList():
    global sympgraph_service

    q_term = request.args.get("query_term")
    temp = sympgraph_service.getSymptoms(q_term)
    return jsonify(temp)

if __name__ == "__main__":
    app.run(debug=True)