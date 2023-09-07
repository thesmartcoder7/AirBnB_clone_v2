#!/usr/bin/python3
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['54.237.79.76', '100.25.156.57']
env.user = 'ubuntu'


def do_pack():
    """ fabric script that generates a .tgz """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    path = "versions/web_static_{}.tgz".format(date)
    try:
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(path))
        return path
    except Exception:
        return None


def do_deploy(archive_path):
    """ fabric script to deploy to a server """
    if not os.path.exists(archive_path):
        return False

    file_name = archive_path.split("/")
    file_name = file_name[1]
    fname = file_name.split('.')
    fname = fname[0]

    newpath = '/data/web_static/releases/{}/'.format(fname)

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(newpath))
        run("tar -xzf /tmp/{} -C {}".format(file_name, newpath))
        run("rm /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(newpath, newpath))
        run("rm -rf {}web_static".format(newpath))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(newpath))
        return True
    except Exception:
        return False


def deploy():
    """ proper deploy"""

    path = do_pack()
    if not os.path.exists(path):
        return False

    res = do_deploy(path)
    return res
