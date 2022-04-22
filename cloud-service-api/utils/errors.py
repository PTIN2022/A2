from flask import jsonify


def malformed_error():
    return {"error": "Malformed request syntax."}
