import urequests
import os
import json

def current_verion():
    ret = 0
    if 'version.json' in os.listdir():
        with open('version.json') as f:
            ret = int(json.load(f)['version'])
    return ret

def latest_version_info(version_url):
    print(f'Checking for latest version at: {version_url}')
    response = urequests.get(version_url)
    data = json.loads(response.text)
    return data

def save_from_url(file_name):
    ret = False
    file_url = URL + file_name
    response = urequests.get(file_url)
    if response.status_code == 200:
        print(f'Fetched latest firmware code, status: {response.status_code}')
        with open(file_name, 'w') as f:
            f.write(response.text)
        ret = True
    else:
        print(f'Firmware download error found - {file_url}, {response.status_code}.')
    return ret

def update_files(files):
    ret = True
    for f in files:
        if not save_from_url(f):
            print(f"FAILED update on file: {f}")
            ret = False
            break
    return ret
