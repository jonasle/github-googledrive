#!/usr/bin/env python2
from sh import git
from sh import cd,ls,pwd,rm
import sys
import logging
from datetime import datetime

class Git:

  srv = None
  usr = None
  lgr = None

  def __init__(self, server = 'git@github.com'):
    self.srv = server
    self.lgr = logging.getLogger('gitbackup')

  def clone(self, reponame):
    print ">> Cloning {0} ".format(reponame).ljust(60, '.'),
    rm('-rf', reponame)
    self.log(git.clone(self.srv + ":" + self.usr + '/' + reponame + '.git'))
    print "DONE"

  def backup(self, reponame):
    self.log(">> Backing up {0} ".format(reponame).ljust(60, '.'))
    filename = reponame + '.bundle'
    cd(reponame)
    self.log(git.bundle.create('../'+filename, '--all'))
    self.log('DONE\n')
    cd('..')
    return filename

  def log(self, string):
    self.lgr.debug(str(string))
    return
