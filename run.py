import os
cmd = 'git pull'
os.system(cmd)

cmd = 'export FLASK_ENV=development'
os.system(cmd)

cmd = 'export FLASK_APP=pasteMaster'
os.system(cmd)

cmd = 'flask run --host=0.0.0.0'
os.system(cmd)