from flask import Flask, jsonify, request, Response, json
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

def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

@app.route('/books')
def get_books():
    return jsonify({'books': books})

@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject((request_data))):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Location'] = "/books/"+str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object pased in request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.9, 'isbn': 1321235435}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype='application/json')
        return response


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)


app.run(port=5000)