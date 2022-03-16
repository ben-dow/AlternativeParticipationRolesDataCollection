import csv
import json

activitiesFile = open('activities.csv', 'r', encoding="utf-8")
activitiesDict = csv.DictReader(activitiesFile)

labelsFile = open('labels.csv', 'r', encoding="utf-8")
labelsDict = csv.DictReader(labelsFile)

reposFile = open('repos.csv', 'r', encoding="utf-8")
reposDict = csv.DictReader(reposFile)

issuesFile = open('issueDataReturn.txt', 'r', encoding="utf-8")
# Combine into one entry for each repository

masterRepos = {}

for r in reposDict:
    masterRepos[r['id']] = r
    masterRepos[r['id']]['labels'] = {}
    masterRepos[r['id']]['activities'] = []

for r in labelsDict:
    if (r['id'] in masterRepos):
        masterRepos[r["id"]]['labels'][r['labelName']] = []

for activity in activitiesDict:
    added = False
    for repo in masterRepos:
        if (masterRepos[repo]['name'] == activity['Project']):
            masterRepos[repo]['activities'].append(activity)
            added = True
            break
    if added == False:
        print(activity['Project'])

for line in issuesFile:
    data = json.loads(line)
    for d in data:
        if data[d]['id'] in masterRepos:
            for i in data[d]['issues']['edges']:
                for l in i['node']['labels']['edges']:
                    label = l['node']['name']
                    if label in masterRepos[ data[d]['id']]['labels']:
                       masterRepos[ data[d]['id']]['labels'][label] = i['node']
# Analysis

# Number of Repositories
numOfRepositories = len(masterRepos)

# Repositories with some concept of alternative-participation activities
reposWithActivitiesCount = 0
for repo in masterRepos:
    activities = masterRepos[repo]['activities']
    if len(activities) > 0:
        reposWithActivitiesCount += 1
reposWithActivitiesPercentage = (reposWithActivitiesCount / numOfRepositories) * 100

# Repos with tags that represent alternative-participation activities
reposWithBugReportTag = []
reposWithEnhancementRequestTag = []
reposWithDocumentationTag = []

for repo in masterRepos:
    labels = masterRepos[repo]['labels']
    for l in labels:
        label = l.lower()
        if "bug" in label:
            if masterRepos[repo]['name'] not in reposWithBugReportTag:
                reposWithBugReportTag.append(masterRepos[repo]['name'])

        if "enhancement" in label or "request" in label:
            if masterRepos[repo]['name'] not in reposWithEnhancementRequestTag:
                reposWithEnhancementRequestTag.append(masterRepos[repo]['name'])

        if "docs" in label or "documentation" in label or "doc" in label:
            if masterRepos[repo]['name'] not in reposWithDocumentationTag:
                reposWithDocumentationTag.append(masterRepos[repo]['name'])

reposWithBugDocsEnhance = list(set(reposWithEnhancementRequestTag) | set(reposWithBugReportTag))
reposWithBugDocsEnhance = list(set(reposWithBugDocsEnhance) | set(reposWithDocumentationTag))

numReposWithBugDocsOrEnhance = len(reposWithBugDocsEnhance)
percentageReposWithBugDocsOrEnahance = (numReposWithBugDocsOrEnhance / numOfRepositories) * 100

numReposWithBug = len(reposWithBugReportTag)
percentageReposWithBug = (numReposWithBug / numOfRepositories) * 100
numReposWithEnhance = len(reposWithEnhancementRequestTag)
percentageReposWithEnhance = (numReposWithEnhance / numOfRepositories) * 100
numReposWithDoc = len(reposWithDocumentationTag)
percentageReposWithDoc = (numReposWithDoc / numOfRepositories) * 100

# Activities Identified

activityDict = {}

for repo in masterRepos:
    activities = masterRepos[repo]['activities']
    for a in activities:
        key = a['Activity Label'].lower()

        if key not in activityDict:
            activityDict[key] = []
        activityDict[key].append(a)

# Print Out

print("Number of Repos: " + str(numOfRepositories))
print("\nRepos with Activities Count " + str(reposWithActivitiesCount))
print("\tPercentage " + str(reposWithActivitiesPercentage))

print(
    "\nRepos with some variation of any of the following labels in the issue tracker [Enhancement/Request, "
    "Documentation, Bug Report]: " + str(
        numReposWithBugDocsOrEnhance))
print("\tPercentage: " + str(percentageReposWithBugDocsOrEnahance))

print("\nNumber of Repos with Enhancement Request Label: " + str(numReposWithEnhance))
print("\tPercentage: " + str(percentageReposWithEnhance))

print("\nNumber of Repos with Documentation Issue Label: " + str(numReposWithDoc))
print("\tPercentage: " + str(percentageReposWithDoc))

print("\nNumber of Repos with Bug Report Label: " + str(numReposWithBug))
print("\tPercentage: " + str(percentageReposWithBug))

print("\nNumber of Unique Activities Found: " + str(len(activityDict)))

for a in activityDict:
    print("\n" + str(a))
    print("\tNumber of Repositories with Activity: " + str(len(activityDict[a])))
    print("\tPercentage of Total Repositories with Activity: " + str((len(activityDict[a]) / numOfRepositories) * 100))
    print("\tPercentage of Repos w/ Activities with this Activity: " + str(
        (len(activityDict[a]) / len(activityDict)) * 100))

    inHowToContribute = 0
    callToAction = 0
    for e in activityDict[a]:

        yesOrNoCallToAction = e[' Does this activity have a formal "call to action?"'].lower()
        if "yes" in yesOrNoCallToAction:
            callToAction += 1

        yesOrNoContrib = e['Is this activity defined in a "How to Contribute" artifact?'].lower()
        if "yes" in yesOrNoContrib.lower():
            inHowToContribute += 1

    print("\tPercentage of Repositories with activity formally defined in a how to contribute artifact: " + str(
        (inHowToContribute / len(activityDict[a]) * 100)))

    print("\tPercentage of repositories with a call to action for this activity: " + str(
        (inHowToContribute / len(activityDict[a]) * 100)))

print("\n\nParticipation Data")