import io
import os
import json
import time

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Instantiates a client
client = speech.SpeechClient()

class SpeechToText(object):
	"""docstring for SpeechToText"""
	def __init__(self, arg):
		super(SpeechToText, self).__init__()
		self.client = speech.SpeechClient()
		self.encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
		self.sample_rate_hertz = 16000
		self.language_code = 'fr-FR'
		self.config = types.RecognitionConfig(
								encoding=self.encoding,
								sample_rate_hertz=self.sample_rate_hertz,
								language_code=self.language_code)
		self.save_path = ''

	def SetSavePath(self, save_path):
		"""sets save path"""
		self.save_path = os.path.join(
							os.path.dirname(__file__),
							save_path)

	def Convert(self, audio_path):
		"""converts an audio into a json file"""
		with io.open(audio_path, 'rb') as audio_file:
			content = audio_file.read()
			audio = types.RecognitionConfig(content=content)

		# Detects speech in the audio file
		response = self.client.recognize(self.config, audio)

		# Stores the information into a dictionary
		data = dict()
		data['file_name'] = audio_path
		data['time'] = '{}'.format(time.time)
		data['transcript'] = []
		for result in response.results:
			data['transcript'].append('{}'.format(result.alternatives[0].transcript))

		#extracts the name of the path

		# Converts the dictionary into a json file
		outfile = json.dumps(data, indent=4, sort_keys=false)





