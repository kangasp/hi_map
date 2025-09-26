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
import machine, neopixel
import asyncio

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

# with open('locations.json') as f:
#     j = json.load(f)
# 
# with open('urls.json', 'w') as f:
#     json.dump(urls, f)

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


def show_flash():
    import os
try:
    s = os.statvfs('/')
    total_blocks = s[0]
    free_blocks = s[3]
    block_size = s[1]
    total_flash_kb = (total_blocks * block_size) / 1024
    free_flash_kb = (free_blocks * block_size) / 1024
    used_flash_kb = total_flash_kb - free_flash_kb
    print(f"Total Flash: {total_flash_kb:.2f} KB")
    print(f"Free Flash: {free_flash_kb:.2f} KB")
    print(f"Used Flash: {used_flash_kb:.2f} KB")
except OSError as e:
    print(f"Error accessing filesystem information: {e}")







# return( response.json()['properties']['periods'][0]['name'], data['properties']['periods'][0]['detailedForecast'] )
_NUM_LOCALS = 4
def get_wx_data(urls):
    import micropython as _m
    import gc
    ret = {}
    headers = {'User-Agent': "hi_map",
            'accept': "application/geo+json",
            'Cache-Control': 'no-cache'}
    # response = urequests.get("https://api.weather.gov", headers=headers)
    for u in urls:
        print( f"fetching {u}")
        gc.collect()
        _m.mem_info()
        response = urequests.get(u[1], headers=headers)
        with open(u[0], 'w') as f:
            json.dump(response.json(), f)
        # all_data = response.json()
        # ret[u[0]] = [ all_data['properties']['periods'][0]['detailedForecast'] ]
        # for j in range(0, len(all_data['properties']['periods'])):
        #     ret[u[0]].append( [
        #             all_data['properties']['periods'][j]['probabilityOfPrecipitation']['value'], 
        #             all_data['properties']['periods'][j]['name'],
        #             all_data['properties']['periods'][j]['temperature'],
        #             all_data['properties']['periods'][j]['temperatureUnit'],
        #             all_data['properties']['periods'][j]['windSpeed'],
        #             all_data['properties']['periods'][j]['windDirection'],
        #             all_data['properties']['periods'][j]['shortForecast']
        #             ] )
        print( f"writing {u[0]} to flash")
        # with open('wx.json', 'w') as f:
        #     json.dump(ret, f)
    print( "Wrote wx.json")
    # return ret

# wx = get_wx_data(urls)
# with open('wx.json', 'w') as f:
#     json.dump(wx, f)
# 
# 
# wx = get_all_data(urls)

def get_data():
    headers = {'User-Agent': "hi_map",
            'accept': "application/geo+json",
            'Cache-Control': 'no-cache'}
    # response = urequests.get("https://api.weather.gov", headers=headers)
    response = urequests.get("https://api.weather.gov/gridpoints/HFO/240,91/forecast", headers=headers)
    # data = json.loads(response.text)
    return( response.json()['properties']['periods'][0]['detailedForecast'] )


def get_wx(place):
    try:
        with open(place, 'r') as f:
            wx_data = json.load(f)['properties']['periods'][0]['detailedForecast']
    except:
        print("No wx data found.")
        wx_data = None
    return wx_data

def get_wx_list(place):
    day = []
    desc = []
    print(f"Getting wx for {place}")
    with open(place, 'r') as f:
        p = json.load(f)['properties']['periods']
    for j in range(0,12,2):
        print("{0}: {1} deg, wind {2}\n   {3} ".format(p[j]['name'], p[j]['temperature'], p[j]['windSpeed'], p[j]['shortForecast']))
        day.append("{0}: {1} deg, wind {2} ".format(p[j]['name'], p[j]['temperature'], p[j]['windSpeed']))
        desc.append(f"{p[j]['shortForecast']}")
    return day, desc

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
    def light_one(self, idx, color=(10,10,10)):
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
    def __init__(self, r: RotaryIRQ, d: Display, l: My_led, places: list):
        self.r = r
        self.d = d
        self.l = l
        self.places = places
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
            r = self.r.value()
            title = self.places[r]
            # weather = get_wx(title)
            day, desc = get_wx_list(title)
        # ret[u[0]] = [ all_data['properties']['periods'][0]['detailedForecast'] ]
            print( f"Updating display for {title}")
            await self.d.update_display(f"{title}", day, desc, fast=True)
    async def r_action(self):
        while True:
            await self.e_r.wait()
            r = self.r.value()
            self.l.light_one(int(r))
            self.e_d.set()
            self.e_r.clear()


# from display import Display
# d = Display()
# asyncio.run(d.update_display("Test", "This is a test of the TextBox widget."))
# asyncio.run(d.refresh(fast=False))


# "name": "Today",
# "temperature": 83,
# "windSpeed": "3 to 12 mph",
# "shortForecast": "Scattered Rain Showers",
# "probabilityOfPrecipitation": {"unitCode": "wmoUnit:percent", "value": 36 },



'''
"windSpeed": "3 to 12 mph",
                "windDirection": "ENE",
                "detailedForecast": "Scattered rain showers. Mostly sunny, with a high near 83. East northeast wind 3 to 12 mph. Chance of precipitation is 40%. New rainfall amounts less than a tenth of an inch possible.",
                "startTime": "2025-08-16T07:00:00-10:00",
"shortForecast": "Scattered Rain Showers",
"name": "Today",
                "temperatureUnit": "F",
                "isDaytime": true,
                "endTime": "2025-08-16T18:00:00-10:00",
                "temperatureTrend": "",
"temperature": 83,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
"value": 36
                },
                "icon": "https://api.weather.gov/icons/land/day/rain_showers,40/rain_showers,20?size=medium",
                "number": 1

'''







async def enter_display_state(places: list):
    from display import Display
    r = RotaryIRQ(pin_num_clk=32, 
              pin_num_dt=33, 
              min_val=0, 
              max_val=_NUM_LOCALS - 1,
              pull_up=True,
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_WRAP)
    # wx = await get_wx() 
    l = My_led()
    d = Display()
    await d.clear()
    await d.clear()
    ap = Display_App(r, d, l, places)
    while True:
        await asyncio.sleep_ms(10)



with open('conf.json') as f:
    conf = json.load(f)

SSID = conf['wifi']['ssid']
PWORD = conf['wifi']['password']
# connect_wifi(SSID, PWORD)


# wx = get_wx()
# if wx is None:
#     print("No weather data found, fetching from API")
#     get_wx_data(urls)
#     wx = get_wx()

def run_app():
    places = [x[0] for x in urls]
    asyncio.run(enter_display_state(places))

run_app()



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

