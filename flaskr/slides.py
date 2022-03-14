from __future__ import print_function

import os.path
import uuid


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations']

# The ID of a sample presentation.
PRESENTATION_ID = '1VGiN6EZCzKODESY1pbyOpd0I5qqUqJKym-BtWX_XKFY'

gen_uuid = lambda : str(uuid.uuid4())  # get random UUID string

creds = None

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

    element_id = 'MyTextBox_01'
    page_object_id = gen_uuid()
    slide_id = gen_uuid()
    title_id = gen_uuid()
    body_id = gen_uuid()
    
    pt350 = {
        'magnitude': 350,
        'unit': 'PT'
    }
    requests = [
        {
            'createShape': {
                'objectId': element_id,
                'shapeType': 'TEXT_BOX',
                'elementProperties': {
                    'pageObjectId': page_object_id,                    
                    'size': {
                        'height': pt350,
                        'width': pt350
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 350,
                        'translateY': 100,
                        'unit': 'PT'
                    }
                }
            }
        },

        # Insert text into the box, using the supplied element ID.
        {
            'insertText': {
                'objectId': element_id,
                'insertionIndex': 0,
                'text': 'New Box Text Inserted!'
            }
        }
    ]
    
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
        {'insertText': {'objectId': title_id, 'text': 'Durham University'}},
        {'insertText': {'objectId': body_id, 'text': 'NO SHOTTTTTTT WE GOT IT'}}
    ]

    # Execute the request.
    body = {
        'requests': requests
    }

    # Call the Slides API
    presentation = service.presentations().batchUpdate(body=body, presentationId=PRESENTATION_ID).execute()
    #slides = presentation.get('slides')
    #create_shape_response = slides.get('replies')[0].get('createShape')
    #print('Created textbox with ID: {0}'.format(
    #    create_shape_response.get('objectId')))
except HttpError as err:
    print(err)