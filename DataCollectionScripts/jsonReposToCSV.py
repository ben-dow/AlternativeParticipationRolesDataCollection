import csv
import json

f = open("eligibleRepositories.txt", "r", encoding="utf-8")


keys = []
keysGot = False
repos = []
for r in f:
    repo = json.loads(r)
    repos.append(repo)
    if not keys:
        keys = repo['repo'].keys()
        keysGot = True

c = open('repos.csv', "w", newline='', encoding="utf-8")
csvwriter = csv.DictWriter(c, fieldnames=keys)
csvwriter.writeheader()

for r in repos:
    csvwriter.writerow(r['repo'])

