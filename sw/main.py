import network
import json
import urequests
from time import sleep
import machine
import os

SSID = ""
PWORD = ""
URL = "https://raw.githubusercontent.com/kangasp/hi_map/main/sw/"
V_URL = URL + "version.json"


def connect_wifi(ssid, password)->bool:
    ret = False
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    for i in range(30):
        if sta_if.isconnected():
            print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')
            ret = True
            break
        print('.', end="")
        sleep(0.5)
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



# connect_wifi(SSID, PWORD)
# latest_version_info(V_URL)

# response = urequests.get("https://raw.githubusercontent.com/kangasp/hi_map/main/sw/main.py")

# machine.reset()

