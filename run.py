import os
print('First time after power down:')

print('export FLASK_ENV=development')
print('export FLASK_APP=pasteMaster\n')

print('sudo shutdown -h now\n')
print('python run.py')

cmd = 'flask run --host=0.0.0.0'
os.system(cmd)
