# xf-tile
Pseudo Tiling window manager for Xfce DE

**What it is?**
A script to auto-tile up to 4 windows on your current workspace. It Supports 9 workspaces. After the 4th window, it will automatically enter full screen mode.

**Dependencies**
wmctrl
devilspie2
pynput (install with pip)
xorg-xev
xorg-xrandr

**Installation** 
Install dependencies. Put xf-tile.py and xf-tile_config.json inside your home directory. Put devilspie2 folder inside your .config folder.
Add xf-tile.py to your startup. (easisiest way: go to settings -> session and startup -> application autostart -> add -> Name: xf-tile | Command: python /home/$user/xf-tile.py | Trigger: on login) $replace user with your username

**Configuration**
max_windows_before_fullscreen = how many windows before activating full screen mode. MAX 4
border  = single border of your decoration window
gaps = gaps between windows
upper_panel_height 
lower_panel_height
dynamic_resolution = in case you have a 2 in 1 laptop where resolution changes continuously
app_to_exclude = applications to exclude from the tiling manager
app_to_mod = some applications don't detect decorations correctly (for example kitty and vlc), if thats the case put the app name here (to see app names run on a terminal "devilspie2 --debug")

Shortcuts must be edited inside the script, line 156.

**Suggestions**
[Theme](https://www.gnome-look.org/p/1016214/)

**Not Supported/Tested**
Multiscreen setups *not tested
Horizontal panels *not supported

