import os
cmd = 'git pull'
os.system(cmd)

print('export FLASK_ENV=development')
print('export FLASK_APP=pasteMaster')

cmd = 'flask run --host=0.0.0.0'
os.system(cmd)