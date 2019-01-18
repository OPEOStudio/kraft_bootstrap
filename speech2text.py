import io
import os
import time
import json
from pydub import AudioSegment

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

def Speech2Text(json_file):
    """transcribes an audio into a json file"""

    sound = AudioSegment.from_file('tmp.mp3', format="mp3", channels=1)
    sound.export("audio.ogg",format="ogg")
    sound = AudioSegment.from_ogg('audio.ogg')
    audio = types.RecognitionAudio(content=sound._data)
    config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=32000,
                language_code='fr-FR')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    data = {}
    data['file_name'] = 'audio.ogg'
    # Change this...
    for result in response.results:
        data['body'] = '{}'.format(result.alternatives[0].transcript)
        break

    json.dump(data, json_file, indent=4, sort_keys=False)