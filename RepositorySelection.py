import json
import random

f = open("rawRepositories.txt", "r", encoding="utf-8")
repos = []

for line in f:
    repos.append(json.loads(line))

randomNums = []
for i in range(0, 50):
    randomNum = random.randint(0, len(repos) - 1)

    while randomNum  in randomNums:
        print('here')
        randomNum = random.randint(0, len(repos) - 1)

    randomNums.append(randomNum)


for i in randomNums:
    print(repos[i])