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

ZELLO_URL_BASE = "https://kraaft.zellowork.com"
ZELLO_URL_LOGIN = ZELLO_URL_BASE + "/user/login"
ZELLO_URL_GETTOKEN = ZELLO_URL_BASE + "/user/gettoken"
ZELLO_URL_METADATA = ZELLO_URL_BASE + "/history/getmetadata"
ZELLO_URL_MEDIA = ZELLO_URL_BASE + "/history/getmedia/key/"

headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }

### -----------------------------
### GETS TOKENS:
gettoken_response = zello_api_connect.gettoken_zello(url = ZELLO_URL_GETTOKEN, headers = headers)

### -----------------------------
### DEFINE THE LOGIN REQUEST
# Get md5(md5(Zello admin account password) + {token} + {API Key})
# Define the payload associated with the request
pre_h_pswd = os.environ['ZELLO_ADMIN_MD5'] + gettoken_response["token"] + os.environ['ZELLO_API_KEY']
payload = "username=Admin&password="+hash_md5(pre_h_pswd)

# Define the sid to be included in the API url request
querystring = {"sid": gettoken_response["sid"]}

# Define the Response object
response = requests.request("POST", ZELLO_URL_LOGIN, data = payload, headers = headers, params = querystring)


## Last ID
params = {}
params['sid'] = gettoken_response["sid"]
params['sort'] = 'id'
params['sort_order'] = 'ASC'
params['max'] = 1

#initialize the start_id parameter
start_id = last_message_id.getLastMessageId()

if start_id <= 1:
    request_metadata = requests.get(ZELLO_URL_METADATA, params = params)
    request_metadata_dict = json.loads(request_metadata.text)
    last_message_id.saveLastMessageId(request_metadata_dict['messages'][0]['id'])
    start_id = request_metadata_dict['messages'][0]['id']
params['start_id'] = start_id

del params['max']

googledrive = googledrive.GoogleDrive();
trello = trelloApi.TrelloAPI()

messages_handler = open('messages.log', 'a')

try:
    while 1:
        request_metadata = requests.get(ZELLO_URL_METADATA, params = params)
        request_metadata_dict = json.loads(request_metadata.text)
        messages = request_metadata_dict['messages']

        if len(messages) <= 1:
            continue

        if start_id != 0:
            del messages[0]

        print(messages[0]['id'])
        for message in messages:
            file_handler_audio = open('tmp.mp3', 'w+b')

            print('download mp3')
            # Download mp3
            if message['type'] != 'call_alert': # if call alert, no field
                url_media = ZELLO_URL_MEDIA + message['media_key']
                request_media = requests.get(url_media, params = querystring)
                request_media_dict = json.loads(request_media.text)
                
                try_nb = 5
                try:
                    while (request_media_dict['status'] == 'Waiting' and try_nb > 0):
                        request_media = requests.get(url_media, params = querystring)
                        request_media_dict = json.loads(request_media.text)
                        try_nb -= 1
                    params['start_id'] = message['id']
                    last_message_id.saveLastMessageId(params['start_id'])

                    if (request_media_dict['status'] == 'Waiting'):
                        raise ValueError('Could not download audio file from Zello')

                    audio_file = requests.get(request_media_dict['url'], data = {}, params = querystring)
                except ValueError as err:
                    print(err.args)
                    continue
                except:
                    continue


                print('json')
                # Transcribe to json
                file_handler_audio.write(audio_file.content)
                try:
                    json_dict = speech2text.Speech2Text()
                except ValueError as err:
                    print(err.args)
                    continue
                except:
                    print('Unknown error in SpeechToText: the most frequent reason is an audio message which is over 1min long.')
                    continue

                print('keyword detection')
                # Keyword detection - /!\ Does not work yet
                if keywordDetector.detect_keywords(json_dict) == False:
                    continue

                print ('Trello card creation')
                # Create Trello card - /!\ Does not work yet
                date = datetime.utcfromtimestamp(int(message['ts'])).strftime('%Y-%m-%d %H:%M:%S')
                card_name = message['sender']+' à '+message['recipient']+' - '+date
                zello_members = [message['sender'], message['recipient']]

                trello_response = trello.createCardWithAttachment(card_name, zello_members, audio_file.content, json_dict['body'])
                trello_dict = json.loads(trello_response.text)

                # In log file: Zello ID, Sender, Recipient, Date, Trello ID, Message Text
                log =  str(message['id']) + "," + message['sender'] + "," + message['recipient'] + "," + date + "," + str(trello_dict['idShort']) + "," + json_dict['body']+"\n"
                messages_handler.write(log)

                file_handler_audio.truncate()
                file_handler_audio.close()

except:
    last_message_id.saveLastMessageId(params['start_id'])
    print('interrupted')

messages_handler.close()