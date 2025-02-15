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






# Another option:
## OFFICIAL, FOR SURE THE LAST ###
import epaper4in2
from machine import Pin, SPI
sck = Pin(18)
miso = Pin(12)
mosi = Pin(23) # DIN
cs = Pin(5)
dc = Pin(17)
rst = Pin(16)
busy = Pin(4)
# spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)
spi = SPI(2, baudrate=50000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)
e = epaper4in2.EPD(spi, cs, dc, rst, busy)
e.init()





import epaper4in2
from machine import Pin, SPI
cs = Pin(5)
dc = Pin(17)
rst = Pin(16)
busy = Pin(4)
spi = SPI(1, 40000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
e = epaper4in2.EPD(spi, cs, dc, rst, busy)
e.init()




w = 400
h = 300
x = 0
y = 0

# --------------------
# use a frame buffer
# 400 * 300 / 8 = 15000 - thats a lot of pixels
import framebuf
buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
black = 0
white = 1
fb.fill(white)
fb.text('Hello World',30,0,black)
# --------------------
print('Frame buffer things')
fb.fill(white)
fb.text('Hello World',30,0,black)
fb.pixel(30, 10, black)
fb.hline(30, 30, 10, black)
fb.vline(30, 50, 10, black)
fb.line(30, 70, 40, 80, black)
fb.rect(30, 90, 10, 10, black)
fb.fill_rect(30, 110, 10, 10, black)
for row in range(0,36):
	fb.text(str(row),0,row*8,black)
fb.text('Line 36',0,288,black)


import epaper_pk
e = epaper_pk.EPD_PK()
e.init()
e.clear()
e.draw_display()
e.clear(black=True)
e.draw_display()
e.clear()
e.draw_display()

import framebuf
w = 400
h = 300
x = 0
y = 0
buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
black = 0
white = 1
fb.fill(white)
fb.text('Hello Again',30,0,black)
e.set_ram(buf)
e.draw_display()


import freesans20
from writer import Writer
class NotionalDisplay(framebuf.FrameBuffer):
    def __init__(self, width, height, buffer):
        self.width = width
        self.height = height
        self.buffer = buffer
        self.mode = framebuf.MONO_HLSB
        super().__init__(self.buffer, self.width, self.height, self.mode)
    def show(self):
        ...


my_display = NotionalDisplay(400, 300, buf)
wri = Writer(my_display, freesans20)

Writer.set_textpos(my_display, 0, 0)
wri.printstring('Sunday\n')
my_display.show()
e.set_ram(buf)
e.draw_display()




















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




