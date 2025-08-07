
#  Let's see if we can make the whole install, minus config files, work with this:
#  $>  mpremote mip install "github:kangasp/hi_map"

DEV=/dev/tty.usbserial-56230476401

CORE="__init__.py colors.py fplot.py nanogui.py writer.py"
WIDG="__init__.py  dial.py  label.py  led.py  meter.py  scale.py  textbox.py"
FONT="arial10.py  arial35.py  arial_50.py  courier20.py  font10.py  font6.py  freesans20.py"
EXTW="calendar.py  clock.py  eclock.py  grid.py"
EXTD="calendar.py  clock_test.py  eclock_async.py  eclock_test.py"
ROT="rotary.py  rotary_irq_esp.py"

CMD="mpremote connect /dev/tty.usbserial* "
LS="$CMD fs --no-verbose ls"
MKDIR="$CMD fs mkdir"
RMDIR="$CMD rm -rf"

$LS pk
$LS

cleanall


DIRS="drivers extras extras/widgets extras/demos gui gui/core gui/widgets gui/demos gui/fonts"
for D in $DIRS; do
$RMDIR $D
done

$LS
$LS

# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f mkdir gui
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f mkdir drivers
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f mkdir extras
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f mkdir extras/widgets
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f mkdir extras/demos
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f mkdir  gui/core
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f mkdir  gui/widgets
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f mkdir  gui/demos
# python ~/git_things/micropython_bin/pyboard.py --device $DEV -f mkdir  gui/fonts
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


