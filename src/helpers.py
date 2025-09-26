import json

CONFIG_PATH = "data/config.json"

with open(CONFIG_PATH) as file:
    CONFIG = json.load(file)
