from flask import Flask, request
import numpy as np
import json

from deeppavlov import configs, build_model
from pullenti_wrapper.processor import (
    Processor,
    DATE,
    GEO,
    ORGANIZATION,
    PERSON,
    MONEY,
    ADDRESS
)

import re


ner_model = build_model(configs.ner.ner_rus, download=True)
ner_needed = [
    'B-PER', 'I-PER', 'B-GPE', 'I-GPE', 'B-LOC', 'I_LOC',
]


processor = Processor([PERSON, ORGANIZATION, GEO, DATE, MONEY])

app = Flask(__name__)

def ner_entities(text):
    tokens, entities = ner_model([text])
    pairs = list(zip(tokens[0], entities[0]))

    idxs = []
    prev_len, last_start = 0, 0
    for pair in pairs:
        l = len(pair[0])
        if pair[1] in ner_needed:
            last_start = text.find(pair[0], last_start + prev_len)
            idxs.append((last_start, last_start+l))
        prev_len = l
    
    return idxs

def pullenti_entities(text):
    result = processor(text)
    idxs = [match.span for match in result.matches]
    # for match in result.matches:
    #     print(match.referent.label, match.span)
    return idxs

@app.route('/json', methods = ['POST'])
def json_handler():
    content = request.get_json()
    text = content['text']

    left_right_boundaries = ner_entities(text) + pullenti_entities(text)
    return json.loads(dict(boundries=left_right_boundaries))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
