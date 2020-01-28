"""
*********************************************************************************
*MIT License                                                                    *
*                                                                               *
*Author: eraserhead1897  eraserhead1897(at)protonmail(dot)com                   *
*                                                                               *
*Permission is hereby granted, free of charge, to any person obtaining a copy   *
*of this software and associated documentation files (the "Software"), to deal  *
*in the Software without restriction, including without limitation the rights   *
*to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      *
*copies of the Software, and to permit persons to whom the Software is          *
*furnished to do so, subject to the following conditions:                       *
*                                                                               *
*The above copyright notice and this permission notice shall be included in all *
*copies or substantial portions of the Software.                                *
*                                                                               *
*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     *
*IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       *
*FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    *
*AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         *
*LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  *
*OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  *
*SOFTWARE.                                                                      *
*********************************************************************************
"""
import subprocess
import threading
import json
from pynput.keyboard import Key, KeyCode, Listener

def send_notif(msg):
	subprocess.Popen(['notify-send', '-t', '5000', msg])

def set_mode():
	if running:
		global mode
		mode = 'tile' if mode == 'max' else 'max'
		send_notif(f"Tiling changed to: {'Tile' if mode == 'tile' else 'Fullscreen'}")
		set_windows(windows)

def set_running():
	global running
	running = False if running else True
	if running:
		set_windows(windows)
	send_notif(f"XF-Tile: {'On' if running  else 'Off'}")	

def on_press(key):
	current_keys.add(key)
	if frozenset(current_keys) in combo_to_func:
		combo_to_func[frozenset(current_keys)]()

def on_release(key):
	current_keys.remove(key)

def get_workspaces_number():
	n = subprocess.check_output(['wmctrl', '-d'], text=True)
	return int(n.strip().split('\n')[-1][0])

def move_to_workspace(ws_n):
	if ws_n <= get_workspaces_number():
		active_window_id = get_active_window()
		if ws_n != get_current_workspace():	
			for window in windows:
				if window['ID'] == active_window_id:
					window['WS'] = ws_n
					break
			subprocess.call(['wmctrl', '-v', '-i', '-r', str(active_window_id), '-t', str(ws_n)])	
			set_windows(windows)
		
def workspace_daemon():
	proc2 = subprocess.Popen(['xev','-root', '-event', 'property'], stdout=subprocess.PIPE, universal_newlines=True)
	while True:
		output2 = proc2.stdout.readline().strip()
		if output2.find('_NET_CURRENT_DESKTOP') != -1:
			set_windows(windows)
			
def get_active_window():
	output = subprocess.check_output(['xprop', '-root', '32x', '"\t$0"', '_NET_ACTIVE_WINDOW'])
	output = subprocess.check_output(['cut', '-f', '2'], input=output).decode()
	return int(output[:-2],16)	

def move_window(direction):
	try:
		active_window_id = get_active_window()
		ws = get_current_workspace()
		ws_windows = [index for index,window in enumerate(windows) if ws == window['WS']]
		ws_window = [index for index,window in enumerate(windows) if active_window_id == window['ID']]
		ws_window_in_windows = ws_windows.index(ws_window[0])
		if direction == 'left':
			windows[ws_windows[ws_window_in_windows]], windows[ws_windows[ws_window_in_windows-1]] = windows[ws_windows[ws_window_in_windows-1]],windows[ws_windows[ws_window_in_windows]]
		elif direction == 'right':
			try:
				windows[ws_windows[ws_window_in_windows]], windows[ws_windows[ws_window_in_windows+1]] = windows[ws_windows[ws_window_in_windows+1]],windows[ws_windows[ws_window_in_windows]]
			except IndexError:
				windows[ws_windows[ws_window_in_windows]], windows[ws_windows[0]] = windows[ws_windows[0]], windows[ws_windows[ws_window_in_windows]]
		set_windows(windows)
	except:
		pass
			
def get_current_workspace():
	workspaces = subprocess.check_output(['wmctrl', '-d'], text=True)
	n = workspaces.find('*')
	return int(workspaces[n-3:n-1].strip()) 

def set_app_mod(win, apps):
	mod = 0
	if win['APP'] in apps:
		mod += int(border/2)	
	return mod

def get_screen_res():
	screen_res = subprocess.check_output('xrandr')
	screen_res = subprocess.check_output(['grep', 'current'], input=screen_res).decode().strip().split(' ')
	screen_w =int(screen_res[7])
	screen_h = int(screen_res[9][:-1])
	return [screen_w, screen_h]

def get_screen_coords():
	global screen_width, screen_height
	try:	
		screen_width
		screen_height
	except NameError:
		screen_width = 0
		screen_height = 0
	if screen_width != get_screen_res()[0] or screen_width != get_screen_res()[1]:
		screen_width = get_screen_res()[0]
		screen_height = get_screen_res()[1]
		x = screen_width/2 + (gaps/2) 
		y=(screen_height-u_panel_height-l_panel_height)/2 + u_panel_height + (gaps/2)
		w=(screen_width/2)-(border)-(gaps*2) + (gaps/2) 
		h=((screen_height-u_panel_height-l_panel_height)/2) - (border) - (gaps*2) + (gaps/2) 
		single_window_h = screen_height - u_panel_height - l_panel_height - (border) - (gaps*2)   
		layout_setup(x,y,w,h,single_window_h)

