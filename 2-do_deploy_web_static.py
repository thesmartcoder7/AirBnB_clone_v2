#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py
it distributes an archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ["54.237.79.76", "100.25.156.57"]


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        print("False")
        return False

    file_name = archive_path.split("/")
    file_name = file_name[1]
    fname = file_name.split(".")
    fname = fname[0]

    newpath = "/data/web_static/releases/{}/".format(fname)

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(newpath))
        run("tar -xzf /tmp/{} -C {}".format(file_name, newpath))
        run("rm /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(newpath, newpath))
        run("rm -rf {}web_static".format(newpath))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(newpath))
        print("New version deployed!")
        return True
    except Exception:
        print("False 2")
        return False
