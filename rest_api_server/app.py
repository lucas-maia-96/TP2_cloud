import logging
import os
import pickle
from collections import OrderedDict
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

VERSION = "1.0.0"
MODELPATH = "rules.pkl"
MODEL_DATE = datetime.fromtimestamp(os.path.getmtime(MODELPATH)).strftime(
    "%Y-%m-%d %H:%M:%S"
)


def load_model(path):
    global MODEL_DATE
    if not os.path.exists(path):
        logging.error(f"Model file not found: {path}")
        raise FileNotFoundError(f"Model file not found: {path}")

    with open(path, "rb") as f:
        model = pickle.load(f)

    logging.info(f"Model loaded from {path} last modified at {MODEL_DATE}")

    return model


app.model = load_model("rules.pkl")


@app.route("/api/recommend", methods=["POST"])
def recommend():
    try:
        max_rules = 100000000

        if not request.is_json:
            return jsonify({"error": "Request must be a JSON object"}), 400

        data = request.get_json()
        songs = list(set(data["songs"]))

        if not songs:
            return jsonify({"error": "No songs provided"}), 400

        recommended_songs = []

        rules = app.model

        for i, rule in enumerate(rules):
            if i == max_rules:
                break
            antecedent = set(rule["antecedent"])
            consequent = set(rule["consequent"])
            confidence = rule["confidence"]

            if antecedent.issubset(songs):
                recommended_songs.append((tuple(consequent), confidence))

        recommended_songs.sort(key=lambda x: x[1], reverse=True)

        unique = list(
            OrderedDict.fromkeys(song for item, _ in recommended_songs for song in item)
        )

        response = {"songs": unique, "version": VERSION, "model_date": MODEL_DATE}

        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": f"Internal server error -> {e}"}), 500


if __name__ == "__main__":
    app.model = load_model("rules.pkl")
    app.run(debug=True, host="0.0.0.0", port=52046)
