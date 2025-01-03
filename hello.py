from flask import Flask, request, jsonify
import pickle
from collections import OrderedDict


app = Flask(__name__)



def load_model(path):

    with open(path, "rb") as f:
        model = pickle.load(f)

    return model


app.model = load_model('rules.pkl')

def recommend_songs(songs, rules, n=5, max_rules = 1000000000):
    recommended_songs = []

    for i, rule in enumerate(rules):
        if i == max_rules:
            break
        antecedent = set(rule["antecedent"])
        consequent = set(rule["consequent"])
        confidence = rule["confidence"]

        if antecedent.issubset(songs):
            recommended_songs.append((tuple(consequent), confidence))
    
    recommended_songs.sort(key=lambda x: x[1], reverse=True)

    unique = list(OrderedDict.fromkeys(song for item, _ in recommended_songs for song in item))
    
    return unique



@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    songs = data["songs"]

    recommended_songs = recommend_songs(songs, app.model)


    response = {"songs": recommended_songs}

    return jsonify(response)



if __name__ == "__main__":
    app.model = load_model('rules.pkl')
