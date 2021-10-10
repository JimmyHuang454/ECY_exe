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

REPO = 'JimmyHuang454/ECY_exe'
TAG = NOW_TIME
NAME = "Build"


def UploadFile(release_id, file_path):
    upload_files = {'file': open(file_path, 'rb')}
    respon = requests.post(
        'https://uploads.github.com/repos/%s/releases/%s/assets?%s' %
        (REPO, release_id, urlencode({'name': os.path.split(file_path)[1]})),
        files=upload_files,
        headers={
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/zip',
            'Authorization': 'token ' + TOKEN
        })


def Delete(release_id):
    respon = requests.delete('https://api.github.com/repos/%s/releases/%s' %
                             REPO,
                             release_id,
                             headers={
                                 'Accept': 'application/vnd.github.v3+json',
                                 'Authorization': 'token ' + TOKEN
                             })
    print(respon.text)


#######################################################################
#                               delete                               #
#######################################################################
respon = requests.get('https://api.github.com/repos/%s/releases' % REPO)
respon = json.loads(respon.text)
for item in respon:
    print(item['id'])
    Delete(item['id'])


#######################################################################
#                               new                                #
#######################################################################
def NewPage():
    respon = requests.post('https://api.github.com/repos/%s/releases' % REPO,
                           json={
                               'tag_name': TAG,
                               'name': NAME,
                               'prerelease': False,
                           },
                           headers={
                               'Accept': 'application/vnd.github.v3+json',
                               'Authorization': 'token ' + TOKEN
                           })
    respon = json.loads(respon.text)
    print(respon)
    new_release_id = respon['id']
    return new_release_id


new_release_id = NewPage()

UploadFile(new_release_id, BASE_DIR + '/dist/cli.exe')
