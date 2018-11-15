import os
import sys
import time
import subprocess
import shlex

import win32file
import win32con

# Aim of this file:
# - When a change is detected in the ZelloWork rep,
# - Call a script that cleans the old_files folder and
# that saves the newer files in the old_files folder
# - Create a list of .ogg files in the new_files folder

ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed from something",
  5 : "Renamed to something"
}
# Thanks to Claudio Grondi for the correct set of numbers
FILE_LIST_DIRECTORY = 0x0001

path_to_watch = "C:/Users/Guillon/AppData/Local/ZelloWork Artisan"
# path_to_watch = "C:/Users/Guillon/Documents/Marc/Kraft_Bootstrap/data"
print("Watching %s at %s" % (path_to_watch, time.asctime ()))

hDir = win32file.CreateFile (
  path_to_watch,
  FILE_LIST_DIRECTORY,
  win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
  None,
  win32con.OPEN_EXISTING,
  win32con.FILE_FLAG_BACKUP_SEMANTICS,
  None
)
while 1:
  #
  # ReadDirectoryChangesW takes a previously-created
  # handle to a directory, a buffer size for results,
  # a flag to indicate whether to watch subtrees and
  # a filter of what changes to notify.
  #
  # NB Tim Juchcinski reports that he needed to up
  # the buffer size to be sure of picking up all
  # events when a large number of files were
  # deleted at once.
  #
  results = win32file.ReadDirectoryChangesW (
    hDir,
    1024,
    True,
    # win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
    #  win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
    #  win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
     win32con.FILE_NOTIFY_CHANGE_SIZE,#  |
    #  win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
    #  win32con.FILE_NOTIFY_CHANGE_SECURITY,
    None,
    None
  )
  for action, file in results:
    full_filename = os.path.join (path_to_watch, file)
    print(full_filename, ACTIONS.get (action, "Unknown"))

  # Clean old_files; save the newer files in old_files
  os.system('erase_folders.py')   
  print("Folders cleaned, ready to create .ogg files")

  # Here, we need to run the hex.exe command that can 
  # trigger the conversion of data file into .ogg files
  # We first create the list of arguments
  # We then run with subprocess.call the command
  hex_path = "C:/Users/Guillon/Documents/Marc/hex.exe"
  input_path = "C:/Users/Guillon/AppData/Local/ZelloWork Artisan/artisan1's HistoryData"
  output_path = "C:/Users/Guillon/Documents/Marc/Kraft_Bootstrap/data/new_files"
  args = [hex_path,"-D",input_path, "-O", output_path]

  subprocess.call(args)

  # Save the latest .ogg file in a history file which we will use
  os.system('convert_latest_file.py')
  
  print()
  print("The latest file has been added to History and converted into .raw")
  print()
  
  