from machine import Pin, SPI
from time import sleep_ms

# Display resolution
EPD_WIDTH  = const(400)
EPD_HEIGHT = const(300)

sck = Pin(18)
miso = Pin(12)
mosi = Pin(23) # DIN
cs = Pin(5)
dc = Pin(17)
rst = Pin(16)
busy = Pin(4)
# spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)
# spi = SPI(2, baudrate=50000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)


class EPD_PK:
    def __init__(self, miso=12, mosi=23, sck=18, cs=5, dc=17, reset=16, busy=4,baudrate=50000, width=400, height=300):
        self.spi = SPI(2, baudrate=baudrate, polarity=0, phase=0, sck=Pin(sck), miso=Pin(miso), mosi=Pin(mosi))
        self.cs = Pin(cs)
        self.dc = Pin(dc)
        self.rst = Pin(rst)
        self.busy = Pin(busy)
        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=0)
        self.busy.init(self.busy.IN)
        self.width = width
        self.height = height

    def _cmd(self, command, data=None):
        self.wait_until_idle()
        self.dc(0)
        self.cs(0)
        self.spi.write(command)
        self.cs(1)
        self.dc(1)
        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)

    def init(self):
        self.reset()
        sleep_ms(20)
        self.soft_reset()
        self._cmd(b'\x01', b'\x2B\x01\x00')
        self._cmd(b'\x3C', b'\x01')
        self._cmd(b'\x18', b'\x80')

    def snd_e(self):
        self._cmd(b'\x11', b'\x03')
        self._cmd(b'\x44', b'\x00\x31')
        self._cmd(b'\x45', b'\x00\x00\x2B\x01')
        self._cmd(b'\x4E', b'\x00')
        self._cmd(b'\x4F', b'\x00\x00')

    def snd_buf(self, cmd_pre, buf=None):
        self._cmd(cmd_pre)
        self.dc(1)
        self.cs(0)
        if buf != None:
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([buf[i]]))
        else:
            for i in range(0, self.width * self.height // 8):
                self.spi.write(bytearray([0xFF]))
        self.cs(1)

    def end_frame(self):
        self._cmd(b'\x21', b'\x40\x00')
        self._cmd(b'\x1A', b'\x6E')
        self._cmd(b'\x22', b'\xD7')
        self._cmd(b'\x20')
        self.wait_until_idle()


    def display_frame(self, frame_buffer):
        self.snd_e()
        self.snd_e()
        self.snd_buf(cmd_pre=b'\x26')
        self.snd_e()
        self.snd_buf(cmd_pre=b'\x24')
        self.end_frame()
        self.snd_e()
        self.snd_buf(cmd_pre=b'\x26', buf=frame_buffer)
        self.snd_e()
        self.snd_buf(cmd_pre=b'\x24', buf=frame_buffer)
        self.end_frame()
        self.snd_e()
        self.snd_buf(cmd_pre=b'\x26', buf=frame_buffer)
        self.snd_e()
        self.snd_buf(cmd_pre=b'\x24', buf=frame_buffer)
        sleep_ms(1)
        self._cmd(b'\x10', b'\x01')
        self.wait_until_idle()

    def wait_until_idle(self):
        while self.busy.value():
            sleep_ms(100)
    
    #    Reset line:  high 20ms, low for 2ms, hold high forever.
    def reset(self):
        self.rst(1)
        sleep_ms(20)
        self.rst(0)
        sleep_ms(2)
        self.rst(1)
        sleep_ms(10)

    def soft_reset(self):
        self._cmd(b'\x12')

