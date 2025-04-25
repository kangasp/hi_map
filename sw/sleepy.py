from machine import  RTC, Pin, deepsleep, DEEPSLEEP
import esp32

def isr(p):
    print("INTERRUPT: ", p)

def go_to_sleep(ms=10000, wake_pin=32):
    # configure RTC.ALARM0 to be able to wake the device
    # rtc = RTC()
    # rtc.irq(trigger=rtc.ALARM0, wake=DEEPSLEEP)
    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    # rtc.alarm(rtc.ALARM0, ms)
    # Don't use pin 35, pullup is too weak or doesn't exist?
    p = Pin(wake_pin, Pin.IN, Pin.PULL_UP)
    p.irq(isr, Pin.WAKE_LOW, wake=DEEPSLEEP)
    esp32.wake_on_ext0(pin=p, level=esp32.WAKEUP_ALL_LOW)
    # put the device to sleep
    deepsleep(ms)

