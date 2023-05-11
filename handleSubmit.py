# To submit : repoName, repoOwner, taskid, prAuthor, prNum, prTitle, prDescription
import requests
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--prAuthor', help='Github username of the Pull request author')    # ${{ github.event.pull_request.user.login }}
parser.add_argument('--prNum', help='Number attached to the pull request')              # ${{ github.event.pull_request.number }}
parser.add_argument('--prDescription', help='Title of the pull request')                # ${{ github.event.pull_request.body }}
parser.add_argument('--repoDetails')                                                    # ${{ github.repository }}

args = parser.parse_args()
host = os.environ['HOST']

prAuthor = args.prAuthor
prNum = args.prNum
prDescription = args.prDescription
repoDetails = args.repoDetails

# prAuthor = os.environ['prAuthor']
# prNum = os.environ['prNum']
# prDescription = os.environ['prDescription']
# repoDetails = os.environ['repoDetails']

repoName = repoDetails.split('/')[1]
repoOwner = repoDetails.split('/')[0]

response = requests.post(f'{host}/api/gh/task', json={
    'repoName': repoName,
    'repoOwner': repoOwner,
    'taskid': os.environ['TASK_ID'],
    'prAuthor': prAuthor,
    'prNum': prNum,
    'prTitle': os.environ['PR_TITLE'],
    'prDescription': prDescription
})

try:
    response.raise_for_status()
    print("Task completed successfully")
except requests.exceptions.HTTPError as err:
    print("Task submission failed, check server logs", err)   
    sys.exit(1)