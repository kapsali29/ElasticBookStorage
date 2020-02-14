from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/ask/storage/', methods=['POST'])
def ask_elastic_storage():
    data = request.get_json()
    print(data)
    return jsonify({'status':'ok'})