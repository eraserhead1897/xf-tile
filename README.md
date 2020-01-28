# xf-tile
Pseudo Tiling window manager for Xfce DE<br />
<br />
**What it is?**<br />
A script to auto-tile up to 4 windows on your current workspace. It Supports 9 workspaces. After the 4th window, it will automatically enter full screen mode.<br />
<br /><br />
**Dependencies**<br />
wmctrl<br />
devilspie2<br />
pynput (install with pip)<br />
xorg-xev<br />
xorg-xrandr <br />
<br />
**Installation** <br />
Install dependencies. Put xf-tile.py and xf-tile_config.json inside your home directory. Put devilspie2 folder inside your .config folder.
Add xf-tile.py to your startup. (easisiest way: go to settings -> session and startup -> application autostart -> add -> Name: xf-tile | Command: python /home/$user/xf-tile.py | Trigger: on login) $replace user with your username<br />
<br />
**Configuration**<br />
max_windows_before_fullscreen = how many windows before activating full screen mode. MAX 4<br />
border  = single border of your decoration window<br />
gaps = gaps between windows<br />
upper_panel_height <br />
lower_panel_height <br />
dynamic_resolution = in case you have a 2 in 1 laptop where resolution changes continuously<br />
app_to_exclude = applications to exclude from the tiling manager<br />
app_to_mod = some applications don't detect decorations correctly (for example kitty and vlc), if thats the case put the app name here (to see app names run on a terminal "devilspie2 --debug")<br />
<br />
Shortcuts must be edited inside the script, line 156.<br />
<br />
**Suggestions**<br />
[Theme](https://www.gnome-look.org/p/1016214/)<br />
<br />
**Not Supported/Tested**<br />
Multiscreen setups *not tested<br />
Horizontal panels *not supported<br />

