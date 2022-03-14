import csv

activitiesFile = open('activities.csv', 'r', encoding="utf-8")
activitiesDict = csv.DictReader(activitiesFile)

labelsFile = open('labels.csv', 'r', encoding="utf-8")
labelsDict = csv.DictReader(labelsFile)

reposFile = open('repos.csv', 'r', encoding="utf-8")
reposDict = csv.DictReader(reposFile)

# Combine into one entry for each repository

masterRepos = {}

for r in reposDict:
    masterRepos[r['id']] = r
    masterRepos[r['id']]['labels'] = []
    masterRepos[r['id']]['activities'] = []

for r in labelsDict:
    if (r['id'] in masterRepos):
        masterRepos[r["id"]]['labels'].append(r['labelName'])

for activity in activitiesDict:
    added = False
    for repo in masterRepos:
        if (masterRepos[repo]['name'] == activity['Project']):
            masterRepos[repo]['activities'].append(activity)
            added = True
            break
    if added == False:
        print(activity['Project'])

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





# Print Out

print("Number of Repos: " + str(numOfRepositories))
print("\nRepos with Activities Count " + str(reposWithActivitiesCount))
print("\tPercentage " + str(reposWithActivitiesPercentage))

print("\nRepos with some variation of any of the following labels in the issue tracker [Enhancement/Request, Documentation, Bug Report]: " + str(numReposWithBugDocsOrEnhance))
print("\tPercentage: " + str(percentageReposWithBugDocsOrEnahance))

print("\nNumber of Repos with Enhancement Request Label: " + str(numReposWithEnhance))
print("\tPercentage: " + str(percentageReposWithEnhance))

print("\nNumber of Repos with Documentation Issue Label: " + str(numReposWithDoc))
print("\tPercentage: " + str(percentageReposWithDoc))

print("\nNumber of Repos with Bug Report Label: " + str(numReposWithBug))
print("\tPercentage: " + str(percentageReposWithBug))
