
# Zello API at https://zellowork.com/api.htm#auth_section

# Takes as INPUT:
# - API Key
# - md5(Zello admin account password)

# Calls zello_api_connect.py to get the API tokens (token & sid)
# Calls password_hasher.py to get API connection password
# --> md5(md5(Zello admin account password) + {token} + {API Key})
# LOGINS to Zello API
# GETs METADATA

# Creates a dictionnary with only the new messages
# ---> yet to be coded

# Searches for the media key
# ---> yet to be coded

# Downloads the corresponding messages and send them to a file
# ---> yet to be coded

# I need to get inspiration from https://www.digitalocean.com/community/tutorials/how-to-use-web-apis-in-python-3
# for further coding

print(" ")

import json
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
import os
import urllib
import tempfile
import requests
import zello_api_connect
import last_message_id
import googledrive
import trelloApi
import speech2text
import keywordDetector
from datetime import datetime
from password_hasher import hash_md5
from print_request import print_r

### -----------------------------
### INPUT variables
API_key = "RZCLSHHV4TE30WCMLUIWXI7HOM1HD8WV"
Zello_admin_password_md5 = "4cd60c519c8c507aaf3426b6323c0624"

url = "https://kraaft.zellowork.com"
url_login = "https://kraaft.zellowork.com/user/login"
url_gettoken = "https://kraaft.zellowork.com/user/gettoken"

headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }

### -----------------------------
### GETS TOKENS:
gettoken_response = zello_api_connect.gettoken_zello(url = url_gettoken, headers = headers)

token = gettoken_response["token"]
sid = gettoken_response["sid"]

### -----------------------------
### GETS md5(md5(Zello admin account password) + {token} + {API Key})
pre_h_pswd = Zello_admin_password_md5 + token + API_key

h_pswd = hash_md5(pre_h_pswd)

### -----------------------------
### DEFINE THE LOGIN REQUEST
# Define the payload associated with the request
payload = "username=Admin&password="+h_pswd

# Define the sid to be included in the API url request
querystring = {"sid":sid}

# Define the Response object
response = requests.request("POST", url_login, data = payload, headers = headers, params = querystring)

url_metadata = url + "/history/getmetadata"

## Last ID
params = {}
params['sid'] = sid
params['sort'] = 'id'
params['sort_order'] = 'ASC'
params['max'] = 1

#initialize the start_id parameter
start_id = last_message_id.getLastMessageId()

if start_id <= 1:
    request_metadata = requests.get(url_metadata, params = params)
    request_metadata_dict = json.loads(request_metadata.text)
    last_message_id.saveLastMessageId(request_metadata_dict['messages'][0]['id'])
    start_id = request_metadata_dict['messages'][0]['id']
params['start_id'] = start_id

del params['max']

googledrive = googledrive.GoogleDrive();
trello = trelloApi.TrelloAPI()


try:
    while 1:
        request_metadata = requests.get(url_metadata, params = params)
        request_metadata_dict = json.loads(request_metadata.text)
        messages = request_metadata_dict['messages']

        if len(messages) <= 1:
            continue

        if start_id != 0:
            del messages[0]

        print(messages[0]['id'])
        for message in messages:
            file_handler_audio = open('tmp.mp3', 'w+b')
            file_handler_json = open('tmp.json', 'w+')

            print('download mp3')
            # Download mp3
            url_media = url + "/history/getmedia/key/" + message['media_key']
            request_media = requests.get(url_media, params = querystring)
            request_media_dict = json.loads(request_media.text)
            try_nb = 5
            try:
                while (request_media_dict['status'] == 'Waiting' and try_nb > 0):
                    request_media = requests.get(url_media, params = querystring)
                    request_media_dict = json.loads(request_media.text)
                    try_nb -= 1
                params['start_id'] = message['id']

                if (request_media_dict['status'] == 'Waiting'):
                    raise ValueError('Could not download audio file from Zello')

                audio_file = requests.get(request_media_dict['url'], data = {}, params = querystring)
            except ValueError as err:
                print(err.args)
                continue


            print('json')
            # Transcribe to json
            file_handler_audio.write(audio_file.content)
            try:
                speech2text.Speech2Text(file_handler_json)
            except ValueError as err:
                print(err.args)
                continue

            print('keyword detection')
            # Keyword detection - /!\ Does not work yet
            # if keywordDetector.detect_keywords('tmp.json') == False:
            #    continue

            print('google drive')
            # Upload to Google Drive - /!\ works, but is not needed anymore - if needed, file naming has to be implemented first
            # googledrive.uploadFile('tmp.mp3', 'final.mp3', 'audio/*', googledrive.TO_JOIN_FOLDER_ID)
            # googledrive.uploadFile('tmp.json', 'final.json', 'application/json', googledrive.TO_DECIDE_FOLDER_ID)

            print ('Trello card creation')
            # Create Trello card - /!\ Does not work yet
            date = datetime.utcfromtimestamp(int(message['ts'])).strftime('%Y-%m-%d %H:%M:%S')
            card_name = message['sender']+' à '+message['recipient']+' - '+date
            zello_members = [message['sender'], message['recipient']]

            response = trello.createCardWithAttachment(card_name, zello_members, audio_file.content)
            print(response.text)

            file_handler_audio.truncate()
            file_handler_audio.close()
            file_handler_json.truncate()
            file_handler_json.close()

except KeyboardInterrupt:
    last_message_id.saveLastMessageId(params['start_id'])
    print('interrupted')

