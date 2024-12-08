import network

import os



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


repo_url = "https://raw.githubusercontent.com/kangasp/hi_map/main/version.json"


def latest_version(version_url):
    print(f'Checking for latest version at: {version_url}')
    response = urequests.get(version_url)
    data = json.loads(response.text)
    print(f"data is: {data}, url is: {version_url}")
    print(f"data version is: {data['version']}")

