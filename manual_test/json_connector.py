#!/usr/bin/env python

### Usage:
### ./json_connector.py [url] <[input_json] >[output_json]
###
### Example:
### ./json_connector.py http://localhost:8000/users/register/ < json_inputs/user_register.json

import sys
import json
import requests

lines = ""
try:
    while True:
        line = input()
        lines += line
except EOFError:
    pass

headers = {
    'Content-type': 'application/json',
}

response = requests.post(sys.argv[1], headers=headers, data=lines)
print(str(response.content, encoding='utf8'))
