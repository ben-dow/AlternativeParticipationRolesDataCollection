import json
import random
import webbrowser

f = open("rawRepositories.txt", "r", encoding="utf-8")
repos = []

for line in f:
    repos.append(json.loads(line))

random.shuffle(repos)

eR = open("eligibleRepositories.txt", "a", encoding="utf-8")


for r in repos:
    webbrowser.open_new_tab(r['repo']['url'])
    response = input(r['repo']['url'] + "\nDoes this qualify? (y/n)")

    if response == "y":
        eR.write(json.dumps(r)+"\n")
        eR.flush()