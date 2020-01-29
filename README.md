# xf-tile
Pseudo Tiling window manager for Xfce DE<br />
<br />
![](https://i.ibb.co/ZVnmWbQ/desk1.png)<br /><br />
## What it is? <br />
A script to auto-tile up to 4 windows on your current workspace. It Supports 9 workspaces. After the 4th window, it will automatically enter full screen mode.<br />
Features:
+Tiling based on window type detection 
+Auto tiling without key bindings
+Move windows to different workspaces
+Full screen and tiling mode
+Config file
<br />
I tried to make it as integrated with XFCE as possible. For example, most shortcuts are configurable directly in the xfce settings manager without the need to edit any script or config file.<br />
<br />
## Why? <br />
If you like XFCE, but you want a more keyboard-driven experience or some basic tiling manager functionality without the hassle to install a different WM, then this script may be a good bet.<br />
<br />
## Dependencies <br />
[wmctrl](https://linux.die.net/man/1/wmctrl)<br />
[devilspie2](http://www.nongnu.org/devilspie2/)<br />
[pynput](https://pypi.org/project/pynput/) (install with pip)<br />
[xorg-xev](https://www.x.org/releases/X11R7.7/doc/man/man1/xev.1.xhtml)<br />
[xorg-xrandr](https://www.x.org/wiki/Projects/XRandR/)<br />
<br />
## Installation <br />
Install dependencies. Put xf-tile.py and xf-tile_config.json (edit with right values) inside your home directory. Put devilspie2 folder inside your .config folder.
Add xf-tile.py to your startup. (easisiest way: go to settings -> session and startup -> application autostart -> add -> Name: xf-tile | Command: python /home/$user/xf-tile.py | Trigger: on login) $replace user with your username<br />
Launch script or reboot.<br />
<br />
## Configuration<br />
max_windows_before_fullscreen = how many windows before activating full screen mode. MAX 4<br />
border  = single border px of your decoration window<br />
gaps = gaps in px between windows<br />
upper_panel_height <br /> upper panel height in px
lower_panel_height <br /> lower panel height in px
dynamic_resolution = in case you have a 2 in 1 laptop where resolution changes continuously<br />
app_to_exclude = applications to exclude from the tiling manager<br />
app_to_mod = some applications don't detect decorations correctly (for example kitty and vlc), if thats the case put the app name here (to see app names run on a terminal "devilspie2 --debug")<br />
<br />
## Shortcuts<br />
These shortcuts must be edited inside the script (line 156) and removed from XFCE settings to avoids conflicts.<br />
Super+e        = Set Mode (Tiled/Fullscreen)<br />
Super+CTRL=e   = Tiling Manager On/Off<br />
Super+CTRL+r   = Reload Config File<br />
Super+CTRL+l   = Move active window right<br />
Super+CTRL+h   = Move active window left<br />
Super+CTRL+0-9 = Move active window to x workspace<br />
<br />
Other shortcuts can be configured directly with XFCE <br />
<br />
## Suggestions<br />
[Theme](https://www.gnome-look.org/p/1016214/)<br />
<br />
## Not Supported/Tested<br />
- Multiscreen setups *not tested<br />
- Horizontal panels *not supported<br />
- Themes with not equal window border size *not supported<br />
<br />
## Bugs<br />
- Not really a bug, but some apps (like Gimp) set a hardcoded minimum window size, so depending on your monitor resolution and number of windows opened, you could get a window going beyond the limits of your screen. Not much i can do, move it to another workspace to have fullscreen mode. (you can also put the app in the exclude list)<br />
