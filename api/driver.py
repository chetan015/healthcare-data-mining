from os import path
import sys
sys.path.append(path.abspath('../services'))
from search_service import SearchService
# from project.services.search_service import search_service

from flask import Flask, request, send_file, jsonify, redirect
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

search_service = SearchService()

@app.route("/")
def home():
    app.logger.info("[api-home]")
    return "Home"

@app.route("/api/v1/search", methods=["GET"])
@cross_origin()
def search():
    global search_service
    # print(dir(request))
    # print(request.args)
    # q_term = request.args["query_term"]
    q_term = request.args.get("query_term")
    q_type = request.args.get("query_type")
    # print(q_term)
    # q_symptom = request.args.get("symptom")
    query_object = {
        "query_term": q_term,
        "query_type": q_type
    }
    temp = search_service.search(query_object)
    # print(temp)
    return jsonify(temp)

if __name__ == "__main__":
    app.run(debug=True)