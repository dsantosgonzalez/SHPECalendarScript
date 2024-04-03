import re
from pypdf import PdfReader
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    slides = input("Enter the relative path of the PDF file: ")

    reader = PdfReader(slides) ##change to relative after
    text = ''
    for page in reader.pages:
        text += page.extract_text()

    # looks for a title in all caps, then a description, then the text date, time, and location of the event
    # not perfect by any means. this kinda sucks but blame a non standardized format for listing events
    events = re.findall(r'([A-Z\s]+)\n(.+?)\nDate: (.+?)\nTime: (.+?)\nLocation: (.+?)\n', text)

    # MANUAL LABOR!
    APIevents = []
    for event in events:
        print(event)

        name = input("Enter the name of the event: ")
        description = input("Enter a short description of the event: ")
        start = input("Enter the start date and time of the event in this format (YYYY-MM-DDTHH:MM:SS-04:00): ")
        end = input("Enter the end date and time of the event in this format (YYYY-MM-DDTHH:MM:SS-04:00): ")
        location = input("Enter the location of the event: ")
        colorID = int(input("What type of event is this? (1)GBM, (2)Volunteering, (3)Info Session, (4)Workshop, (5)Social: "))


        APIevents.append({
            'summary': name,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start,
                'timeZone': 'America/New_York'
            },
            'end': {
                'dateTime': end,
                'timeZone': 'America/New_York'
            },
            'colorID': colorID
        })

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        if not APIevents:
            print("No events to add")
            return

        #CREATE THE EVENTS! yeahhhhh
        for event in APIevents:
            print(event)
            event = service.events().insert(calendarId='primary', body=event).execute()
            print("Event created: %s" % (event.get("htmlLink")))



    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
