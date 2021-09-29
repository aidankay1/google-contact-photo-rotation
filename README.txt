For more information on the People API:
https://developers.google.com/people

---

Required files/directories:

creds/
    credentials.json
        # Credentials downloaded from Google Cloud project page
    token.json
        # OAuth tokens created during authentication process (happens automatically when running the program, requires access to a web browser)

images/
    # All images to be used in the rotation (ideally should have 1:1 aspect ratio)

vars/
    resource_name
        # plaintext resourceName value for desired contact (found in the URL of their Google Contacts page)
