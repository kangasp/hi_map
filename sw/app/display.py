from gui.core.nanogui import refresh as gui_refresh
from gui.core.writer import Writer
from gui.core.colors import *
from gui.widgets.label import Label, ALIGN_CENTER
from gui.widgets.textbox import Textbox
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
        # self.writer_title.set_clip(True, True, False)
        # self.title = Label(self.writer_title, 0, 150, 'Title', align=ALIGN_CENTER)
        # self.title = Textbox(self.writer_title, 2, 20, 360, 1, clip=False )
        self.title = Label(self.writer_title, 2, 20, text=400-40, align=ALIGN_CENTER)
        Writer.set_textpos(self.ssd, 0, 0)
        _w = Writer(self.ssd, freesans20, verbose=False)
        self.day = []
        self.desc = []
        self.rows = 5
        _LH = 20
        _row_spacing = 26
        for i in range(self.rows):
                          # writer, row, col, width, height, clip=True, bdcolor=False
            row = 2 + 35 + 5 + i*(_LH + _row_spacing)
            col = 5
            width = 390
            height = 1
            t = Textbox(_w, row, col, width, height, clip=True, bdcolor=True )
            print(f"Day Row {i} at {row},{col} size {width}x{height}, t.height {t.height}")
            self.day.append(t)
        for i in range(self.rows):
            row = 2 + 35 + 25 + 5 + i*(_LH + _row_spacing)
            col = 60
            width = 400 - col - 5
            height = 1
            t = Textbox(_w, row, col, width, height, clip=True, bdcolor=True )
            print(f"DESC Row {i} at {row},{col} size {width}x{height}, t.height {t.height}")
            self.desc.append(t)
        # self.writer_body = Writer(self.ssd, freesans20, verbose=False)
        # self.writer_body.set_clip(True, True, False)
        # self.body = Label(self.writer_body, 100, 100, 'Body')

    def ready(self):
        # print(' comp: {0}, updated: {1}, _busy: {2} pin: {3}'.format(
        #     self.ssd.complete.state, self.ssd.updated.state, self.ssd._busy, self.ssd._busy_pin() ))
        return self.ssd.ready()

    async def refresh(self, fast=True):
        if fast:
            self.ssd.set_partial()
        else:
            self.ssd.set_full()
        self.ssd.show()
        await self.ssd.complete.wait()            
    
    async def clear(self):
        gui_refresh(self.ssd, True)
        await self.ssd.complete.wait()            
    
    async def update_display(self, title, day, desc, fast=True):
        self.title.value(title)
        #self.title.clear()
        # self.title.append(title)
        # self.title.value(title)
        for i in range(self.rows):
            self.day[i].clear()
            self.day[i].append(day[i])
            self.desc[i].clear()
            self.desc[i].append(desc[i])
        await self.refresh(fast)
