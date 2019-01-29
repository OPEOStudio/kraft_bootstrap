import io
import os
import time
import json
from pydub import AudioSegment

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import googlestorage

# Instantiates a client
speech_client = speech.SpeechClient()
storage_client = googlestorage.GoogleStorage()

def Speech2Text(json_file):

    """transcribes an audio into a json file"""

    sound = AudioSegment.from_file('tmp.mp3', format="mp3", channels=1)
    sound.export("audio.ogg",format="ogg")
    sound = AudioSegment.from_ogg('audio.ogg')

    storage_client.uploadFile(sound._data)

    audio = types.RecognitionAudio(uri="gs://kraaft-bootstrap/audio.ogg")
    config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=32000,
                language_code='fr-FR')

    # Detects speech in the audio file
#    try:
    response = speech_client.long_running_recognize(config, audio)

    print(response)
 #   data = {}
 #   data['file_name'] = 'audio.ogg'
    # Change this...
 #   for result in response.results:
 #       data['body'] = '{}'.format(result.alternatives[0].transcript)
 #       break

 #   json.dump(data, json_file, indent=4, sort_keys=False)
#    except:
#        print('Error with speech to text')