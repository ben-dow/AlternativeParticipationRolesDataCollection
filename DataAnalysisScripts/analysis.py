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

categoriesFile = open('activitycategories.csv', 'r', encoding="utf-8")
categoriesDictRaw = csv.DictReader(categoriesFile)


categoriesDict = {}
categoriesList = []

for c in categoriesDictRaw:
    if c['Activity Label'] not in categoriesDict.keys():
        categoriesDict[c['Activity Label'].lower()] = c['Category'].lower()
    if c['Category'].lower() not in categoriesList:
        categoriesList.append(c['Category'].lower())


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
                    if label in masterRepos[data[d]['id']]['labels']:
                        masterRepos[data[d]['id']]['labels'][label] = i['node']
# Analysis

#how to contribute section
reposWithHowToContributeSection = []
reposWithComprehensiveHowtoContributeSection = []
reposWithHowToContributeSectionForDevelopers = []
reposWithHowtoContributeSectionNeutral = []
reposWithoutHowToContributeSection = []


for repo in masterRepos:
    if "yes" in  masterRepos[repo]['Does the project contain a "How to Contribute" section?'].lower():

        if "comprehensive" in masterRepos[repo]['Does the project contain a "How to Contribute" section?'].lower():
            reposWithComprehensiveHowtoContributeSection.append(repo)
        elif "developer" in masterRepos[repo]['Does the project contain a "How to Contribute" section?'].lower() or "development" in masterRepos[repo]['Does the project contain a "How to Contribute" section?'].lower():
            reposWithHowToContributeSectionForDevelopers.append(repo)
        else:
            reposWithHowtoContributeSectionNeutral.append(repo)
        reposWithHowToContributeSection.append(repo)
    else:
        reposWithoutHowToContributeSection.append(repo)


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
reposWithParticipationInBugLabels = []

reposWithEnhancementRequestTag = []
reposWithParticipationInEnhancementLabels = []

reposWithDocumentationTag = []
reposWithParticipationInDocumentationLabels = []
reposWithLabel = []
for repo in masterRepos:
    labels = masterRepos[repo]['labels']
    repoName = masterRepos[repo]['name']
    for l in labels:
        label = l.lower()
        if "bug" in label:
            if repoName not in reposWithBugReportTag:
                reposWithBugReportTag.append(masterRepos[repo]['name'])

            if repoName not in reposWithParticipationInBugLabels:
                reposWithParticipationInBugLabels.append(repoName)
            if repoName not in reposWithLabel:
                reposWithLabel.append(repoName)

        if "enhancement" in label or "request" in label:
            if repoName not in reposWithEnhancementRequestTag:
                reposWithEnhancementRequestTag.append(masterRepos[repo]['name'])
            if repoName not in reposWithParticipationInEnhancementLabels:
                reposWithParticipationInEnhancementLabels.append(repoName)
            if repoName not in reposWithLabel:
                reposWithLabel.append(repoName)
        if "docs" in label or "documentation" in label or "doc" in label:
            if repoName not in reposWithDocumentationTag:
                reposWithDocumentationTag.append(masterRepos[repo]['name'])
            if repoName not in reposWithParticipationInDocumentationLabels:
                reposWithParticipationInDocumentationLabels.append(repoName)
            if repoName not in reposWithLabel:
                reposWithLabel.append(repoName)

numReposWithBugReportLabel = len(reposWithBugReportTag)
numReposWithParticipationInBugReportLabel = len(reposWithParticipationInBugLabels)
percentOfBugReportReposWithParticipation = (
                                                       numReposWithParticipationInBugReportLabel / numReposWithBugReportLabel) * 100

numReposWithEnhancementLabel = len(reposWithEnhancementRequestTag)
numReposWithParticipationInEnhancementLabel = len(reposWithParticipationInEnhancementLabels)
percentOfEnhancementReposWithParticipation = (numReposWithParticipationInEnhancementLabel / numReposWithEnhancementLabel) * 100

numReposWithDocsLabel = len(reposWithDocumentationTag)
numReposWithParticipationInDocsLabel = len(reposWithParticipationInDocumentationLabels)
percentOfDocsReposWithParticipation = (numReposWithParticipationInDocsLabel / numReposWithDocsLabel) * 100

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

# Participation Data

numOfReposWithSomeParticipationInTags = 0
reposWithoutParticipation = []
for repo in masterRepos:
    hasParticipation = False
    for label in masterRepos[repo]['labels']:
        if len(masterRepos[repo]['labels'][label]) > 0:
            numOfReposWithSomeParticipationInTags += 1
            hasParticipation = True
            break
    if not hasParticipation:
        reposWithoutParticipation.append(repo)

