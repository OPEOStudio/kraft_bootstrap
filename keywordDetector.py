import os
import json
import time
import shutil
import ntpath

# define a list of keywords
keywords = ('carte', 'cartes', 'nouvelle carte', 'nouvelles cartes',
            'ticket', 'tickets', 'nouveau ticket', 'nouveaux tickets')

# Directories
FROM_DIRECTORY = "FROM_DIRECTORY"
TO_DIRECTORY = "TO_DIRECTORY"

file_name = 'test.json'



def detect_keywords(file_name):
    """ Detects if a file contains trigger keywords """

    file_path = os.path.join(
                    os.path.dirname(__file__),
                    FROM_DIRECTORY,
                    file_name)

    # Open the json file
    with open(file_path) as json_file:

        # read json file
        json_dict = json.loads(json_file.read())
        
        # check if "body" (lowercased) contains any of the keywords
        if any(keyword in json_dict["body"].lower() for keyword in keywords):

            # Print the detected keyword
            print('A keyword has been detected in {} 🔑'.format(file_name))

            # Return
            return True

        else:

            # Print there is no detected keyword
            print('Could not fin any keyword in {} 🤷‍♀️'.format(file_name))

            # Return
            return False



def transfer_file(file_name):
    """ Transfere a json file from FROM_DIRECTORY to TO_DIRECTORY """
    
    # Source file
    src = os.path.join(
            os.path.dirname(__file__),
            FROM_DIRECTORY,
            file_name)

    # Destination file
    dst = os.path.join(
            os.path.dirname(__file__),
            TO_DIRECTORY,
            file_name)

    # Copy file from source to destination
    shutil.copyfile(src, dst)

    # Print the success
    print('{} has been transfered successfully 🎉'.format(file_name))



def newFileScanner():
    """ Detects when new file in the directory. """

    before = dict ([(f, None) for f in os.listdir(FROM_DIRECTORY)])
    while 1:
        time.sleep (10)
        after = dict ([(f, None) for f in os.listdir(FROM_DIRECTORY)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]

        # If new file in directory
        if added:

            # Print the name of the new files added
            print("Added: ", ", ".join(added))

            for f in added:

                # extract the name of the file
                file_name = ntpath.basename(f)

                # If a trigger keyword is detected in a file
                if detect_keywords(file_name):

                    # Transfer the file to a new directory
                    transfer_file(file_name)

        before = after



newFileScanner()





    