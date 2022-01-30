import json
import datetime
import queue
import threading
from threading import Thread
from time import sleep

import requests

### Config Variables ###
from util import keys_exists

START_DELTA = 30
REPO_FETCH_MAX_THREADS = 1

f = open("tokens.json")
data = json.load(f)

requestURL = "https://api.github.com/graphql"
headersAuth1 = {"Authorization": "Bearer " + data[0]}
headersAuth2 = {"Authorization": "Bearer " + data[1]}

headers = [headersAuth1, headersAuth2]


queryFile = open("repositoryQuery.graphql", "r")
queryData = queryFile.read()
queryFile.close()

# Date Setup
today = datetime.datetime.today()
start = today - datetime.timedelta(days=START_DELTA)

cursor = start
incrementDelta = datetime.timedelta(days=1)
print("Today: " + today.strftime('%Y-%m-%d'))
print("Start: " + start.strftime('%Y-%m-%d'))

days = queue.Queue()
contribCheck = queue.Queue()

while cursor <= today:
    days.put(cursor.strftime('%Y-%m-%d'))
    cursor += incrementDelta


def GithubGraphQLQuery(q, header):
    while q.empty() is False:
        date = q.get()
        repos = []
        qD = queryData.replace("${DATE}", date).replace("${AFTER}", "")

        r = requests.post(requestURL, data=json.dumps({"query": qD}), headers=header)
        j = json.loads(r.content)
        repos = repos + j.get("data").get("search").get("repos")

        while keys_exists(j, "data", "search", "pageInfo", "hasNextPage") and j.get('data').get("search").get("pageInfo").get("hasNextPage"):
            qD = queryData.replace("${DATE}", date).replace("${AFTER}", "after: \"" + j.get('data').get("search").get("pageInfo").get("endCursor") + "\" ")
            r = requests.post(requestURL, data=json.dumps({"query": qD}), headers=header)
            j = json.loads(r.content)
            print(j)
            sleep(1)

        repF = open("repositories.txt", "a", encoding="utf-8")
        for r in repos:
            repF.write(str(r) + "\n")
        sleep(1)


for i in range(len(headers)):
    worker = Thread(target=GithubGraphQLQuery, args=(days,headers[i],))
    worker.start()


#request = json.loads(r.content)
#print(json.dumps(request, indent=4, sort_keys=True))
