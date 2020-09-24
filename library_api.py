"""
This python file contains a RESTful API for the catalog_manager
"""
# ACIT 2515 - Assignment 2
# library_api.py
# Group 19


from flask import jsonify, make_response, Flask, request
from catalog_manager import CatalogManager
import json

app = Flask(__name__)

catalog_manager = CatalogManager("BC Library")


@app.route("/catalogmanager/catalog", methods=["POST"])
def create_item():
    """ Create an item using POSTed json """
    content = json.loads(request.data.decode())
    try:
        catalog_manager.add_item_from_json(content)
    except ValueError as err:
        print(err)
        return make_response(f"{err}", 400)
    except:
        return make_response("Item is in invalid format, no item created.", 400)
    return make_response(f"{content['isbn']}", 200)


@app.route("/catalogmanager/catalog/<int:isbn>", methods=["PUT", "DELETE", "GET"])
def get_put_delete_item(isbn):
    """ Get/ Delete/ Borrow/ Return an item from the catalog if item with that isbn exist """
    item = catalog_manager.get_item_by_isbn(isbn)
    if item is None:
        return make_response(f"Item with isbn: {isbn} not found.", 404)
    if request.method == "PUT":
        content = json.loads(request.data.decode())
        try:
            if content["operation"] == "return":
                try:
                    item.return_item()
                except RuntimeError as err:
                    return make_response(f"{err}", 400)
                return make_response("OK", 200)
            elif content["operation"] == "borrow":
                try:
                    item.borrow(content["date"])
                except Exception as err:
                    return make_response(f"{err}", 400)
                return make_response("OK", 200)
            else:
                return make_response("Invalid Operation Specified", 400)
        except KeyError:
            return make_response("Operation not specified", 400)
    elif request.method == "GET":
        return make_response(jsonify(item.to_dict()), 200)
    elif request.method == "DELETE":
        try:
            catalog_manager.delete_item_by_isbn(isbn)
            return make_response("OK", 200)
        except Exception as err:
            return make_response(f"{err}", 400)


@app.route("/catalogmanager/catalog/all", methods=["GET"])
def get_all_item():
    """ Return all item in the catalog manager """
    return make_response(jsonify(catalog_manager.to_dict()), 200)


@app.route("/catalogmanager/catalog/all/<string:type_>", methods=["GET"])
def get_all_item_by(type_):
    """ Return all item with a type of either 'multimedia' || 'book' """
    if type_ not in ("multimedia", "books"):
        return make_response(f"Type: {type_} not supported.", 400)
    items = catalog_manager.get_items_by_type(type_)
    items = [item.to_dict() for item in items]
    return make_response(jsonify(items), 200)


@app.route("/catalogmanager/catalog/stats", methods=["GET"])
def get_stats():
    """ Return the stats of the catalog manager """
    stats = catalog_manager.get_stats()
    return make_response(jsonify(stats.to_dict()), 200)


if __name__ == "__main__":
    app.run(debug=True)
