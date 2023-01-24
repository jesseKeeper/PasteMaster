import os
import time
cmd = 'git pull'
os.system(cmd)
time.sleep(2)
# print('First time after power down:')

cmd = 'export FLASK_ENV=development'
os.system(cmd)
time.sleep(2)

cmd = 'export FLASK_APP=pasteMaster'
os.system(cmd)
time.sleep(2)

# print('export FLASK_ENV=development')
# print('export FLASK_APP=pasteMaster\n')

# print('sudo shutdown -h now\n')
# print('python run.py')

cmd = 'flask run --host=0.0.0.0'
os.system(cmd)