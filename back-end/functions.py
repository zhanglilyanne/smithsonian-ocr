import requests
import shutil
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
import io
from PIL import Image
import os
import sys

import pytesseract
from pytesseract import image_to_pdf_or_hocr
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_image_url(input_url):
    try:
        r = requests.get(input_url)
        soup = BeautifulSoup(r.text)

        if 'project phaedra' in soup.text.lower().strip():
            pid = soup.find('div', {'id': 'transcription-asset-wrapper'})['data-idsid']
        else:
            pid = input_url.split('/')[-1]

        image_url = 'https://ids.si.edu/ids/deliveryService?max_w=2000&id=' + pid
        return image_url
    except Exception as e:
        print(e)
        return None

def get_hOCR(image_url):
    
    # load the image over requests
    response = requests.get(image_url, stream=True)
    img = Image.open(io.BytesIO(response.content))

    # get the hocr & parse. replace the image in the current text with the image_url
    hocr_output = image_to_pdf_or_hocr(img, extension='hocr')
    hocr = hocr_output.decode('utf-8')
    soup = BeautifulSoup(hocr, parser='xml')
    soup = BeautifulSoup(re.sub(r'image \"(.+?)\"', 'image ' + '"' + image_url + '"', str(soup)))
    return soup