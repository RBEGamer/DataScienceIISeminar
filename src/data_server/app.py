import os.path
import os
from pathlib import Path
import logging

from flask import Flask, jsonify, Response, redirect

APP_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_DATA_PATH = os.path.join(APP_PATH,'data/')
logging.info(STATIC_DATA_PATH)
print(STATIC_DATA_PATH)
app = Flask(__name__, static_folder=STATIC_DATA_PATH, static_url_path='/static')


app.config.from_object(__name__)





@app.route('/')
def index():
	return redirect('/files')

# LIST FILES
@app.route('/files')
def files():
	files = [f for f in os.listdir(STATIC_DATA_PATH)]
	print(files)
	return jsonify({'files': files})

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=3017)