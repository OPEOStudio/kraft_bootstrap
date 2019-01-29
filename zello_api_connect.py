
### GOAL: function that gets the token of Zello API
### and RETURNS the dictionnary containing the response parameters

import requests
import json

url = "https://kraaft.zellowork.com/user/gettoken"

payload = ""

'''headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Postman-Token': "325a479f-5cf9-45e9-8b94-3a0355fa8bf2"
    }'''

headers = {
	'Content-Type': "application/x-www-form-urlencoded",
	'cache-control': "no-cache"
	}

def gettoken_zello(url, headers):

	print("Retrieving sid and token from the Zello API...")

	# creates a Response object containing the response of the API call
	response = requests.request("GET", url, data=payload, headers=headers)

	# stores the result of response in a dictionnary
	response_dict = json.loads(response.text)

	# For the test, extracts the token from the result
	token = response_dict["token"]
	sid = response_dict["sid"]

	return response_dict
