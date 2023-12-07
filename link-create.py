import os.path
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

def find_google_drive_file_id(service, file_name, file_path):
    """
    Find the Google Drive file ID based on file name and path.
    """
    try:
        query = f"name = '{file_name}'"
        response = service.files().list(q=query, fields="files(id, name, parents)").execute()
        files = response.get('files', [])

        # If there's only one match, return it
        if len(files) == 1:
            return files[0]['id']
        elif len(files) > 1:
            # Additional logic to handle multiple files with the same name
            # For example, check the parents against the expected path
            # This is a placeholder for more complex logic you may need
            print(f"{file_name},{files[2]['id']}")
        return files[0]['id']
    except HttpError as error:
        print(f"An error occurred while searching for file {file_name}: {error}")
        return None

def generate_shareable_link(service, file_id):
    """
    Generates a shareable link for the file with the given file ID.
    """
    try:
        # Create a new permission to make the file readable by anyone with the link
        service.permissions().create(fileId=file_id, body={"type": "anyone", "role": "reader"}).execute()

        # Retrieve the file to get the webViewLink
        file = service.files().get(fileId=file_id, fields='webViewLink').execute()
        print(file.get('webViewLink'))
        return file.get('webViewLink')
    except HttpError as error:
        print(f"An error occurred while generating link for file {file_id}: {error}")
        return None

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)
        catalog_df = pd.read_csv('Update LLM Catalog - catalog.csv')
        location= 69134

        for row in catalog_df.iterrows():
            
            row=row[1]
            print( row)
            google_drive_file_id = find_google_drive_file_id(service, catalog_df.at[location, 'file_name'], catalog_df.at[location, 'google_drive_file_id'])
            if google_drive_file_id:
                link = generate_shareable_link(service, google_drive_file_id)
                if link:
                    # location= row['file_name'].replace('LM', '')
                    # location  = int(location.split('.')[0])
                    print(catalog_df.at[location, 'google_drive_file_id'])
                    catalog_df.at[location, 'google_drive_file_id'] = google_drive_file_id
                    catalog_df.at[location, 'shareable_link'] = link
                    catalog_df.to_csv('Update LLM Catalog - catalog.csv', index=False)
                     
                    print(f"Updated catalog saved. index: {location}")
                    location += 1  
        

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
