from flask import Flask, request, jsonify
from flask_cors import CORS

from query_builder import QueryBuilder

app = Flask(__name__)
CORS(app)

builder = QueryBuilder()


@app.route('/ask/storage/', methods=['POST'])
def ask_elastic_storage():
    data = request.get_json()

    if 'action' not in data.keys():
        return 'action not in request body', 400
    else:
        elastic_results = builder.command(action=data['action'], payload=data)
        json_results = builder.get_source(elastic_results)

        if 'file_type' in data.keys():
            builder.save_results(
                results=json_results,
                file_name=data['action'],
                file_type=data['file_type']
            )

        return jsonify(json_results)
