#!/usr/bin/python3
from fabric.api import *

env.hosts = ["54.237.79.76", "100.25.156.57"]


def do_clean(number=0):
    """deletes out of data archives"""

    number = int(number)
    command = "cd /data/web_static/releases; ls | head -n -{} | xargs rm -rf"
    if number == 1 or number == 0:
        local("cd versions; ls | head -n -1 | xargs rm -rf")
        run("cd /data/web_static/releases; ls | head -n -1 | xargs rm -rf")
    else:
        local("cd versions; ls | head -n -{} | xargs rm -rf".format(number))
        run(
            command.format(number)
        )
