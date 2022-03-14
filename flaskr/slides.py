from __future__ import print_function

import os.path
import uuid

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def create_slide(uni_list, body_text):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/presentations']

    # The ID of a sample presentation.
    PRESENTATION_ID = '1VGiN6EZCzKODESY1pbyOpd0I5qqUqJKym-BtWX_XKFY'

    gen_uuid = lambda : str(uuid.uuid4())  # get random UUID string

    creds = None
    
    title_text = ""
    for uni in uni_list:
        title_text += uni.capitalize() + ", "
    title_text = title_text[:-2:]
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('slides', 'v1', credentials=creds)

        slide_id = gen_uuid()
        title_id = gen_uuid()
        body_id = gen_uuid()

        requests = [
            {
            'createSlide': {
                'objectId': slide_id,
                'slideLayoutReference': {'predefinedLayout': 'TITLE_AND_BODY'},
                'placeholderIdMappings': [
                        {
                        'objectId': title_id,
                        'layoutPlaceholder': {'type': 'TITLE', 'index': 0}
                        },
                        {
                        'objectId': body_id,
                        'layoutPlaceholder': {'type': 'BODY', 'index': 0}                
                        }
                    ]
                }
            },
            {'insertText': {'objectId': title_id, 'text': title_text}},
            {'insertText': {'objectId': body_id, 'text': body_text}}
        ]

        # Execute the request.
        body = {
            'requests': requests
        }

        # Call the Slides API
        presentation = service.presentations().batchUpdate(body=body, presentationId=PRESENTATION_ID).execute()
    except HttpError as err:
        print(err)

if __name__ == "__main__":
    create_slide(['title'], 'Body of slide')