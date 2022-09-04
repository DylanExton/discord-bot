import datetime
import json
import os

with open('testJSON.json', 'r') as f:
    data = json.load(f)

    print(data['result'])