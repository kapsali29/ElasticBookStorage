from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/ask/storage/', methods=['POST'])
def ask_elastic_storage():
    data = request.get_json()
    if 'action' not in data.keys():
        return 'action not in request body', 400
    else:
        return jsonify({'status':'ok'})