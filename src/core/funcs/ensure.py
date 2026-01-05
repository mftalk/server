from flask import jsonify
from typing import Any

def ensure_args(d: dict[Any, Any], keys: list[str]):
    """Returns a Response error if a key is not present in the dictionary.

    Args:
        d (dict): The dictionary to check.
        keys (list[str]): A list of keys to check.

    Returns:
        Response | None: An error Response if a key is missing, else None
    """
    for key in keys:
        if not key in d:
            return jsonify({
                "success": False,
                "message": f"{key} is a required argument",
            }), 400
        
    return None