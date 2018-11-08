#!/usr/bin/env python3

import json
import hashlib
import jsonpointer
from flask import jsonify
from flask import Flask, Response, request, g, current_app
import werkzeug.exceptions

app = Flask(__name__)

CONFIG = {"network": {"nics": {"eth0": {"addresses": ["192.168.122.1/24", "192.168.122.5/24"]}}}}

def jsonify_meta(body, meta):
    if request.args.get("require_meta") == "yes":
        return jsonify(body=body, meta=meta)
    else:
        return jsonify(body)

def json_hash(doc, algo="sha1"):
    hash = hashlib.new(algo)
    hash.update(json.dumps(doc, sort_keys=True).encode("utf-8"))

    return hash.hexdigest()


class Database:
    def __init__(self, default=None):
        if default is None:
            default = {}

        self.data = default

    def query(self, pointer: str, default=jsonpointer._nothing): # pylint: disable=W0212

        if not pointer.startswith("/"):
            pointer = "/" + pointer
        return jsonpointer.resolve_pointer(self.data, pointer, default=default)

    def update(self, pointer: str, value):
        if not pointer.startswith("/"):
            pointer = "/" + pointer
        jsonpointer.set_pointer(self.data, pointer, value, inplace=True)


@app.route("/config/<path:pointer>", methods=["GET"])
def query(pointer):
    meta = {"pointer": pointer}
    db = current_app.config["DATABASE"]
    try:
        result = db.query(pointer)
    except jsonpointer.JsonPointerException as error:
        return jsonify(error=str(error), meta=meta), 404

    meta["etag"] = etag = json_hash(result)
    g.etag = etag
    return jsonify_meta(body=result, meta=meta)


@app.route("/config/<path:pointer>", methods=["PUT"])
def update(pointer):
    request_json = request.get_json()
    meta = {"pointer": pointer}
    db = current_app.config["DATABASE"]
    try:
        query_result = db.query(pointer)
        etag = json_hash(query_result)
    except jsonpointer.JsonPointerException as error:
        return jsonify(error=str(error), meta=meta), 404

    request_etag = request_json.get("meta", {}).get("etag")
    if request_etag is None:
        return jsonify({"error": "Etag missing from request"}), 400
    if etag != request_etag.strip('"'):
        return jsonify({"error": "Etag mismatch"}), 400

    db.update(pointer, request_json["body"])

    return query(pointer)


@app.route("/config/<path:pointer>", methods=["POST"])
def create(pointer):
    request_json = request.get_json()
    meta = {"pointer": pointer}
    db = current_app.config["DATABASE"]

    try:
        db.query(pointer)
    except jsonpointer.JsonPointerException:
        pass
    else:
        return jsonify(error="Object already exists", meta=meta), 400

    try:
        db.update(pointer, request_json)
    except jsonpointer.JsonPointerException as error:
        return jsonify(error=str(error), meta=meta), 400
    return query(pointer)


@app.route("/info")
def info():
    if "counter" in g:
        g.counter = g.counter + 1
    else:
        g.counter = 0
    return jsonify(g.counter)

@app.errorhandler(jsonpointer.JsonPointerException)
def handle_json_pointer_exception(error):
    return jsonify(error=str(error)), 400


def errors_to_json(error: werkzeug.exceptions.HTTPException):
    return jsonify(error=str(error.description)), error.code

def register_error_handlers():
    for class_name in dir(werkzeug.exceptions):
        klass = getattr(werkzeug.exceptions, class_name)
        try:
            if issubclass(klass, werkzeug.exceptions.HTTPException):
                app.register_error_handler(klass, errors_to_json)
        except TypeError:
            pass

@app.after_request
def add_headers(response: Response):
    if "etag" in g:
        response.set_etag(g.etag)
    return response

register_error_handlers()

if __name__ == "__main__":
    app.config["DATABASE"] = Database(CONFIG)
    app.run()
