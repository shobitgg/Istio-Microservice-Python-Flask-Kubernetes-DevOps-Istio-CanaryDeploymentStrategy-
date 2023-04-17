from enum import unique
from flask import Flask, jsonify, render_template, request
import os
import logging
app = Flask(__name__)

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'year_published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'year_published': '1975'}
]


car = [
    {'id': 0,
     'name': 'Arun',
     'car': 'Audi',
     'color': 'Blue',
     'bought': '2021'},
    {'id': 1,
     'name': 'Tipsy',
     'car': 'BMW',
     'color': 'Red',
     'bought': '2022'},
    {'id': 2,
     'name': 'Sam',
     'car': 'Merc',
     'color': 'Blue',
     'bought': '2030'
     }
     
]

@app.route('/api/v1/resources/users/all')
def ws():
    return jsonify(car)


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."
    results = []
    for book in books:
        if book['id'] == id:
            results.append(book)
    return jsonify(results)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
