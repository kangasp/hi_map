import network
import json
import urequests
from time import sleep
import machine
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

_NUM_LOCALS = 3

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


class My_led():
    def __init__(self, pin=15, num_led=_NUM_LOCALS +1):
        self.led_num = num_led
        self.np = neopixel.NeoPixel(machine.Pin(pin), num_led)
    def light_one(self, idx, color=(100,100,100)):
        for i in range(self.led_num):
            self.np[i] = (0,0,0)
        self.np[idx] = color
        self.np.write()


class App():
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


async def main():
    r = RotaryIRQ(pin_num_clk=32, 
              pin_num_dt=33, 
              min_val=0, 
              max_val=_NUM_LOCALS,
              pull_up=True,
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_WRAP)
    l = My_led()
    d = Display()
    await d.clear()
    ap = App(r, d, l)
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

