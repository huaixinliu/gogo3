#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-17 15:50:41
# @Author  : Wangmengcn (eclipse_sv@163.com)
# @Link    : https://eclipsesv.com
# @Version : $Id$

from fabric.api import *
from fabric.contrib.console import confirm

env.use_ssh_config = True
env.hosts = ['al']


def run_test():
    with settings(warn_only=True):
        result = local('python tester.py', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


def commit():
    local('git add -A && git commit')


def push():
    local('git push origin master && git push tx master')


def pre_deployed():
    run_test()
    commit()
    push()


def deploy():
    code_dir = '~/git/gogo3'
    run('ls')
    with settings(warn_only=True):
        if run("ls {}".format(code_dir)).failed:
            run("git clone https://github.com/love3forever/gogo3.git {}".format(code_dir))
    with cd(code_dir):
        run("git pull")
        run("sudo pip install -r ./src/backend/requirements.txt")
        with cd('./src/backend/api/'):
            run(
                'ps -ef | grep 0.0.0.0:33333 | grep -v grep | awk "{print $2}" | xargs kill')
            run("nohup gunicorn -w 2 -b 0.0.0.0:33333 server:app &")
    # with cd(code_dir):
    #     run("ps -ef | grep 0.0.0.0:33333 | grep -v grep \
    #         | awk '{print $2}' | head -n 1 | xargs kill")
    #     print('old process killed')
    #     run('git pull origin master')
    #     run('nohup gunicorn -w 2 -b 0.0.0.0:33333 server:app &')
