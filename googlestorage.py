# Imports the Google Cloud client library
from google.cloud import storage
import datetime

class GoogleStorage:

    def __init__(self):
        self.client = storage.Client()

    def uploadFile(self, file_data):
        name = 'audio_'+datetime.datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')+'.ogg'
        bucket = self.client.get_bucket('kraaft-bootstrap')
        blob = bucket.blob(name)
        blob.upload_from_string(file_data, 'audio/ogg')
        return name
