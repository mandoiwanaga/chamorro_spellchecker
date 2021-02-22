from flask import Flask, request, render_template, jsonify
import pandas as pd
from collections import Counter
import numpy as np 
import pickle



with open('webapp/cham_words_dict.pkl', 'rb') as f:
    WORDS = pickle.load(f)
    
with open('webapp/cham_words_df.pkl', 'rb') as f:
    df = pickle.load(f)

app = Flask(__name__, static_url_path="")

@app.route('/')
def index():
    """Return the main page."""
    return render_template('index.html')

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = "åabcdefghijklmnñopqrstuvwxyz'"
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


def known(words): 
    return set(w for w in words if w in WORDS)

def edits2(word): 
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def P(word, N=sum(WORDS.values())): 
    return WORDS[word] / N


def correction(word): 
    return max(candidates(word), key=P)

def candidates(word): 
    return known([word]) or known(edits1(word)) or known(edits2(word)) or [word]

def correction_2(word):
    words = candidates(word)
    return sorted(words, key=lambda x: P(x), reverse=True)[:5]

def correction_3(word):
    recs = {}
    words = candidates(word)
    word_recs = sorted(words, key=lambda x: P(x), reverse=True)[:5]
    for i in word_recs:
        #recs[i] = df.loc[df['word'] == i, ['definition']]
        recs[i] = df.loc[df['word'] == i].definition.values[0]
    return recs


def check_spelling(word):
    if [word] == correction_2(word):
        return print("No Spelling Suggestions Available")
    else:
        return correction_3(word)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Return recommendations."""
    word = request.json
    recs = check_spelling(str(word['user_input']))
    return jsonify({'recs': recs})