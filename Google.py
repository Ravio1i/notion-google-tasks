import pickle
import os.path
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

AUTH_URL="https://www.googleapis.com/auth/"

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 9, 000).isoformat() + 'Z'
    return dt

class GoogleService():
    def __init__(self, client_secrets_file: str, api_name: str, api_version: str, scopes: list):
        self.client_secrets_file = client_secrets_file
        self.api_name = api_name
        self.api_version = api_version
        self.scopes = scopes
        self.creds = self.authenticate()
        self.service = build(self.api_name, self.api_version, credentials=self.creds)

    def authenticate(self):
        creds = None
        if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds


class GoogleCalendarService(GoogleService):
    def __init__(self, client_secrets_file, api_version: str='v3'):
        self.api_name = 'calendar'
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        super().__init__(client_secrets_file, self.api_name, api_version, self.scopes)


class GoogleDriveService(GoogleService):
    def __init__(self, client_secrets_file, api_version: str='v3'):
        self.api_name = 'drive'
        self.scopes = ['https://www.googleapis.com/auth/drive']
        super().__init__(client_secrets_file, self.api_name, api_version, self.scopes)


class GoogleTasksService(GoogleService):
    def __init__(self, client_secrets_file, api_version: str='v1'):
        self.api_name = 'tasks'
        self.scopes = ['https://www.googleapis.com/auth/tasks']
        super().__init__(client_secrets_file, self.api_name, api_version, self.scopes)

    def list_tasklists(self):
        # Call the Tasks API
        response = self.service.tasklists().list().execute()
        return response.get('items', [])
 
    def list_tasks(self, tasklist: str, showCompleted: bool=False):
        response = self.service.tasks().list(
            tasklist=tasklist,
            showCompleted=True,
            showHidden=True
        ).execute()
        lstItem = response.get('items')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = self.service.tasks().list(
                tasklist=tasklist,
                showCompleted=True,
                showHidden=True,
                pageToken=nextPageToken
            ).execute()
            lstItem = response.get('items')
            nextPageToken = response.get('nextPageToken')
        return lstItem
