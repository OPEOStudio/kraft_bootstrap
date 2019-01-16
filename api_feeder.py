
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
import urllib
import requests
import zello_api_connect
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

nbr_msg_to_check = "max=1"

### -----------------------------
### GETS TOKENS:
gettoken_response = zello_api_connect.gettoken_zello(url = url_gettoken, headers = headers)

token = gettoken_response["token"]
sid = gettoken_response["sid"]

print("token : " + token)
print("sid : " + sid)
print(" ")

### -----------------------------
### GETS md5(md5(Zello admin account password) + {token} + {API Key})
pre_h_pswd = Zello_admin_password_md5 + token + API_key
print("Pre md5 hash password : " + pre_h_pswd)

h_pswd = hash_md5(pre_h_pswd)
print("md5(md5(Zello admin account password) + token + API Key) = " + h_pswd)

### -----------------------------
### DEFINE THE LOGIN REQUEST
# Define the payload associated with the request
payload = "username=Admin&password="+h_pswd
print("payload : " + payload)

# Define the sid to be included in the API url request
querystring = {"sid":sid}

# Define the Response object
response = requests.request("POST", url_login, data = payload, headers = headers, params = querystring)

### Print the request object for dev purposes
print_r("POST", url_login, data = payload, headers = headers, params = querystring)

### -----------------------------
### DEFINE THE GET METADATA REQUEST
### Request test to get the 1 last history metadata message
# Don't know why, the max just doesn't work, I get 100 messages
# I'll have to further select the first element of the list, no choice
url_metada = url + "/history/getmetadata"
request_metadata = requests.request("POST", url_metada, data = nbr_msg_to_check, params = querystring)
# Print the request for dev purposes
print_r("POST", url_metada, data = nbr_msg_to_check, headers = {}, params = querystring)

print("request_metada : " + request_metadata.text)

### -----------------------------
### DOWNLOADS A DEFINED OBJECT
# Just a test with the media key of the last Zello message
media_key = "1901d582e2e467671680d73dfb4d5944ac6ba959240412e718f424154fa03c9d"
url_media = url + "/history/getmedia/key/" + media_key

request_media = requests.request("GET", url_media, data = "", headers ={}, params = querystring)
print_r("GET", url_media, data = "", headers = {}, params = querystring)
print("request media :" + request_media.text) # Prints the server response

## Extracts url containing file from the request body
# Transforms json response into a dictionnary and extract the url field
request_media_dict = json.loads(request_media.text)
print('==== Request Media Dictionary ====')
for key, value in request_media_dict.items():
    print(key, value)
print('==== END Request Media Dictionary ====')
url_download = request_media_dict["url"]
print("url_download = " + url_download)

## MP3 file download
print("Beginning the download of the file...")
file_handler = open('sound.mp3', 'wb')
response = requests.get(url_download, data = {}, params = querystring)
file_handler.write(response.content)










