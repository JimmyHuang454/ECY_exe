#!/usr/bin/env python3

import json
import os
import requests
import datetime
import sys

from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = BASE_DIR.replace('\\', '/')

NOW_TIME = str(int(datetime.datetime.now().timestamp()))
TOKEN = os.getenv('GITHUB_TOKEN', default='')

repo = 'JimmyHuang454/ECY_exe'
tag = NOW_TIME
name = "Build"


def UploadFile(release_id, file_path):
    upload_files = {'file': open(file_path, 'rb')}
    respon = requests.post(
        'https://uploads.github.com/repos/%s/releases/%s/assets?%s' %
        (repo, release_id, urlencode({'name': os.path.split(file_path)[1]})),
        files=upload_files,
        headers={
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/zip',
            'Authorization': 'token ' + TOKEN
        })


def Delete(release_id):
    respon = requests.delete('https://api.github.com/repos/%s/releases/%s' %
                             repo,
                             release_id,
                             headers={
                                 'Accept': 'application/vnd.github.v3+json',
                                 'Authorization': 'token ' + TOKEN
                             })
    print(respon.text)


#######################################################################
#                               delete                               #
#######################################################################
respon = requests.get('https://api.github.com/repos/%s/releases' % repo)
respon = json.loads(respon.text)
for item in respon:
    print(item['id'])
    Delete(item['id'])


#######################################################################
#                               new                                #
#######################################################################
def NewPage():
    url_template = 'https://{}.github.com/repos/' + repo + '/releases'
    respon = requests.post('https://api.github.com/repos/%s/releases' % repo,
                           json={
                               'tag_name': tag,
                               'name': name,
                               'prerelease': False,
                           },
                           headers={
                               'Accept': 'application/vnd.github.v3+json',
                               'Authorization': 'token ' + TOKEN
                           })
    respon = json.loads(respon.text)
    new_release_id = respon['id']
    return new_release_id


new_release_id = NewPage()

UploadFile(new_release_id, BASE_DIR + '/dist/cli.exe')
