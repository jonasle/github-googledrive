#!/usr/bin/env python2
from sh import git
from sh import cd,ls,pwd,rm,mkdir
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
    self.lgr.info(">> Cloning {0} .".format(self.srv + ":" + reponame))
    if(self.usr is not None):
      reponame = self.usr + '/' + reponame
    self.lgr.debug(git.clone(self.srv + ":" + reponame + '.git'))
    self.lgr.info("DONE")

  def backup(self, reponame):
    self.lgr.info(">> Backing up {0} ".format(reponame))
    spos = reponame.rfind('/')
    reponame = reponame[spos+1:] if spos > 0 else reponame
    cd(reponame)
    filename = reponame + '.bundle'
    self.lgr.debug(git.bundle.create('../'+filename, '--all'))
    self.lgr.info('DONE\n')
    return filename

