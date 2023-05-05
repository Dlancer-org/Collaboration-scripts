import requests
import os
import sys
import argparse
import base64

parser = argparse.ArgumentParser()
parser.add_argument('--pr-title', help='Taskid of the task submitted')
args = parser.parse_args()

pr_title = args.taskid
task_id = pr_title.split(';')[-1]

res = requests.get('http://localhost:5000/api/gh/task/' + task_id)
data = res.json()

test_dest_path = data['test_dest_path']
dep_installer = data['dep_installer']
test_dest_file_name = data['test_dest_file_name']
tests = data['open_tests'] + "\n" + data['hidden_tests']

os.chdir(test_dest_path)

if(os.path.isfile(test_dest_path)):
    test_file = open(test_dest_path, 'a')
    test_file.write("\n")
    test_file.write(tests)
    test_file.close()
else:
    try:
        test_file = open(os.path.join(test_dest_path, test_dest_file_name) , 'x')
    except:
        print("File with given name already exists")
        sys.exit(1)

    test_file.write(tests)
    test_file.close()

workflow_initial = requests.get('https://raw.githubusercontent.com/Dlancer-org/Collaboration-scripts/master/template.yml')
workflow_initial = workflow_initial.content
workflow_initial = workflow_initial.decode('utf-8')

workflow_initial_b64 = workflow_initial.encode('ascii')
workflow_initial_b64 = base64.b64encode(workflow_initial_b64)

workflow_current = open(os.path.join('.github','workflows','Dlancer-Integration.yml'), 'r').read()
workflow_current_b64 = workflow_current.encode('ascii')
workflow_current_b64 = base64.b64encode(workflow_current_b64)

if(workflow_initial_b64 != workflow_current_b64):
    print("Workflow file has been changed. Please update the workflow file to the initial state")
    sys.exit(1)

os.environ['DEP_INSTALL_CMD'] = dep_installer
os.environ['TEST_SUITE'] = tests
os.environ['TEST_RUNNER'] = data['test_runner'] # Add the template change detection logic here
os.environ['TEST_DEST_PATH'] = test_dest_path
os.environ['TASK_ID'] = task_id

cmd = 'echo -e "TEST_SUITE=$TEST_SUITE\nTEST_RUNNER=$TEST_RUNNER\nTEST_DEST_PATH=$TEST_DEST_PATH\nTASK_ID=$TASK_ID" >> $GITHUB_ENV'
os.system(cmd)