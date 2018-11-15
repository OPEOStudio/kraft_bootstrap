
import glob
import os
import pydub

from pydub import AudioSegment

# Goal : convert a .ogg file into .raw file
### Eventually, we are not going to use this file
### because we use convert_latest_file.py

# Explicitely set the path toward the ffmpeg package /bin
pydub.AudioSegment.converter = r"C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe"
# print(os.path.exists("C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe"))

# Takes whatever 
request_dir = "data/"
extension_list = ('*.ogg','*.wav')

# ogg_filename = os.path.splitext(os.path.basename(request))[0] + '.ogg'

'''os.chdir(request_dir)'''

#Main function
for extension in extension_list:
    for request in glob.glob(extension):
        ogg_filename = os.path.splitext(os.path.basename(request))[0] + '.ogg'
        raw_filename = os.path.splitext(os.path.basename(request))[0] + '.raw'
        print(raw_filename)
        print(ogg_filename)
        raw_file = AudioSegment.from_file(request_dir+ogg_filename, format="raw",
                                   frame_rate=44100, channels=2, sample_width=2)
        raw_file.export(request_dir+raw_filename,format="raw")

'''
raw_audio = AudioSegment.from_file("audio.ogg", format="raw",
                                   frame_rate=44100, channels=2, sample_width=2)

raw_audio.export("audio.raw",format="raw")
'''
print()
print("I have change the file from .ogg to .raw")

## Old attempts
# Attempt to use the SoundFile package
# data, samplerate = sf.read('audio.ogg')
# sf.write('new_audio.raw', data, samplerate)

# Attempt to use the AudioSegment pydub function
# AudioSegment.from_file("audio.ogg").resample(sample_rate_Hz=32000,sample_width=2,channels=1)