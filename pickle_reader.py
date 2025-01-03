import pickle
from collections import OrderedDict


def load_model(path):
    
    with open(path, "rb") as f:
        model = pickle.load(f)

    return model


def main():
    rules = load_model('rules.pkl')
    recommended_songs = []
    songs = ["Believe", "Purpose", "Sorry", "Love Yourself", "What Do You Mean?", "7 Rings", "Into You", "One Last Time", "blinding lights", "Starboy", "Save Your Tears"]
    for i, rule in enumerate(rules):
        antecedent = set(rule["antecedent"])
        consequent = set(rule["consequent"])
        confidence = rule["confidence"]
        if antecedent.issubset(songs):
            recommended_songs.append((tuple(consequent), confidence))
    
    
    recommended_songs.sort(key=lambda x: x[1], reverse=True)

    unique = list(OrderedDict.fromkeys(song for item, _ in recommended_songs for song in item))

    # a = [list(i) for i in unique]



    # print(a)

    print(unique)


if __name__ == '__main__':
    main()