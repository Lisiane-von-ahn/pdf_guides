import streamlit as st
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive.readonly"]

creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret_169033200057-3qr8ptcvab54gtl0t87mt1mfd323f8ht.apps.googleusercontent.com.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

with open("token.json", "w") as token:
    token.write(creds.to_json())


drive_service = build('drive', 'v3', credentials=creds)


# Call the Drive v3 API
results = (
    drive_service.files()
    .list(pageSize=1000, fields="*")
    .execute()
)
items = results.get("files", [])

print(items)

# Function to list all files in a folder and its subfolders recursively
def list_files(folder_id):
    files = []
    response = drive_service.files().list(q=f"'{folder_id}' in parents",
                                          fields='files(id, name, mimeType)').execute()
    for file in response.get('files', []):
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            files.extend(list_files(file['id']))  # Recursively list files in subfolders
        else:
            files.append({'name': file['name'], 'id': file['id']})
    return files

# Function to search for text within a file
def search_text_in_file(file_id, text):
    content = drive_service.files().get_media(fileId=file_id).execute()
    print(content)

# Streamlit app
st.title("Google Drive Text Search")

# Select a folder from Google Drive
folder_id = st.text_input("Enter Google Drive folder ID:")

# Search text
search_text = st.text_input("Enter text to search:")

if st.button("Search"):
    if folder_id:
        files = list_files(folder_id)
        if files:
            st.write(f"Searching in {len(files)} files...")
            found_files = []
            for file in files:
                if search_text_in_file(file['id'], search_text):
                    found_files.append(file['name'])
            st.write("Found files:")
            for found_file in found_files:
                st.write(found_file)
        else:
            st.write("No files found in the specified folder.")
    else:
        st.write("Please enter a folder ID.")
