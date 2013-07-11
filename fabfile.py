#!/usr/bin/env python

from __future__ import with_statement

from fabric.api import run
from fabric.api import env
from fabric.api import cd
from fabric.api import execute

env.hosts = ["thousand-days.lobos.biz"]
env.user = "ubuntu"
env.key_filename = ["/Users/ewheeler/ewheeler.pem", ]

code_dir = "/home/ubuntu/rapidsms-thousand-days"


def update():
    run("git stash")
    run("git pull origin master")
    run("git stash pop")
    # remove pyc files
    run('find . -name "*.pyc" -exec rm {} \;')


def deploy():
    with cd(code_dir):
        run("circusctl stop")
        execute(update)
        run("circusctl start")
