from machine import Pin, SPI
from time import sleep_ms
from micropython import const




# Display resolution
EPD_WIDTH  = const(400)
EPD_HEIGHT = const(300)


C_GATE_OUTPUT = const(b'\x01')
C_DATA_ENTRY_MODE = const(b'\x11')
C_TEMP_SELECTION = const(b'\x18')
C_TEMP_SENSOR_EXTERN = const(b'\x1A')
C_DISP_UPDATE_ACTVT = const(b'\x20')
C_DISP_UPDATE_CNTRL1 = const(b'\x21')
C_DISP_UPDATE_CNTRL2 = const(b'\x22')
C_RAM_BW = const(b'\x24')
C_RAM_RED = const(b'\x26')
C_BORDER_WAVEFORM = const(b'\x3C')
C_RAM_STARTEND_X = const(b'\x44')
C_RAM_STARTEND_Y = const(b'\x45')
C_RAM_COUNTER_X = const(b'\x4E')
C_RAM_COUNTER_Y = const(b'\x4F')










# Default Pin Settings
sck = Pin(18)
miso = Pin(12) # This isn't really used, but setup in spi anyway
mosi = Pin(23) # DIN
cs = Pin(5)
dc = Pin(17)
rst = Pin(16)
busy = Pin(4)

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
        self.hw_reset()
        self.wait_until_idle()
        sleep_ms(5)
        self.soft_reset()
        self.wait_until_idle()
        self._cmd(C_GATE_OUTPUT, b'\x2B\x01\x00')  # Is this needed??  (height-1 % 256), (height-1 / 256), 0
        self._cmd(C_DISP_UPDATE_CNTRL1, b'\x40\x00') # Display Update Control, 0x40=bypass red ram, 0x00=Single chain
        # self._cmd(C_BORDER_WAVEFORM, b'\x05') # 01 => LUT1,  05=> ??  bit3 is not defined in my datasheet.  Lets copy waveshare code.
        self._cmd(C_BORDER_WAVEFORM, b'\x01') # 01 => LUT1,  05=> ??  bit3 is not defined in my datasheet.  Lets copy waveshare code.
        self._cmd(C_TEMP_SELECTION, b'\x80') # 80 = internal
        self._cmd(C_DATA_ENTRY_MODE, b'\x03')  # Increment x & y up, in the x direction.  POR settings.  Do we need to set???
        self.set_window(0,0,self.height, self.width)
        self.set_cursor(0,0)
        self.wait_until_idle()

#     def snd_e(self):
#         self._cmd(b'\x11', b'\x03')
#         self._cmd(b'\x44', b'\x00\x31')
#         self._cmd(b'\x45', b'\x00\x00\x2B\x01')
#         self._cmd(b'\x4E', b'\x00')
#         self._cmd(b'\x4F', b'\x00\x00')

    def snd_buf(self, cmd_pre, buf=None, zero=False):
        self._cmd(cmd_pre)
        self.dc(1)
        self.cs(0)
        if buf != None:
            for i in range(0, self.width * self.height // 8):
                self._data(bytearray([buf[i]]))
        else:
            for i in range(0, self.width * self.height // 8):
                if zero:
                    self.spi.write(bytearray([0x00]))
                else:
                    self.spi.write(bytearray([0xFF]))
        self.cs(1)

#     def end_frame(self):
#         self._cmd(b'\x21', b'\x40\x00') # Display Update Control, 0x40=bypass red ram, 0x00=Single chain
#         self._cmd(b'\x1A', b'\x6E')
#         self._cmd(b'\x22', b'\xD7')
#         self._cmd(b'\x20')
#         self.wait_until_idle()
# 
# 
#     def display_frame(self, frame_buffer):
#         self.snd_e()
#         self.snd_e()
#         self.snd_buf(cmd_pre=b'\x26')
#         self.snd_e()
#         self.snd_buf(cmd_pre=b'\x24')
#         self.end_frame()
#         self.snd_e()
#         self.snd_buf(cmd_pre=b'\x26', buf=frame_buffer)
#         self.snd_e()
#         self.snd_buf(cmd_pre=b'\x24', buf=frame_buffer)
#         self.end_frame()
#         self.snd_e()
#         self.snd_buf(cmd_pre=b'\x26', buf=frame_buffer)
#         self.snd_e()
#         self.snd_buf(cmd_pre=b'\x24', buf=frame_buffer)
#         sleep_ms(1)
#         self._cmd(b'\x10', b'\x01')
#         self.wait_until_idle()

    def wait_until_idle(self):
        while self.busy.value():
            sleep_ms(100)
    
    #    Reset line:  high 20ms, low for 2ms, hold high forever.
    def hw_reset(self):
        self.rst(1)
        sleep_ms(20)
        self.rst(0)
        sleep_ms(2)
        self.rst(1)
        sleep_ms(10)

    def soft_reset(self):
        self._cmd(b'\x12')

    def set_ram(self, buf, x=0, y=0):
        self._cmd(C_DATA_ENTRY_MODE, b'\x03')
        self.set_window(0,0,self.height, self.width)
        self.set_cursor(0,0)
        self.snd_buf(C_RAM_BW, buf=buf)
        self._cmd(C_DATA_ENTRY_MODE, b'\x03')
        self.set_window(0,0,self.height, self.width)
        self.set_cursor(0,0)
        self.snd_buf(C_RAM_RED, buf=buf)  # Do I need to do this?

    def clear(self, black=False):
        self.snd_buf(C_RAM_BW, zero=black)
        self.snd_buf(C_RAM_RED, zero=black)  # Do I need to do this?

    def draw_display(self, fast=False, temp_fast=True):
        if temp_fast:
            self._cmd(C_TEMP_SELECTION, b'\x48') # 80 = internal, 48 = external
            self._cmd(C_TEMP_SENSOR_EXTERN, b'\x6E') # b'\x5A')
        # d = b'\xFF' # FF for BW, F7 for 3 color, FF is also used for partial
        d = b'\xD7' # FF for BW, F7 for 3 color, FF is also used for partial
        if fast:
            d = b'\xCF' # FF for BW, C7 for 3 color,  HOW ABOUT 99??
        self._cmd(C_DISP_UPDATE_CNTRL1, b'\x40\x00')
        self._cmd(C_DISP_UPDATE_CNTRL2, d)
        self._cmd(C_DISP_UPDATE_ACTVT)
        self.wait_until_idle()

    def set_window(self, x_start=0, y_start=0, x_end=0, y_end=0):
        self._cmd(C_RAM_STARTEND_X, b'\x00\x31')
        # self._cmd(C_RAM_STARTEND_X, bytes([((x_start>>3) & 0xFF ), ((x_end>>3) & 0xFF)]))
        # self._cmd(C_RAM_STARTEND_Y, bytes([(y_start & 0xFF), ((y_start >> 8) & 0xFF), (y_end & 0xFF), ((y_end >> 8) & 0xFF)]))
        self._cmd(C_RAM_STARTEND_Y, b'\x00\x00\x2B\x01')

    def set_cursor(self, x_start=0, y_start=0):
        self._cmd(C_RAM_COUNTER_X, bytes([x_start & 0xFF]))
        self._cmd(C_RAM_COUNTER_Y, bytes([(y_start & 0xFF), ((y_start >> 8) & 0xFF)]))





