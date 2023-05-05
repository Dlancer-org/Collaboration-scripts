# To submit : repoName, repoOwner, taskid, prAuthor, prNum, prTitle, prDescription, tests, testDestPath, testDestFileName
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

repoName = args.repoDetails.split('/')[1]
repoOwner = args.repoDetails.split('/')[0]

response = requests.post('http://localhost:5000/api/gh/task', json={
    'repoName': repoName,
    'repoOwner': repoOwner,
    'taskid': os.environ['TASK_ID'],
    'prAuthor': args.prAuthor,
    'prNum': args.prNum,
    'prTitle': os.environ['PR_TITLE'],
    'prDescription': args.prDescription,
    'tests': os.environ['TEST_SUITE'],
    'testDestPath': os.environ['TEST_DEST_PATH'],
    'testDestFileName': os.environ['TEST_DEST_FILE_NAME']
})

if(response.status_code == 200):
    print("Task submitted successfully")
    sys.exit(0)
else:
    print("Task submission failed")
    sys.exit(1)