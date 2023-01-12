import os
cmd = 'git pull'
os.system(cmd)
print('First time after power down:')

print('export FLASK_ENV=development')
print('export FLASK_APP=pasteMaster\n')

print('sudo shutdown -h now\n')
print('python run.py')

cmd = 'flask run --host=0.0.0.0'
os.system(cmd)