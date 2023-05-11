import requests
import os

host = os.environ['HOST']

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--prNum', help='Number attached to the pull request')              # ${{ github.event.pull_request.number }}
parser.add_argument('--repoDetails')                                                    # ${{ github.repository }}
parser.add_argument('--step')
args = parser.parse_args()

prNum = args.prNum
repoDetails = args.repoDetails
step = args.step
taskid = os.environ['TASK_ID']

repoName = repoDetails.split('/')[1]
repoOwner = repoDetails.split('/')[0]

response = requests.patch(f'{host}/api/gh/task/{taskid}', json={
    'repoName': repoName,
    'repoOwner': repoOwner,
    'prNum': prNum
})

try:
    response.raise_for_status()
    if step == 1:
        print("Dependencies can't be installed, contact project owner")
    elif step == 2:
        print("Tests failed due to Incorrect runner cmd or Incorrect code, Please handle accordingly")
    print("Pull Request Closed")

except requests.exceptions.HTTPError as err:
    print("Pull request couln't be closed", err)   

sys.exit(1)