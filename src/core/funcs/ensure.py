from flask import jsonify, Response
from typing import Any, Literal

def ensure_args(d: dict[Any, Any], keys: list[str]) -> (tuple[Response, Literal[400]] | None):
    """
    Returns a Response error if a key is not present in the dictionary.
    
    :param d: The dictionary to check.
    :type d: dict[Any, Any]
    :param keys: A list of keys to check.
    :type keys: list[str]
    :return: An error Response if a key is missing, else None
    :rtype: tuple[Response, Literal[400]] | None
    """
    for key in keys:
        if not key in d:
            return jsonify({
                "success": False,
                "message": f"{key} is a required argument",
            }), 400
        
    return None