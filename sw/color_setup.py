import machine
import gc

from epaper_42_v2 import EPD as SSD

gc.collect()  # Precaution before instantiating framebuf
ssd = SSD()  # Create a display instance
# Set this to run demos written for arbitrary displays:
# ssd.demo_mode = True


