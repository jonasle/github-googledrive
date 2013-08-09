#!/usr/bin/env python2
from git import Git
from gdrive import GDrive
import sys
import logging

logging.basicConfig(filename='gitbackup-{0}.log'.format(datetime.now()))
logger = logging.getLogger('gitbackup')

confFile = ''
try:
  confFile = open('gitbackup.conf', 'r')
except IOError as e:
  logger.error('Uh oh...' + str(e))
  confFile = open('gitbackup.conf', 'w')
  
g = Git()
gd = GDrive()
gd.connect()
gd.createFolder()
try:
  for line in confFile:
    logger.info("## {0}".format(line))
    data = line.split(':')
    data[1] = data[1].rstrip()
    if(data[0] == 'server'):
      g.srv = data[1]
    if(data[0] == 'repository' or data[0] == 'repo'):
      g.clone(data[1])
      fn = g.backup(data[1])
      gd.connect()
      gd.upload(fn, {'title': data[1], 'description': 'Backup of repository ' + data[1] })
    if(data[0] == 'user'):
      g.usr = data[1]

except:
  logger.error("error", str(sys.exc_info()))