def get_config(first_run):
	global dynamic_res, max_windows, border, gaps, u_panel_height, l_panel_height, exclude, app_to_mod
	with open('xf-tile_config.json') as config:
		data = json.load(config)
		max_windows = int(data['max_windows_before_fullscreen'])
		border = int(data['border']) * 2
		gaps = int(data['gaps'])
		u_panel_height = int(data['upper_panel_height']) + 1
		l_panel_height = int(data['lower_panel_height'])
		dynamic_res = int(data['dynamic_resolution'])
		exclude = tuple(data['app_to_exclude'])
		app_to_mod = tuple(data['app_to_mod'])
		if not first_run:
			get_screen_coords()
			set_windows(windows)
			send_notif('Config file reloaded')

def layout_setup(x,y,w,h,single_window_h):
	global lay_two, lay_three, lay_four
	lay_two = [[gaps,gaps+u_panel_height,w,single_window_h],[x,gaps+u_panel_height,w,single_window_h]]
	lay_three = [[gaps,gaps+u_panel_height,w,single_window_h],[x,gaps+u_panel_height,w,h],[x,y,w,h]]
	lay_four = [[gaps,gaps+u_panel_height,w,h],[x,gaps+u_panel_height,w,h],[gaps,y,w,h],[x,y,w,h]]

def set_windows(windows):
	current_windows = [window for window in windows if window["WS"] == get_current_workspace()]
	if current_windows and running:
		win_n = len(current_windows)
		for index,window in enumerate(current_windows):
			win_id = str(window["ID"])
			subprocess.call(['wmctrl', '-ir', win_id, '-b', 'remove,hidden'])	
			if mode == "max" or win_n > max_windows or win_n == 1:	
				subprocess.call(['wmctrl', '-ir', win_id, '-b', 'add,maximized_vert,maximized_horz'])
			else:
				subprocess.call(['wmctrl', '-ir', win_id, '-b', 'remove,maximized_vert,maximized_horz'])	
				mod = set_app_mod(window, app_to_mod)			
				if win_n == 2:
					subprocess.call(['wmctrl', '-ir', win_id, '-e', f"0,{int(lay_two[index][0] + mod)},{int(lay_two[index][1]+mod)},{int(lay_two[index][2])},{int(lay_two[index][3])}"])	
				elif win_n == 3:
					subprocess.call(['wmctrl', '-ir', win_id, '-e', f"0,{int(lay_three[index][0]+mod)},{int(lay_three[index][1]+mod)},{int(lay_three[index][2])},{int(lay_three[index][3])}"])			
				elif win_n == 4:
					subprocess.call(['wmctrl', '-ir', win_id, '-e', f"0,{int(lay_four[index][0]+mod)},{int(lay_four[index][1]+mod)},{int(lay_four[index][2])},{int(lay_four[index][3])}"])	

#=====================FUNC ENDS=============================

combo_to_func = {
    frozenset([Key.cmd, KeyCode(char='e')]): set_mode,
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='e')]): set_running,
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='r')]): lambda first_run=0: get_config(first_run),
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='l')]): lambda direction='right': move_window(direction),
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='h')]): lambda direction='left': move_window(direction),	
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='1')]): lambda ws_n=0: move_to_workspace(ws_n),
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='2')]): lambda ws_n=1: move_to_workspace(ws_n),
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='3')]): lambda ws_n=2: move_to_workspace(ws_n),
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='4')]): lambda ws_n=3: move_to_workspace(ws_n),
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='5')]): lambda ws_n=4: move_to_workspace(ws_n),
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='6')]): lambda ws_n=5: move_to_workspace(ws_n),
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='7')]): lambda ws_n=6: move_to_workspace(ws_n),
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='8')]): lambda ws_n=7: move_to_workspace(ws_n),
    frozenset([Key.cmd, Key.ctrl, KeyCode(char='9')]): lambda ws_n=8: move_to_workspace(ws_n)   
}

current_keys = set()	
running = True
mode = "tile"
windows = []
get_config(1)
get_screen_coords()

listener = Listener(on_press=on_press, on_release=on_release)
listener.start()	
proc = subprocess.Popen(['devilspie2','--debug'], stdout=subprocess.PIPE, universal_newlines=True)
thread1 = threading.Thread(target=workspace_daemon, daemon=True)
thread1.start()

while True:
	if dynamic_res and (screen_width != get_screen_res()[0] or screen_width != get_screen_res()[1]):
		get_screen_coords()
		set_windows(windows)
	output = proc.stdout.readline().strip().split(',')
	if output[0].startswith("+") and output[1] not in exclude and output[2] == 'WINDOW_TYPE_NORMAL':
		window = {'ID': int(float(output[0][1:])), 'APP': output[1], 'WS': get_current_workspace()}
		windows.append(window)
	elif output[0].startswith("-"):
		windows = [window for window in windows if not window["ID"] == int(float(output[0][1:]))]
	set_windows(windows)
