#!/usr/bin/env python2
from git import Git
from gdrive import GDrive
from datetime import datetime
from sh import cd,ls,pwd,rm,mkdir
import sys, traceback, string
import random
import logging

def rand_id():
  char_set = string.ascii_letters + string.digits
  return ''.join(random.sample(char_set*6,6))

def performBackup(gitclient, gdclient, repository):
  tmpdir = rand_id()
  wrkdir = pwd().strip()
  mkdir(tmpdir)
  cd(tmpdir)
  gitclient.clone(repository)
  fn = gitclient.backup(repository)
  gdclient.connect()
  gdclient.createFolder()
  gdclient.upload(wrkdir + '/' + tmpdir + '/' + fn, {'title': repository, 'description': 'Backup of repository ' + repository })
  cd(wrkdir)
  rm('-rf', tmpdir)


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
gd = GDrive(pwd().strip())

try:
  for line in confFile:
    if(line[0] == '#'):
      continue
    data = line.strip().split(':')
    logger.debug('## Parsed config line to "{0}" - "{1}"'.format(data[0], data[1]))
    if(data[0] == 'gdrive_id'):
      gd.CLIENT_ID = data[1]
    if(data[0] == 'gdrive_secret'):
      gd.CLIENT_SECRET = data[1]
    if(data[0] == 'server'):
      g.srv = data[1]
    if(data[0] == 'gh-user'):
      g.usr = data[1]
    if(data[0] == 'gh-repo'):
      performBackup(g, gd, data[1])
    if(data[0] == 'repository'):
      g.usr = None
      g.srv = data[1]
      performBackup(g, gd, data[2])

except:
  exceptioninfo = sys.exc_info()
  logger.error(exceptioninfo[0])
  logger.error(exceptioninfo[1])
  tb = traceback.format_tb(exceptioninfo[2])
  for line in tb:
    logger.debug(line.rstrip())





