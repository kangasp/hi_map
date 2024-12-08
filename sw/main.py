import network
import json
import urequests
from time import sleep
import machine
import os
import ota as ota

SSID = ""
PWORD = ""
G_URL = "https://raw.githubusercontent.com/kangasp/hi_map/main/sw/"
V_URL = G_URL + "version.json"


# TODO:  Get this grid programatically based on GPS coords
KR_URL = "https://api.weather.gov/gridpoints/HFO/240,91/forecast"



# headers = {'User-Agent': "hi_map",
#         'accept': "application/geo+json",
#         'Cache-Control': 'no-cache'}
# 
# response = urequests.get("https://api.weather.gov", headers=headers)
# response = urequests.get("https://api.weather.gov/gridpoints/HFO/240,91/forecast", headers=headers)
# data = json.loads(response.text)
# data['properties']['periods'][0]['name']
# data['properties']['periods'][0]['detailedForecast']



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




# connect_wifi(SSID, PWORD)
# latest_version_info(V_URL)

# response = urequests.get("https://raw.githubusercontent.com/kangasp/hi_map/main/sw/main.py")

# machine.reset()

