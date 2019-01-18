from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
import googleapiclient.http
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.

class GoogleDrive:
    TO_JOIN_FOLDER_ID = '19mLU1ID_S4jNxdXfHWMcKBAyDKDC5QyV'
    TO_DECIDE_FOLDER_ID = '1zYVgfPLf3QR_Ujc-meJdQt35O38C6cd-'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    def __init__(self):
        self.service = self.authenticate()

    def authenticate(self):
        # Google Drive Authentication

        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('drive', 'v3', credentials=creds)

    def uploadFile(self, file_path, file_name, mimetype = 'application/octet-stream', directory = ''):
        file_metadata = {
            'name': file_name,
            'parents': [directory]
            }
        media = googleapiclient.http.MediaFileUpload(file_path, mimetype=mimetype)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
