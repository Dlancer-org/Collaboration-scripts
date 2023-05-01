import requests
import os
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--pr-title', help='Taskid of the task submitted')
args = parser.parse_args()

pr_title = args.taskid
task_id = pr_title.split(';')[-1]

res = requests.get('http://localhost:5000/taskTrackingInfo/' + task_id)
data = res.json()

test_dest_path = data['test_dest_path']
test_dest_file_name = data['test_dest_file_name']
tests = data['test_cases']

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
        print("File with given already exists")
        sys.exit(1)

    test_file.write(tests)
    test_file.close()

os.environ['TEST_SUITE'] = data['test_cases']
os.environ['TEST_RUNNER'] = data['test_runner']
os.environ['TEST_DEST_PATH'] = test_dest_path
os.environ['TASK_ID'] = task_id

cmd = 'echo -e "TEST_SUITE=$TEST_SUITE\nTEST_RUNNER=$TEST_RUNNER\nTEST_DEST_PATH=$TEST_DEST_PATH\nTASK_ID=$TASK_ID" >> $GITHUB_ENV'
os.system(cmd)