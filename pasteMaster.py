# 
# ttps://flask.palletsprojects.com/en/2.2.x/quickstart/#file-uploads

from flask import Flask, render_template
app = Flask(__name__)

if __name__ == '__main__':
   app.run()

@app.route('/index.html')
def home():
   return render_template('index.html')

@app.route('/start', methods=['GET'])
def index():
   # file = open(r'./src/pythonScript/test.py', 'r').read()
   # return render_template('start.html'), exec(file)
   return render_template('start.html')

# @app.route('/start.html', methods=['GET'])
# def index():
#    return render_template('start.html')


# @app.route('/run')
def run_script():
   # return db naam / file naam --> return foto + array
   return render_template('page_not_found.html')

@app.errorhandler(404)
def page_not_found(error):
   return render_template('page_not_found.html'), 404
