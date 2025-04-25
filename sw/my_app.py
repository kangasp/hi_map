import network
import json
import urequests
from time import sleep
import machine
import ntptime
import os
import ota as ota
import time
from rotary_irq_esp import RotaryIRQ
from display import Display
import machine, neopixel
import asyncio

SSID = ""
PWORD = ""
G_URL = "https://raw.githubusercontent.com/kangasp/hi_map/main/sw/"
V_URL = G_URL + "version.json"


# TODO:  Get this grid programatically based on GPS coords
KR_URL = "https://api.weather.gov/gridpoints/HFO/240,91/forecast"

headers = {'User-Agent': "hi_map",
            'accept': "application/geo+json",
            'Cache-Control': 'no-cache'}
    # response = urequests.get("https://api.weather.gov", headers=headers)


GPS_ENDPOINT="https://api.weather.gov/points/"

# These don't work on micropython due to redirects
# WX_LOCALS = { "Kapaau": "20.235893868943386,-155.81184755521605",
#             "Kohala": "20.1082065567992,-155.8186041874043",
#             "Waimea": "20.020149125546165,-155.66956105109475",
#             "Mauna Kea": "19.82138417516427,-155.46855754250737",
#             "Mauna Loa": "19.472784734884513,-155.5922102463164",
#             "Hilo": "19.72158633670828,-155.08621452878822",
#             "South Point": "18.91155439777815,-155.6782112246365",
#             "Captain Cook": "19.488153218911417,-155.8936071377536",
#             "Kona": "19.64277330828564,-155.99612646286792",
#             "Waikoloa": "19.915998642211846,-155.88556972461396"
#               }

# Shorten the GPS location to avoid a redirect. These work.
WX_LOCALS = { "Kapaau": "20.2358,-155.8118",
            "Kohala": "20.1082,-155.8186",
            "Waimea": "20.0201,-155.6695",
            "Mauna Kea": "19.8213,-155.4685",
            "Mauna Loa": "19.4727,-155.5922",
            "Hilo": "19.7215,-155.0862",
            "South Point": "18.9115,-155.6782",
            "Captain Cook": "19.4881,-155.8936",
            "Kona": "19.6427,-155.9961",
            "Waikoloa": "19.9159,-155.8855"
              }

with open('locations.json') as f:
    j = json.load(f)

with open('urls.json', 'w') as f:
    json.dump(urls, f)

def get_urls(wx_locations):
    d = []
    for k in wx_locations.keys():
        response = urequests.get(GPS_ENDPOINT + wx_locations[k], headers=headers)
        url = response.json()['properties']['forecast']
        d.append((k,url))
    return d

# get_urls() should return something like this:
urls = [
 ('Kapaau', 'https://api.weather.gov/gridpoints/HFO/240,97/forecast'),
 ('Kohala', 'https://api.weather.gov/gridpoints/HFO/240,91/forecast'),
 ('Waimea', 'https://api.weather.gov/gridpoints/HFO/246,87/forecast'),
 ('Mauna Kea', 'https://api.weather.gov/gridpoints/HFO/254,78/forecast'),
 ('Mauna Loa', 'https://api.weather.gov/gridpoints/HFO/249,63/forecast'),
 ('Hilo', 'https://api.weather.gov/gridpoints/HFO/270,74/forecast'),
 ('South Point', 'https://api.weather.gov/gridpoints/HFO/245,38/forecast'),
 ('Captain Cook', 'https://api.weather.gov/gridpoints/HFO/236,63/forecast'),
 ('Kona', 'https://api.weather.gov/gridpoints/HFO/232,70/forecast'),
 ('Waikoloa', 'https://api.weather.gov/gridpoints/HFO/237,82/forecast')]


# return( response.json()['properties']['periods'][0]['name'], data['properties']['periods'][0]['detailedForecast'] )
_NUM_LOCALS = 3
def get_wx_data(urls):
    ret = []
    headers = {'User-Agent': "hi_map",
            'accept': "application/geo+json",
            'Cache-Control': 'no-cache'}
    # response = urequests.get("https://api.weather.gov", headers=headers)
    for u in urls:
        print( f"fetching {u}")
        response = urequests.get(u[1], headers=headers)
        ret.append(response.json()['properties']['periods'][0]['detailedForecast'])
        print( "Got it")
    return ret

