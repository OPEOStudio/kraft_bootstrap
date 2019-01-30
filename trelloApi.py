from trello import TrelloClient
import requests
import os
import json

# Trello ids - /!\ should store these in yaml or environment variables
LIST_TEAM_1_NOUVEAU = '5c41eeaee697f77851706ae7'
BOARD_SODAPEM = 'c2sq0A0u'

class TrelloAPI:
    zello_to_trello_usernames = {
    "user_kraaft_1": "user_kraaft_1",
    "user_kraaft_2": "user_kraaft_2",
    "kathy_g": "kathygreer"
    }

    def __init__(self):
        self.board_members = self.getBoard()

    def getBoard(self):
        querystring = {
                'key': os.environ['TRELLO_API_KEY'],
                'token': os.environ['TRELLO_API_SECRET']
                }
        url = "https://api.trello.com/1/boards/"+BOARD_SODAPEM+"/members"
        response = requests.get(url, params=querystring)
        return json.loads(response.text)

    def createCardWithAttachment(self, card_name, zello_users, audio_data, text_data):
        id_members = ""
        for user in zello_users:
            id = self.getBoardMemberIdByZelloUsername(user)
            if id != None:
                if id_members != "":
                    id_members += ','
                id_members += id

        querystring = {
            "name":card_name,
            "idList": LIST_TEAM_1_NOUVEAU,
            "idMembers":id_members,
            "desc": text_data,
            "key": os.environ['TRELLO_API_KEY'],
            "token": os.environ['TRELLO_API_SECRET']
            }
        url = "https://api.trello.com/1/cards"

        return requests.post(url, params=querystring, files={'fileSource': ('audio.mp3', audio_data)})

    def getBoardMemberIdByZelloUsername(self, zello_name):
        for member in self.board_members:
            try:
                if member['username'] == self.zello_to_trello_usernames[zello_name]:
                    return member['id']
            except KeyError:
                continue
        return None
