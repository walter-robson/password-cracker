#!/usr/bin/env python3
import requests
import json

# Constants

URL = 'http://catalog.cse.nd.edu:9097/query.json'

# TODO: Make a HTTP request to URL
response = requests.get(URL)

# TODO: Access json representation from response object
data = response.json()

# TODO: Display all machine names with type "wq_factory"
for row in data:
    if row['type'] == 'wq_factory':
        print(row['name'])
