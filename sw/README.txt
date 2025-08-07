

To just start the repl use:
alias repl="mpremote connect /dev/tty.usbserial-* repl"




To use with vim slime.

Use tmux to open a split window:
$> ctrl-B |

Then open vim on the left, and the repl of choice on the right.
Then send things to the repl with:
$> ctrl-c ctrl-c


The default window settings are saved in the vimrc, as:
let g:slime_default_config = {"socket_name": get(split($TMUX, ","), 0), "target_pane": ":.2"}

The repl for python to micropython can be started with:
screen /dev/tty.usbserial-56230476401 115200

To see help in screen:
ctrl-a ?
To quite:
ctrl-a ctrl-\






