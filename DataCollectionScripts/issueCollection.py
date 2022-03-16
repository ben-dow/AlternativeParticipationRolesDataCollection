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


queryFile = open("issueRequest.graphql", "r")
queryData = queryFile.read()
queryFile.close()

# Date Setup
today = datetime.datetime.today()
start = today - datetime.timedelta(days=START_DELTA)

reposFile = open("eligibleRepositories.txt")
repoData = []

for r in reposFile:
    repoData.append(json.loads(r))

labelsFile = open("labels.csv", encoding="utf-8")
labelData = {}

csvReader = csv.DictReader(labelsFile)
for row in csvReader:
    label = row['labelName']

    if "bug" in label or "docs" in label or "documentation" in label or "doc" in label or "enhancement" in label or "request" in label:

        if row['resourcePath'] not in labelData:
            labelData[row['resourcePath']]  = []


        labelData[row['resourcePath']].append( row['labelName'])

requestQueries = []

request = ""
letters = string.ascii_uppercase
queryCount = 0
for r in repoData:
    resourcePath = r['repo']['resourcePath']
    owner, name = resourcePath.split('/')[1:]

    if resourcePath in labelData:
        for l in labelData[resourcePath]:

            query = copy.copy(queryData)
            query = query.replace("${owner}", owner)
            query = query.replace("${name}", name)
            query = query.replace("${label}", l)

            request += ''.join(random.choice(letters) for i in range(10)) + ":" + query
            queryCount += 1

            if queryCount == 2:
                request = "{ \n" + request + "}"
                requestQueries.append(request)
                request = ""
                queryCount = 0

request = "{ \n" + request + "}"
requestQueries.append(request)
request = ""
queryCount = 0

print(len(requestQueries))
for q in requestQueries:
    print("Making Request")
    r = requests.post(requestURL, data=json.dumps({"query": q}), headers=headersAuth1)
    j = json.loads(r.content)
    print(r.content)
    data = j["data"]

    dataFile = open("issueDataReturn.txt", "a")
    dataFile.write("\n" + json.dumps(data))
