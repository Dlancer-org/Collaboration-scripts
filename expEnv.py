import requests
import os
import sys
import argparse
import base64

parser = argparse.ArgumentParser()
parser.add_argument('--prTitle', help='Taskid of the task submitted')
args = parser.parse_args()

host = os.environ['HOST']

pr_title = args.prTitle
split_title = pr_title.split(';')
task_id = split_title[-1]
print(host)
res = requests.get(f'{host}/api/gh/task/{task_id}')
data = res.json()
print(res)

test_dest_path = data['test_dest_path']
dep_installer = data['dep_installer']
test_dest_file_name = data['test_dest_file_name']

# workflow_initial = requests.get('https://raw.githubusercontent.com/Dlancer-org/Collaboration-scripts/master/template.yml')
# workflow_initial = workflow_initial.content
# workflow_initial = workflow_initial.decode('utf-8')

# workflow_initial_b64 = workflow_initial.encode('ascii')
# workflow_initial_b64 = base64.b64encode(workflow_initial_b64)

# workflow_current = open(os.path.join('.github','workflows','Dlancer-Integration.yml'), 'r').read()
# workflow_current_b64 = workflow_current.encode('ascii')
# workflow_current_b64 = base64.b64encode(workflow_current_b64)

# if(workflow_initial_b64 != workflow_current_b64):
#     print("Workflow file has been changed. Please update the workflow file to the initial state")
#     sys.exit(1)

with open(os.path.join('.', 'dep_ins.sh') , 'w') as dep:
    dep.write('#!/bin/bash\n')
    dep.write(str(data["dep_installer"]))

with open(os.path.join('.', 'test.sh') , 'w') as test:
    test.write('#!/bin/bash\n')
    test.write(str(data["test_runner"]) + " " + test_dest_path + test_dest_file_name)                    

with open(os.path.join(test_dest_path, test_dest_file_name) , 'w') as test_file:
    test_file.write(data['open_tests'] + "\n")
    test_file.write(data['hidden_tests'])

os.environ["PR_TITLE"] = ''.join(split_title[:-1])
os.environ["TASK_ID"] = task_id

try:
    cmd = 'echo "TASK_ID=$TASK_ID\nPR_TITLE=$PR_TITLE\n" >> $GITHUB_ENV'
    os.system(cmd)
except:
    print("Error while exporting environment variables")
    sys.exit(1)
