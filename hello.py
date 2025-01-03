from flask import Flask, request, jsonify
import pickle


app = Flask(__name__)

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    return jsonify(data)
