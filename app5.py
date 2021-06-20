from flask import Flask, jsonify, request, Response, json
import json
from settings import *
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


def valid_put_request_data(request_data):
    if "name" in request_data and "price" in request_data:
        return True
    else:
        return False


@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    if not valid_put_request_data(request_data):
        invalidBookObjectErrorMsg = {
            "error": "Valid book object must be passed in the request",
            "helpString": "Data passed in similar to this {'name': 'bookname', 'price': 7.9, 'isbn': 1321235435}"
        }
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    i = 0
    for book in books:
        currentIsbn = book["isbn"]
        if currentIsbn == isbn:
            books[i] = new_book
        i += 1
    response = Response("", status=204)

    return response

@app.route('/books/<int:isbn', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    update_book = {}
    if "name" in request_data:
        update_book["name"] = request_data['name']
    if("price" in request_data):
        update_book["price"] = request_data['price']
    for book in books:
        if book["isbn"] == isbn:
            book.update(update_book)
    response = Response("", status=204)
    response.headers['Location'] = "/books/"+str(isbn)
    return response

# DELETE /books/81123781273

@app.route('/books/<int:isbn>', metthods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book["isbn"] == isbn:
            books.pop(i)
            response = Response("", status=204)
            return response
        i += 1
    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number that was provided was not found,"
                 "so therfore unable "
    }
    response = Response(json(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response

app.run(port=5000)