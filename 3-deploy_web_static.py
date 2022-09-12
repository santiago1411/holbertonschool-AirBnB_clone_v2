#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive
to your web servers, using the function deploy
"""

from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['3.90.180.30', '18.206.165.178']


def do_pack():
    """generates a tgz archive"""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        file = archive_path.split('/')[-1].split('.')[0]
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # Create the folder to uncompress the archive
        run('mkdir -p /data/web_static/releases/{}/'.format(file))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}'
            .format(file, file))
        # Remove file from /tmp/ dir
        run('rm /tmp/{}.tgz'.format(file))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}'.format(file, file))
        # Deletes existing symbilic link
        run('rm -rf /data/web_static/releases/{}/web_static'.format(file))
        run('rm -rf /data/web_static/current')
        # New symbolic link
        run('ln -s /data/web_static/releases/{}\
            /data/web_static/current'.format(file))
        return True
    except Exception as e:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path:
        do_deploy(archive_path)
    else:
        return False
