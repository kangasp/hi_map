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

def update():
    i = ota.latest_version_info(V_URL)
    ota.update_files(i['files'], G_URL)
# i = ota.latest_version_info(V_URL)
# ota.update_files(i['files'], G_URL)

# connect_wifi(SSID, PWORD)
# latest_version_info(V_URL)

# response = urequests.get("https://raw.githubusercontent.com/kangasp/hi_map/main/sw/main.py")

# machine.reset()


#########  THIS CODE WORKS.  This is what we're going with. ###########
from color_setup import ssd  # Create a display instance
from gui.core.nanogui import refresh
from gui.core.writer import Writer
from gui.core.colors import *
from gui.widgets.label import Label
import gui.fonts.freesans20 as freesans20

refresh(ssd)  # Initialise and clear display.
Writer.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
wri = Writer(ssd, freesans20, verbose=False)
wri.set_clip(True, True, False)

# End of boilerplate code. This is our application:
Label(wri, 2, 2, 'Hello world!')
refresh(ssd)
ssd.set_partial()
ssd.fill(0)
Label(wri, 2, 20, 'Hello world!')
refresh(ssd)
#########  THIS CODE WORKS.  This is what we're going with. ###########



# LED Code

import machine, neopixel
np = neopixel.NeoPixel(machine.Pin(4), 8)
np[0] = (255, 0, 0) # set to red, full brightness
np[1] = (0, 128, 0) # set to green, half brightness
np[2] = (0, 0, 64)  # set to blue, quarter brightness
np.write()

import time

def demo(np):
    n = np.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()



import time
from rotary_irq_esp import RotaryIRQ
r = RotaryIRQ(pin_num_clk=32, 
              pin_num_dt=33, 
              min_val=0, 
              max_val=5,
              pull_up=True,
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_WRAP)
              
val_old = r.value()
while True:
    val_new = r.value()
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
    time.sleep_ms(50)

Pin( 36, Pin.OUT)


