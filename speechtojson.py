import io
import os
import time
import json
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

client = speech.SpeechClient()

# BEFORE STARTING, FOLLOW https://codelabs.developers.google.com/codelabs/cloud-speech-intro/index.html#8
# COMMAND LINES & others : just instantiate the client on your machine

target_URL = "https://drive.google.com/drive/u/1/folders/1ILGoWUwjWMz2GUu9zzdtwQDBYw0Kb9mf?ogsrc=32"

def convert(dir_path, audio_name):
    with io.open(audio_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code='fr-FR')
    response = client.recognize(config, audio)
    with open(outfile_path, 'w') as write_file:  
        json.dump(data, write_file, indent=4, sort_keys=False)
