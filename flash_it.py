#!/usr/bin/env python3

import subprocess
import sys
import argparse


CORE="__init__.py colors.py fplot.py nanogui.py writer.py"
WIDG="__init__.py  dial.py  label.py  led.py  meter.py  scale.py  textbox.py"
FONT="arial10.py  arial35.py  arial_50.py  courier20.py  font10.py  font6.py  freesans20.py"
EXTW="calendar.py  clock.py  eclock.py  grid.py"
EXTD="calendar.py  clock_test.py  eclock_async.py  eclock_test.py"
ROT="rotary.py  rotary_irq_esp.py"

ALL_FILES=[[ROT, "lib/micropython-rotary", "drivers"],
           [CORE, "lib/micropython-nano-gui/gui/core", "gui/core"],
           [WIDG, "lib/micropython-nano-gui/gui/widgets", "gui/widgets"],
           [FONT, "lib/micropython-nano-gui/gui/fonts", "gui/fonts"],
           [EXTW, "lib/micropython-nano-gui/extras/widgets", "extras/widgets"],
           [EXTD, "lib/micropython-nano-gui/extras/demos", "extras/demos"]]

DIRS="drivers extras gui extras/widgets extras/demos gui/core gui/widgets gui/demos gui/fonts"

# 
# for i in $ROT; do
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/micropython-rotary/$i :
# done
# for i in $CORE; do
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/micropython-nano-gui/gui/core/$i :/gui/core/
# done
# for i in $WIDG; do
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/micropython-nano-gui/gui/widgets/$i :/gui/widgets/
# done
# for i in $FONT; do
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/micropython-nano-gui/gui/fonts/$i :/gui/fonts/
# done
# for i in $EXTW; do
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/micropython-nano-gui/extras/widgets/$i :/extras/widgets/
# done
# for i in $EXTD; do
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/micropython-nano-gui/extras/demos/$i :/extras/demos/
# done
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/hi_map/sw/color_setup.py :
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/hi_map/sw/epaper_42_v2.py :
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/micropython-nano-gui/drivers/boolpalette.py :drivers/
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/micropython-nano-gui/gui/demos/aclock.py :gui/demos/
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/micropython-nano-gui/gui/demos/epd_async.py :gui/demos/
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f cp ~/git_things/micropython-nano-gui/extras/demos/clock_test.py :gui/demos/







MP_CMD = "mpremote connect /dev/tty.usbserial* "

def run_mpremote(args):
    result = subprocess.run(args, shell=True, capture_output=True, text=True)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return(result.stdout)

def cmd_fs(cmd_list):
    cmd = f"{MP_CMD} fs {' '.join(cmd_list)}"
    return run_mpremote(cmd)

def copy_file(src, dest):
    return cmd_fs(["cp", src, dest])

def remove_file(target):
    return cmd_fs(["rm", target])

def list_files(target):
    return cmd_fs(["ls", target])

def remove_all_files():
    files = list_files(' ')
    for file in files.splitlines()[1:]:
        tgt = file.strip().split(' ')[-1]
        print(f"Removing {tgt}")
        cmd_fs(["rm", "-r", tgt])

def full_install():
    for D in DIRS.split():
        cmd_fs([f"mkdir", D])
    for files, from_dir, to_dir in ALL_FILES:
        for file in files.split():
            print(f"Copying {file} to {to_dir}")
            cmd_fs(["cp", f"{from_dir}/{file}", f":/{to_dir}/{file}"])

def main():
    if len(sys.argv) == 1:
        print(list_files(' '))
    if sys.argv[1] == "clean_all":
        remove_all_files()
    elif sys.argv[1] == "full_install":
        full_install()
    else:
        print(cmd_fs(sys.argv[1:]))

if __name__ == "__main__":
    main()