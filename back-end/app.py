from flask import Flask, jsonify, request, Response
import json
import functions

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hi there!'

@app.route('/get-hOCR/<url>', methods=['GET'])
def get_hocr(url):
    image_url = functions.get_image_url(url)
    if image_url is None:
        return 'Not Valid'	
    hocr = functions.get_hOCR(image_url)
    
    return str(hocr)
if __name__ == "__main__":
    app.run(host='0.0.0.0')