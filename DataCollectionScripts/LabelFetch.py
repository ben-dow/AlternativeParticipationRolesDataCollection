import copy
import csv
import json
import datetime
import queue
import string
import threading
import random
from threading import Thread
from time import sleep

import requests

### Config Variables ###
from util import keys_exists

START_DELTA = 40
REPO_FETCH_MAX_THREADS = 1

f = open("tokens.json")
data = json.load(f)

requestURL = "https://api.github.com/graphql"
headersAuth1 = {"Authorization": "Bearer " + data[0]}
headersAuth2 = {"Authorization": "Bearer " + data[1]}

headers = [headersAuth1, headersAuth2]


queryFile = open("labelRequest.graphql", "r")
queryData = queryFile.read()
queryFile.close()

# Date Setup
today = datetime.datetime.today()
start = today - datetime.timedelta(days=START_DELTA)

reposFile = open("eligibleRepositories.txt")
repoData = []

for r in reposFile:
    repoData.append(json.loads(r))

request = ""
letters = string.ascii_uppercase

for r in repoData:
    owner, name = r['repo']['resourcePath'].split('/')[1:]

    query = copy.copy(queryData)
    query = query.replace("${owner}", owner)
    query = query.replace("${name}", name)

    request += ''.join(random.choice(letters) for i in range(10)) + ":" + query

request = "{ \n" + request + "}"

r = requests.post(requestURL, data=json.dumps({"query": request}), headers=headersAuth1)
j = json.loads(r.content)
data = j["data"]

labelData = []

for d in data:
    repo = data[d]
    for l in repo['labels']['nodes']:
        name = l["name"]

        labelData.append([repo["id"], repo["name"], repo["resourcePath"], name])




with open('labels.csv', 'w', encoding="utf-8", newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["id", "repoName", "resourcePath", "labelName"])

    csvwriter.writerows(labelData)