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
    self.lgr.info(">> Cloning {0} ".format(reponame).ljust(60, '.'))
    rm('-rf', reponame)
    self.lgr.debug(git.clone(self.srv + ":" + self.usr + '/' + reponame + '.git'))
    self.lgr.info("DONE")

  def backup(self, reponame):
    self.lgr.info(">> Backing up {0} ".format(reponame).ljust(60, '.'))
    filename = reponame + '.bundle'
    cd(reponame)
    self.lgr.debug(git.bundle.create('../'+filename, '--all'))
    self.lgr.info('DONE\n')
    cd('..')
    return filename