percentageOfReposWithParticipationInTags = (numOfReposWithSomeParticipationInTags / numOfRepositories) * 100

# Print Out

print("Number of Repos: " + str(numOfRepositories))
print("\nRepos with Activities Count " + str(reposWithActivitiesCount))
print("\tPercentage " + str(reposWithActivitiesPercentage))

print("\nNumber of Unique Activities Found: " + str(len(activityDict)))

print("Repositories with how to contribute section: " + str(len(reposWithHowToContributeSection)))

print("Repositories without how to contribute section: " + str(len(reposWithoutHowToContributeSection)))



activityData = {}

for a in activityDict:
    print("\n" + str(a))
    numReposWithActivity = len(activityDict[a])
    print("\tNumber of Repositories with Activity: " + str(numReposWithActivity))
    percentTotalReposWithActivity = (numReposWithActivity / numOfRepositories) * 100
    print("\tPercentage of Total Repositories with Activity: " + str(percentTotalReposWithActivity))
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

    percentInHowToContribute = (inHowToContribute / len(activityDict[a])) * 100
    print("\tPercentage of Repositories with activity formally defined in a how to contribute artifact: " + str(
        (inHowToContribute / len(activityDict[a]) * 100)))

    percentCallToAction = (inHowToContribute / len(activityDict[a])) * 100
    print("\tPercentage of repositories with a call to action for this activity: " + str(
        (inHowToContribute / len(activityDict[a]) * 100)))


    if a  in categoriesDict:
        activityData[a] = {
            'category' : categoriesDict[a],
            'numReposWithActivity': numReposWithActivity,
            'inHowToContribute': inHowToContribute,
            'callToAction': callToAction,
        }

print("\n\nCategory Data\n")

for c in categoriesList:

    reposWithActivity =  0
    reposWithActivityInHowToContribute = 0
    reposWithActivityCallToAction = 0


    for a in activityData:
        if activityData[a]['category'] == c:
            reposWithActivity += activityData[a]['numReposWithActivity']
            reposWithActivityInHowToContribute += activityData[a]['inHowToContribute']
            reposWithActivityCallToAction += activityData[a]['callToAction']

    print("\n" + str(c))
    print("\tNumber of Repositories with Activity: " + str(reposWithActivity))
    print("\tPercentage of Total Repositories with Activity: " + str(
        (reposWithActivity / numOfRepositories) * 100))
    print("\tPercentage of Repos with Acivities in How to Contribute: " + str(
        (reposWithActivityInHowToContribute / reposWithActivity) * 100))
    print("\tPercentage of Repos with Call to Action: " + str(
        (reposWithActivityCallToAction / reposWithActivity) * 100))





print("\n\nParticipation Data\n")

print("Number of Repos that Have Participation in their Alternative-Activity Labels: " + str(
    numOfReposWithSomeParticipationInTags))
print("Percentage of Repos that Have Participation in their Alternative-Activity Labels: " + str(
    percentageOfReposWithParticipationInTags))

print(
    "\nRepos with some variation of any of the following labels in the issue tracker [Enhancement/Request, "
    "Documentation, Bug Report]: " + str(
        numReposWithBugDocsOrEnhance))
print("\tPercentage: " + str(percentageReposWithBugDocsOrEnahance))

print("\nNumber of Repos with Enhancement Request Label: " + str(numReposWithEnhance))
print("\tPercentage of total repositories: " + str(percentageReposWithEnhance))
print("\tNumber of Repositories with Participation in Enhancement Requests: " + str(
    numReposWithParticipationInEnhancementLabel))
print(
    "\tPercentage of Repositories (that have an enhancement label) with Participation in Enhancement Requests: " + str(
        percentOfDocsReposWithParticipation))

print("\nNumber of Repos with Documentation Issue Label: " + str(numReposWithDoc))
print("\tPercentage of total repositories: " + str(percentageReposWithDoc))
print(
    "\tNumber of Repositories with Participation in documentation label: " + str(numReposWithParticipationInDocsLabel))
print(
    "\tPercentage of Repositories (that have a documentation label) with participation in enhancement requests: " + str(
        percentOfDocsReposWithParticipation))

print("\nNumber of Repos with Bug Report Label: " + str(numReposWithBug))
print("\tPercentage of total repositories: " + str(percentageReposWithBug))
print("\tNumber of repositories with participation in bug report label: " + str(
    numReposWithParticipationInBugReportLabel))
print("\tPercentage of repositories (that have a documentation label) with participation in bug report: " + str(
    percentOfBugReportReposWithParticipation))

print(str(len(reposWithLabel)) + " repositories with an alternative participation  label")