from gui.core.nanogui import refresh as gui_refresh
from gui.core.writer import Writer
from gui.core.colors import *
from gui.widgets.label import Label, ALIGN_CENTER
import gui.fonts.freesans20 as freesans20
import gui.fonts.arial_50 as arial50 # This needs to be remade with more chars
import gui.fonts.arial35 as arial35
import asyncio
from color_setup import ssd as _ssd

class Display():
    def __init__(self):
        self.ssd = _ssd
        Writer.set_textpos(self.ssd, 0, 0)
        self.writer_title = Writer(self.ssd, arial35, verbose=False)
        self.writer_title.set_clip(True, True, False)
        self.title = Label(self.writer_title, 0, 150, 'Title', align=ALIGN_CENTER)
        Writer.set_textpos(self.ssd, 0, 0)
        self.writer_body = Writer(self.ssd, freesans20, verbose=False)
        self.writer_body.set_clip(True, True, False)
        self.body = Label(self.writer_body, 100, 100, 'Body')

    def ready(self):
        print(' comp: {0}, updated: {1}, _busy: {2} pin: {3}'.format(
            self.ssd.complete.state, self.ssd.updated.state, self.ssd._busy, self.ssd._busy_pin() ))
        return self.ssd.ready()

    async def refresh(self, fast=True):
        print( "4")
        if fast:
            self.ssd.set_partial()
        else:
            self.ssd.set_full()
        self.ssd.show()
        print( "5")
        await self.ssd.complete.wait()            
        print( "6")
    
    async def clear(self):
        gui_refresh(self.ssd, True)
        await self.ssd.complete.wait()            
    
    async def update_display(self, title, body, fast=True):
        print( "3")
        self.title.value(title)
        self.body.value(body)
        print( "3.5")
        await self.refresh(fast)
