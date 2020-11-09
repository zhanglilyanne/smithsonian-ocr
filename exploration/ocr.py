import json
import os
import sys
import requests
import time
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO

os.environ['COMPUTER_VISION_ENDPOINT'] = 'https://smithsonian-ocr.cognitiveservices.azure.com/'  ### ==> create a vision API end point in Azure portal and replace the value
os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY'] = 'your vision subscription key' ## ==> use the Vison API endpoint subscription key 

missing_env = False
# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("From Azure Cognitive Service, retrieve your endpoint and subscription key.")
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable, such as \"https://westus2.api.cognitive.microsoft.com\".\n")
    missing_env = True

if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("From Azure Cognitive Service, retrieve your endpoint and subscription key.")
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable, such as \"1234567890abcdef1234567890abcdef\".\n")
    missing_env = True

if missing_env:
    print("**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

text_recognition_url = endpoint + "/vision/v3.0/read/analyze"

def get_text(image_url, project_id, plot = True):
    
    image_id = image_url.split('id=')[-1]

    # Set image_url to the URL of an image that you want to recognize.
    # image_url = "https://static.adsabs.harvard.edu/static/phaedra/phaedra0882/0000882.187.jpg"
    
    if 'http' in image_url:
        print('web hosted image')
        headers = {'Ocp-Apim-Subscription-Key': subscription_key}
        data = {'url': image_url}
        response = requests.post(
            text_recognition_url, headers=headers, json=data)
        response.raise_for_status()

    # image_path = "smithsonian.png"
    else:
        # Read the image into a byte array
        image_data = open(image_url, "rb").read()
        headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                   'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Categories,Description,Color'}
        response = requests.post(text_recognition_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()


    # Extracting text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.

    # Holds the URI used to retrieve the recognized text.
    operation_url = response.headers["Operation-Location"]

    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()

#         print(json.dumps(analysis, indent=4))

        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False
    
    if plot:
        polygons = []
        if ("analyzeResult" in analysis):
            # Extract the recognized text, with bounding boxes.
            polygons = [(line["boundingBox"], line["text"])
                        for line in analysis["analyzeResult"]["readResults"][0]["lines"]]

        # Display the image and overlay it with the extracted text.
        if 'http' in image_url:
            image = Image.open(BytesIO(requests.get(image_url).content))
        else:
            image = Image.open(image_url)
        ax = plt.imshow(image)
        for polygon in polygons:
            vertices = [(polygon[0][i], polygon[0][i+1])
                        for i in range(0, len(polygon[0]), 2)]
            text = polygon[1]
            patch = Polygon(vertices, closed=True, fill=False, linewidth=.5, color='y')
            ax.axes.add_patch(patch)
            plt.text(vertices[0][0], vertices[0][1]-20, text, fontsize=4, va="top")
        fig1 = plt.gcf()
        plt.show()
        plt.draw()
        
        try:
            if 'http' in image_id and 'phaedra' in image_id:
                filename = './output-ocr-images/' + project_id + '/' + image_id.split('/')[-1].replace('.', '-') + '.png'
            else:
                filename = './output-ocr-images/' + project_id + '/' + image_id + '.png'
            
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            fig1.savefig(filename, dpi=400)
        except Exception as e:
            print(e)
            
        # get hocr output by: 1) create the blank output image, 2) write the text onto the output image, and 3) use tessarct to convert to hocr
        # height, then width
        a = np.full((image.height, image.width, 3), 255, dtype=np.uint8)
        white_image = Image.fromarray(a, "RGB")
        white_image.save("white.png", "PNG")
        
        
    return json.dumps(analysis)