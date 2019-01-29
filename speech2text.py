import io
import os
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

    gs_name = storage_client.uploadFile(sound._data)

    audio = types.RecognitionAudio(uri="gs://kraaft-bootstrap/"+gs_name)
    config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=32000,
                language_code='fr-FR')

    # Detects speech in the audio file
#    try:
    response = speech_client.recognize(config, audio)

#    result = response.result(timeout=600)
    results = response.results
    print(results)
    data = {}
    # Change this...
    for result in results:
        for alternative in result.alternatives:
            data['file_name'] = 'audio.ogg'
            data['body'] = '{}'.format(alternative.transcript)
            break
        break

    return data
#    except:
#        raise ValueError('Error with speech to text')