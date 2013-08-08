#!/usr/bin/env python2
from sh import git
from sh import cd,ls,pwd,rm
import sys
from datetime import datetime

class Git:

  srv = None
  usr = None
  f = None

  def __init__(self, server = 'git@github.com'):
    self.srv = server
    self.f = open('gitbackup-{0}.log'.format(datetime.now()), 'w')

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
    self.f.write("\n### LOG ENTRY - {0} ###\n".format(datetime.now()))
    print str(string)
    self.f.write(str(string))
    return
