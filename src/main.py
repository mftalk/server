from helpers import *
import json
import os

data = {}
def save_data():
    with open(CONFIG["paths"]["data"], "w") as file:
        json.dump(data, file)

if os.path.exists(CONFIG["paths"]["data"]):
    with open(CONFIG["paths"]["data"]) as file:
        data = json.load(file)
else:
    data = {
        "channels": {},
        "users": {}
    }
    save_data()
