from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
import json
import functions


app = Flask(__name__)

cors = CORS(app)
# cors = CORS(app, resources={r"/subscribe": {"origins": ["https://list-links"]}})

@app.route('/')
def hello():
    return 'Hi there!'

@app.route('/get-hOCR/<url>', methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def get_hocr(url):
    image_url = get_image_url(input_url)
    soup = get_hOCR(image_url)
    
    return jsonify(output)