#!/usr/bin/python3
"""creates and distributes an archive to your web servers,
using the function deploy
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['3.90.180.30', '18.206.165.178']


def do_pack():
    """return the archive path if the archive has been correctly generated.
    Otherwise, it should return None
    """
    local("mkdir -p versions")
    date = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    file = local("tar -cvzf versions/web_static_{}.tgz web_static"
                 .format(datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')))
    if file.failed:
        return None
    return ("versions/web_static_{}.tgz".format(date))


def do_deploy(archive_path):
    """Returns True if all operations have been done correctly,
    otherwise returns False
    """
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        file = archive_path.split('/')[-1].split('.')[0]
        sudo("mkdir -p /data/web_static/releases/{}/".format(file))
        sudo("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
             .format(file, file))
        sudo("rm /tmp/{}.tgz".format(file))
        sudo("mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}/".format(file, file))
        sudo("rm -rf /data/web_static/releases/{}/web_static".format(file))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s /data/web_static/releases/{}/ /data/web_static/current"
             .format(file))
        return True
    except Exception:
        return False
        