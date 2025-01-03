import pandas as pd 
import json
from fpgrowth_py import fpgrowth
import pickle


def read_dataset(path):
    playlist_baskets = []

    for chunk in pd.read_csv(path, chunksize=50000):

        basket = chunk.groupby('pid')['track_name'].apply(list).tolist()
        playlist_baskets.extend(basket)
    
    return playlist_baskets


def generate_rules(playlist_baskets, min_support=0.05, min_confidence=0.2):
    freqItemSet, rules = fpgrowth(playlist_baskets, minSupRatio=min_support, minConf=min_confidence)
    
    rules_json = [ { "antecedent": list(rule[0]), "consequent": list(rule[1]), "confidence": rule[2] } for rule in rules ]

    return rules_json

def save_rules(rules, path):
    with open(path, 'wb') as f:
        pickle.dump(rules, f)

def load_rules(path):
    with open(path, 'rb') as f:
        rules = pickle.load(f)
    
    return rules


def main():
    filepath = '2023_spotify_ds1.csv'

    print('Processing dataset...')
    playlist_baskests = read_dataset(filepath)

    print('Generating rules...')
    rules = generate_rules(playlist_baskests)

    print('Saving rules...')
    save_rules(rules, 'rules.pkl')

    print('DONE!')


if __name__ == '__main__':
    main()

    
