#!/usr/bin/env python2
import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials, AccessTokenRefreshError 

import time
from datetime import date
import logging

class GDrive:

  #GIT BACKUP client 
  CLIENT_ID = ''
  CLIENT_SECRET = ''

  # Check https://developers.google.com/drive/scopes for all available scopes
  OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

# Redirect URI for installed apps
  REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

  drive_service = ''
  parent_id = None
  logger = None
  wrkdir = None

  def __init__(self, wrkdir):
    self.logger = logging.getLogger('gitbackup')
    self.wrkdir = wrkdir
    return

  def authorize(self):
    # Run through the OAuth flow and retrieve credentials
    flow = OAuth2WebServerFlow(self.CLIENT_ID, self.CLIENT_SECRET, self.OAUTH_SCOPE, self.REDIRECT_URI)
    authorize_url = flow.step1_get_authorize_url()
    print 'Go to the following link in your browser: ' + authorize_url

    code = raw_input('Enter verification code: ').strip()
    credentials = flow.step2_exchange(code)
    json = credentials.to_json()
    try:
      f = open(self.wrkdir + '/.gitbackup-gdrive', 'w')
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
      f = open(self.wrkdir + '/.gitbackup-gdrive', 'r+')
      json = f.read()
      credentials = OAuth2Credentials.from_json(json)
      # Create an httplib2.Http object and authorize it with our credentials
      http = httplib2.Http()
      http = credentials.authorize(http)
      self.drive_service = build('drive', 'v2', http=http)
      f.close()
    except IOError as e:
      if(first):
        print(e)
        self.authorize()
        self.connect(False)
      else:
        self.logger.error("That's some funky shit, bailing out")
        self.logger.error(e)
  
  def createFolder(self, name=None):
    try:
      if(not name):
        name = 'gitbackup-{0}'.format(date.today())

      # Check if folder exists
      results = self.drive_service.files().list(q="mimeType='application/vnd.google-apps.folder' and trashed=false and title='" + name + "'").execute()
      if( len(results['items']) > 0):
        self.parent_id = results['items'][0]['id']
        return

      body = {
        'title': name,
        'mimeType': "application/vnd.google-apps.folder"
      }
      file = self.drive_service.files().insert(body=body).execute()
      self.parent_id = file['id']
    except AccessTokenRefreshError as e:
      self.logger.error("Got an AccessTokenRefreshError " + str(e))
      self.authorize()
      self.connect()
      self.createFolder(name)

  def upload(self, filename, fileinfo = {'title' : 'Git-Backup', 'description' : 'A bundle backup from git'}):
    self.logger.info(">> Uploading {0} ".format(filename).ljust(60, '.'),)
    try:
      # Insert a file
      print filename
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
      self.logger.info("DONE")
    except AccessTokenRefreshError as e:
      self.logger.error("Got an AccessTokenRefreshError " + str(e))
      self.authorize()
      self.connect()
      self.upload(filename)

