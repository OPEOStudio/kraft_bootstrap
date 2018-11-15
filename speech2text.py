import io
import os
import time
import json

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

def Speech2Text(dir_path, audio_name):
    """converts an audio into a json file"""
    audio_path = os.path.join(dir_path, audio_name)

    # Loads the audio into memory
    with io.open(audio_path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code='fr-FR')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

    data = {}
    data['file_name'] = audio_name
    data['transcript'] = '{}'.format(result.alternatives[0].transcript)

    # Replaces de .ogg by .json
    json_name = audio_name.split('.raw')[0] + '.json'

    # Save the json file
    path_to_save = os.path.join(
                        os.path.dirname(__file__),
                        'data',
                        'new_json')
    
    outfile_path = os.path.join(path_to_save, json_name)

    with open(outfile_path, 'w') as write_file:  
        json.dump(data, write_file, indent=4, sort_keys=False)



path_to_watch = os.path.join(
                    os.path.dirname(__file__),
                    'data',
                    'new_raw')

before = dict ([(f, None) for f in os.listdir(path_to_watch)])
while 1:
    time.sleep (10)
    after = dict ([(f, None) for f in os.listdir(path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added: 
        print("Added: ", ", ".join(added))
        for f in added:
            Speech2Text(path_to_watch, f)
    if removed: 
        print("Removed: ", ", ".join(removed))
    before = after





