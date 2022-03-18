# -*- coding: utf-8 -*-
import warnings
import pickle as pkl

import flask
from flask import (
    request,
    jsonify,
    render_template,
    abort
)

from utils.text_preprocessing import preprocessing, replace_repetitions

warnings.filterwarnings('ignore')


# environments
PATH_MODEL = 'models/'

# run flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# load models
with open(PATH_MODEL + 'log_pipeline.pickle', 'rb') as f:
    model = pkl.load(f)

# load vocab
with open(PATH_MODEL + 'vocab.pickle', 'rb') as f:
    vocab = pkl.load(f)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/analyze_text', methods=['GET', 'POST'])
def analyze_text():
    global model, vocab
    if request.method == 'GET':
        if request.json:
            text = request.json.get('text', '')
        else:
            return jsonify({"error": "please, write text or send json as {'text': ...}"}), 403

        text_process = preprocessing(text)
        text_process = replace_repetitions(text_process, vocab)
        pred = model.predict_proba([text_process])[:, 1][0]

        return jsonify({'text': text, 'toxic': pred})
    elif request.method == 'POST':
        text = request.form['text']
        text_process = preprocessing(text)
        text_process = replace_repetitions(text_process, vocab)
        pred = model.predict_proba([text_process])[:, 1][0]

        return render_template('home.html', text=text, toxic=pred)
    else:
        return abort(404)


if __name__ == '__main__':
    app.run()
