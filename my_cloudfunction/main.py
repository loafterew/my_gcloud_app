import tensorflow as tf
import numpy as np
from google.cloud import storage

model = None
client = None
bucket = None

def retrieve_image(file_name, folder='/tmp/{}'):
  global client
  global bucket

  project_name = os.environ['PROJECT_NAME']
  bucket_name = os.environ['BUCKET_NAME']

  if client is None or bucket is None:
      client = storage.Client(project=project_name)
      bucket = client.get_bucket(bucket_name)

  blob = bucket.blob(file_name)
  dst_path = folder.format(file_name)
  blob.download_to_filename(dst_path)
  
  return dst_path

def classify_image(request):
  file_name = request.get_json().get('file_name')
  src_path = retrieve_image(file_name)

  global model

  if model is None:
      model = tf.keras.applications.ResNet50()

  image = tf.keras.preprocessing.image.load_img(src_path, 
                                              target_size=(224, 224))
  array = tf.keras.preprocessing.image.img_to_array(image)
  array = np.expand_dims(array, axis=0)
  array = tf.keras.applications.resnet50.preprocess_input(array)

  probabilities = model.predict(array)
  raw_prediction = (tf.keras.applications.resnet50.
                      decode_predictions(probabilities, top=1)[0][0])

  classification = raw_prediction[1]
  probability = str(round(raw_prediction[2],3))

  return classification + ',' + probability