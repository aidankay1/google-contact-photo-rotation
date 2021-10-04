# Built from https://developers.google.com/people/quickstart/python
# See https://developers.google.com/people/api/rest/v1/people/updateContactPhoto for information

from __future__ import print_function
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
import random

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/contacts"]


def main():
    """
    Randomly chooses an image from a list and updates a contact's photo accordingly.
    """

    resource_name_file = "vars/resource_name"
    images_dir = "images/"

    # resourceName can be acquired from the contact's URL on contacts.google.com
    with open(resource_name_file, "r") as f:
        resource_name = f.read().strip("\n")

    # Image data must be sent in base64-encoded byte format
    image_bytes = select_image(images_dir)

    service = authenticate(SCOPES, "creds")

    try:
        service.people().updateContactPhoto(
            resourceName=resource_name, body={"photoBytes": image_bytes}
        ).execute()
    except:
        print("An error occurred while completing the request.")
    else:
        print("The request completed successfully.")


def authenticate(scopes, creds_dir):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(f"{creds_dir}/token.json"):
        creds = Credentials.from_authorized_user_file(f"{creds_dir}/token.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                # Will raise an exception if refresh token is expired
                creds.refresh(Request())
            except:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f"{creds_dir}/credentials.json", scopes
                )
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f"{creds_dir}/credentials.json", scopes
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f"{creds_dir}/token.json", "w") as token:
            token.write(creds.to_json())

    service = build("people", "v1", credentials=creds)
    return service


def select_image(dir):
    # https://gist.github.com/lambdaman2/3811448
    random_image = random.choice(os.listdir(dir))
    
    with open(f"{dir}/{random_image}", "rb") as image:
        # https://www.codespeedy.com/convert-image-to-base64-string-in-python/
        # Must be encoded in UTF-8 to be sent in JSON format
        image_bytes = base64.b64encode(image.read()).decode("utf-8")

    return image_bytes


if __name__ == "__main__":
    main()
