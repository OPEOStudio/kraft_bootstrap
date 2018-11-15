import os
import glob

from pydub import AudioSegment

# Explicitely set the path toward the ffmpeg package /bin
AudioSegment.converter = r"C:\\Program Files (x86)\\ffmpeg\\bin\\ffmpeg.exe"


## GOAL : take the latest added .ogg file
# and add it in history_file folder which summarizes everything
# and converts it directly into mp3 (for reading)
# and raw (for input into Google Speech)

# Piece that takes the last file and puts it into history_file

list_of_files = glob.glob("data\\new_files\\*")
# Directory of the latest file:
latest_file = max(list_of_files, key=os.path.getctime)

# Extracts the name of the file
name_latest_file = os.path.splitext(os.path.basename(latest_file))[0]

# Convert file into and put it into new folder
raw_audio = AudioSegment.from_file(latest_file, format="raw",
                                   frame_rate=44100, channels=2, sample_width=2)

raw_audio.export("data\\history_files\\"+name_latest_file+".raw",format="raw")
# raw_audio.export("data\\history_files\\"+name_latest_file+".mp3",format="mp3")

#print()
#print("The latest file has been converted to .raw and added to history_files")