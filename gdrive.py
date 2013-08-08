#!/usr/bin/env python2
import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials, AccessTokenRefreshError 

import time
from datetime import datetime


class GDrive:
  #GIT BACKUP client 
  CLIENT_ID = '119053820637.apps.googleusercontent.com'
  CLIENT_SECRET = 'PfZsNGw6xZITgeWkZgOFfkuq'

  # Check https://developers.google.com/drive/scopes for all available scopes
  OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
  REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

  drive_service = ''
  parent_id = None

  def __init__(self):
    return

  def authorize(self):
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(self.CLIENT_ID, self.CLIENT_SECRET, self.OAUTH_SCOPE, self.REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url
    code = raw_input('Enter verification code: ').strip()
    #code = '4/Bv12BG7EZvzXIoEOKN4gXFElvEmb.YpayhnRqF_cSOl05ti8ZT3aT_E58gAI'
    credentials = flow.step2_exchange(code)
    json = credentials.to_json()
    try:
      f = open('.gitbackup-gdrive', 'w')
      f.write(str(json))
      f.close()
    except IOError as e:
      print e
      return
    # Create an httplib2.Http object and authorize it with our credentials
    #http = httplib2.Http()
    #http = credentials.authorize(http)

    #self.drive_service = build('drive', 'v2', http=http)

  def connect(self, first = True):
    try:
      f = open('.gitbackup-gdrive', 'r+')
      json = f.read()
      credentials = OAuth2Credentials.from_json(json)
      # Create an httplib2.Http object and authorize it with our credentials
      http = httplib2.Http()
      http = credentials.authorize(http)
      self.drive_service = build('drive', 'v2', http=http)
      f.close()
    except IOError as e:
      if(first):
        self.authorize()
        self.connect(False)
      else:
        print("That's some funky shit, bailing out")
        print(e)
  
  def createFolder(self, name=None):
    try:
      if(not name):
        name = 'gitbackup-{0}'.format(datetime.now())
        body = {
          'title': name,
          'mimeType': "application/vnd.google-apps.folder"
        }
        file = self.drive_service.files().insert(body=body).execute()
        self.parent_id = file['id']
    except AccessTokenRefreshError as e:
      print "Got an AccessTokenRefreshError " + str(e)
      self.authorize()
      self.connect()
      self.createFolder(name)

  def upload(self, filename, fileinfo = {'title' : 'Git-Backup', 'description' : 'A bundle backup from git'}):
    print ">> Uploading {0} ".format(filename).ljust(60, '.'),
    try:
      # Insert a file
      media_body = MediaFileUpload(filename, mimetype='application/octet-stream', resumable=False)
      body = {
        'title': fileinfo['title'],
        'description': fileinfo['description'],
        'mimeType': 'application/octet-stream',
      }

      if(self.parent_id):
        body['parents'] = [{'id': self.parent_id}]

      file = self.drive_service.files().insert(body=body, media_body=media_body).execute()
      #pprint.pprint(file)
      print "DONE"
    except AccessTokenRefreshError as e:
      print "FAIL"
      print "Got an AccessTokenRefreshError " + str(e)
      self.authorize()
      self.connect()
      self.upload(filename)

