#!/usr/bin/env python2
from git import Git
from gdrive import GDrive
from datetime import datetime
import sys
import logging



logging.basicConfig(filename='gitbackup-{0}.log'.format(datetime.now()))
logger = logging.getLogger('gitbackup')
logger.setLevel(logging.DEBUG)

confFile = ''
try:
  confFile = open('gitbackup.conf', 'r')
except IOError as e:
  logger.error('Uh oh...' + str(e))
  confFile = open('gitbackup.conf', 'w')
  
g = Git()
gd = GDrive()

try:
  for line in confFile:
    if(line[0] == '#'):
      continue
    logger.info("## Read config line: {0}".format(line))
    data = line.rstrip().split(':')
    logger.debug('## Parsed config line to "{0}" - "{1}"'.format(data[0], data[1]))
    if(data[0] == 'gdrive_id'):
      gd.CLIENT_ID = data[1]
    if(data[0] == 'gdrive_secret'):
      gd.CLIENT_SECRET = data[1]
    if(data[0] == 'server'):
      g.srv = data[1]
    if(data[0] == 'gh-user'):
      g.usr = data[1]
    if(data[0] == 'repository' or data[0] == 'gh-repo'):
      g.clone(data[1])
      fn = g.backup(data[1])
      gd.connect()
      gd.createFolder()
      gd.upload(fn, {'title': data[1], 'description': 'Backup of repository ' + data[1] })
except:
  logger.error("error", str(sys.exc_info()))





