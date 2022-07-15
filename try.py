import base64
import os
import pickle
from django.http import HttpResponse
# Gmail API utils
from Google import create_service
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

SCOPES = ['https://mail.google.com/']
our_email = 'lokeshwaran.naidu@miratsinsights.com'
CLIENT_SECRET_FILE='static/client.json'
API_NAME='gmail'
API_VERSION='v1'

service=create_service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)

email_msg='Yeahh, it is working'
mimeMessage=MIMEMultipart()
mimeMessage['to']='lokeshwaran.naidu@miratsinsights.com'
mimeMessage['subject']='test subject'
mimeMessage.attach(MIMEText(email_msg,'plain'))
raw_string=base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message=service.users().messages().send(userId='me',body={'raw':raw_string}).execute()
print(message)