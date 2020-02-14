from flask import Flask, request, jsonify

from query_builder import QueryBuilder

app = Flask(__name__)

builder = QueryBuilder()


@app.route('/ask/storage/', methods=['POST'])
def ask_elastic_storage():
    data = request.get_json()
    if 'action' not in data.keys():
        return 'action not in request body', 400
    else:
        elastic_results = builder.command(action=data['action'], payload=data)
        json_results = builder.get_source(elastic_results)
        return jsonify(json_results)
