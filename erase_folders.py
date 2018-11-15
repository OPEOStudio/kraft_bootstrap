import os, re, os.path
import sys
import shutil

# Define path to old_files that are going to be deleted
# Define path to new_files in which we are going to put 

path_old_files = "C:/Users/Guillon/Documents/Marc/Kraft_Bootstrap/data/old_files"
path_new_files = "C:/Users/Guillon/Documents/Marc/Kraft_Bootstrap/data/new_files"

# Clear all the old files
for root, dirs, files in os.walk(path_old_files):
	for file in files:
		os.remove(os.path.join(root, file))

print("The folder old_files has been cleaned")

# Replace the old files with the new files
for root, dirs, files in os.walk(path_new_files):
	for file in files:
		shutil.copy(path_new_files+"/"+str(file),path_old_files+"/"+str(file))

print("Files from new_files have been duplicated in old_files")

# Clear all the new files
for root, dirs, files in os.walk(path_new_files):
	for file in files:
		os.remove(os.path.join(root, file))

print("The folder new_files has been cleaned")