wx = get_wx_data(urls)
with open('wx.json', 'w') as f:
    json.dump(wx, f)


wx = get_all_data(urls)

def get_data():
    headers = {'User-Agent': "hi_map",
            'accept': "application/geo+json",
            'Cache-Control': 'no-cache'}
    # response = urequests.get("https://api.weather.gov", headers=headers)
    response = urequests.get("https://api.weather.gov/gridpoints/HFO/240,91/forecast", headers=headers)
    # data = json.loads(response.text)
    return( response.json()['properties']['periods'][0]['detailedForecast'] )



def get_wx():
    try:
        with open('wx.json', 'r') as f:
            wx_data = json.load(f)
            wx_data = f.read()
        
    except:







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


def check_time():
    y, *_ = time.gmtime()
    if y < 2025:
        import ntptime
        ntptime.settime()


class My_led():
    def __init__(self, pin=15, num_led=_NUM_LOCALS):
        self.led_num = num_led
        self.np = neopixel.NeoPixel(machine.Pin(pin), num_led)
    def light_one(self, idx, color=(100,100,100)):
        for i in range(self.led_num):
            self.np[i] = (0,0,0)
        self.np[idx] = color
        self.np.write()

'''
Notes:
Problem:
I don't have enough memory to make the framebuffer and download all the weather.

Ideas:
Download all the weather before making the framebuffer.
I don't know how to fully destroy the framebuffer because of the way the library
creates it with the module.  Maybe I should try to change that?

Download all the weather only on timed wakeup or if we don't have it.
1. Wakeup
    a. If:
            1. We have current time (assume greater than 2000 is correct)
            2. and wx time file is less then 12 hours
                A. Then: enter wx display mode.
    b. Else:
            1. If we have network:
                A. Update time and WX, and SW update check.
                B. Then soft reset.
    b. Else: 
            1. Enter network setup state





'''

class Display_App():
    def __init__(self, r: RotaryIRQ, d: Display, l: My_led):
        self.r = r
        self.d = d
        self.l = l
        self.e_r = asyncio.Event()
        self.e_d = asyncio.Event()
        asyncio.create_task(self.r_action())
        asyncio.create_task(self.d_action())
        self.r.add_listener(self.r_cb)

    def r_cb(self):
        self.e_r.set()

    async def d_action(self):
        while True:
            await self.e_d.wait()
            self.e_d.clear()
            print( "1")
            await self.d.ssd.complete.wait()
            print( "2")
            await self.d.update_display("TITLE", "num: {0}".format(self.r.value()), fast=True)

    async def r_action(self):
        while True:
            await self.e_r.wait()
            r = self.r.value()
            self.l.light_one(int(r))
            self.e_d.set()
            self.e_r.clear()


async def enter_display_state():
    r = RotaryIRQ(pin_num_clk=32, 
              pin_num_dt=33, 
              min_val=0, 
              max_val=_NUM_LOCALS - 1,
              pull_up=True,
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_WRAP)
    wx = await get_wx() 
    l = My_led()
    d = Display()
    await d.clear()
    ap = Display_App(r, d, l)
    while True:
        await asyncio.sleep_ms(10)



class Setup_App():
    def __init__(self, l: My_led):
        print("setup all the things")

async def enter_setup_state():
    l = My_led()
    ap = Setup_App(l)
    while True:
        await asyncio.sleep_ms(10)




class Download_App():
    def __init__(self, l: My_led):
        print("setup all the things")

async def enter_download_state():
    l = My_led()
    ap = Download_App(l)
    while True:
        await asyncio.sleep_ms(10)




# def run_app():
#     l = My_led()
#     d = Display()
#     d.clear()
#     r = RotaryIRQ(pin_num_clk=32, 
#               pin_num_dt=33, 
#               min_val=0, 
#               max_val=_NUM_LOCALS,
#               pull_up=True,
#               reverse=True, 
#               range_mode=RotaryIRQ.RANGE_WRAP)
#     val_old = r.value()
#     while True:
#         val_new = r.value()
#         if val_old != val_new:
#             print('result =', val_new)
#             val_old = val_new
#             d.update_display("TITLE", f"num: {val_new}")
#             l.light_one(int(val_new))
#         else:
#             time.sleep_ms(50)

