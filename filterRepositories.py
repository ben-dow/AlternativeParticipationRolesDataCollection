import json
import datetime
import queue
import threading
from threading import Thread
from time import sleep

import requests

### Config Variables ###
from util import keys_exists

START_DELTA = 40
REPO_FETCH_MAX_THREADS = 1

f = open("tokens.json")
data = json.load(f)

requestURL = "https://api.github.com/repos"
headersAuth1 = {"Authorization": "Bearer " + data[0]}
headersAuth2 = {"Authorization": "Bearer " + data[1]}

headers = [headersAuth1, headersAuth2]

f = open("rawRepositories.txt", "r", encoding="utf-8")
repos = []

for line in f:
    repos.append(json.loads(line))


r = requests.get(requestURL+repos[0]['repo']['resourcePath'], headers=headers[0])

print(r.content)

#request = json.loads(r.content)
#print(json.dumps(request, indent=4, sort_keys=True))
