from flask import Flask, jsonify, request
app = Flask(__name__)

books = [
    {'name': 'Green Eggs and Ham',
     'price': 7.99,
     'isbn': 9870394800165
     },
    {'name': 'The Cat In the Hat',
     'price': 6.99,
     'isbn': 9870394800193
     }
]

@app.route('/books')
def get_books():
    return jsonify({'books': books})

app.run(port=5000)