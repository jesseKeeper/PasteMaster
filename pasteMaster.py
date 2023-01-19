# ttps://flask.palletsprojects.com/en/2.2.x/quickstart/#file-uploads
import json
from flask import Flask, render_template, send_file
app = Flask(__name__)

if __name__ == '__main__':
   app.run()

@app.route('/')
def homes():
   return render_template('index.html')

@app.route('/start', methods=['GET'])
def index():
   # file = open(r'./src/pythonScript/photo.py', 'r').read()
   # return render_template('start.html'), exec(file)
   return render_template('start.html')

@app.route('/pcb')
def get_image():
   filename = 'static/image/view.jpg'
   return send_file(filename, mimetype='image/jpg')

@app.route('/array')
def get_array():
   detections = [[[32,12],[72, 11],[74, 66],[34, 68]], [[124,   9],[164,   7],[166,  62],[126,  64]], [[170, 307],[207, 307],[207, 355],[170, 355]]]

   dict = {
    "detections": detections
   }
   detections_json = json.dumps(detections)

   print(detections_json)
   # filename = 'static/text/test.txt'
   return send_file(detections_json, mimetype='application/json')

@app.errorhandler(404)
def page_not_found(error):
   return render_template('page_not_found.html'), 404

