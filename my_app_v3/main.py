import re
import requests

import time
from google.cloud import storage
from io import BytesIO

import json

from flask import Flask, render_template, request, jsonify

client = None
bucket = None

project_name = 'ds-web-app'
bucket_name = 'ds-app-bucket'
region = 'us-west2'
cloudfunction_name = 'image_classifier'

def get_img_from_url(url):
  file_type = url.split('.')[-1]
  regex = re.compile(
          r'^(?:http|ftp)s?://' # http:// or https://
          r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain
          r'localhost|' #localhost
          r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' #or ip
          r'(?::\d+)?' # optional port
          r'(?:/?|[/?]\S+)$', re.IGNORECASE)
  
  if re.match(regex, url) is not None and file_type in ['png', 'jpg', 'jpeg']:
    response = requests.get(url)
    if response.status_code == 200:
      return response.content

  return None

def upload_to_bucket(url):
  global client
  global bucket

  global project_name
  global bucket_name

  content = get_img_from_url(url)

  if content is not None:
    file_type = url.split('.')[-1]
    timestring = str(int(time.time()*1000))

    file_name = timestring + '.' + file_type
    file_content = BytesIO(content)

    if client is None or bucket is None:
      client = storage.Client(project=project_name)
      bucket = client.get_bucket(bucket_name)

    blob = bucket.blob(file_name)
    blob.upload_from_file(file_content)

    return file_name

  return None

def query_cloudfunction_model(file_name):
  global region
  global project_name
  global cloudfunction_name

  url = 'https://{}-{}.cloudfunctions.net/{}'.format(region, project_name, cloudfunction_name)
  myobj = {"file_name": file_name}

  x = requests.post(url, headers={"content-type":"application/json"}, data = json.dumps(myobj))

  x_arr = x.text.split(',')

  return x_arr

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/serve_prediction")
def serve_prediction():
  #arguments retrieved from user
  url = request.args.get('url')

  file_name = upload_to_bucket(url)

  if file_name:
    classification, probability = query_cloudfunction_model(file_name)

    classification = ' '.join(classification.split('_'))
    classification_text = 'The object in this image is a(n) {}'.format(classification)
    probability_text = 'Prediction probability: {:.1%}'.format(float(probability))

    global bucket_name
    display_url_template = 'https://storage.googleapis.com/{}/{}'
    img_tag_template = '<img src=\"{}\">'
    image_code = img_tag_template.format(display_url_template.format(bucket_name, file_name))

    return jsonify({'classification_text': classification_text,
                    'probability_text': probability_text,
                    'image_code':image_code})
  
  invalid_text = 'Invalid URL: use a direct URL to the image'
  return jsonify({'classification_text': invalid_text,
                  'probability_text': '',
                  'image_code': ''})