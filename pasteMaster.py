from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')
if __name__ == '__main__':
   app.run()

@app.route('/start.html', methods=['GET'])
def index():
   return render_template('start.html')

# @app.route('/start.html', methods=['GET'])
# def index():
#    return render_template('start.html')

@app.route('/run.html')
def run_script():
   file = open(r'./src/pythonScript/detect.py', 'r').read()
   return exec(file)

@app.errorhandler(404)
def page_not_found(error):
   return render_template('index.html'), 404
