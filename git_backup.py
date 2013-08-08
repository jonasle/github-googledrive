#!/usr/bin/env python2
from git import Git
from gdrive import GDrive
import sys
confFile = ''
try:
  confFile = open('gitbackup.conf', 'r')
except IOError as e:
  print 'Uh oh...' + str(e)
  confFile = open('gitbackup.conf', 'w')
  
g = Git()
gd = GDrive()
gd.connect()
gd.createFolder()
try:
  for line in confFile:
    g.log("## {0}".format(line))
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
  g.log("error", str(sys.exc_info()))
