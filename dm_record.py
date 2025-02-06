import os
import time
import mss
import cv2
import socket
import sys
import struct
import math
import random
import win32api as wapi
import win32api
import win32gui
import win32process
import ctypes
from ctypes  import *
from pymem   import *

import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import numpy as np
import matplotlib.pyplot as plt

from key_input import key_check, mouse_check, mouse_l_click_check, mouse_r_click_check
from key_output import set_pos, HoldKey, ReleaseKey
from key_output import left_click, hold_left_click, release_left_click
from key_output import w_char, s_char, a_char, d_char, n_char, q_char
from key_output import ctrl_char, shift_char, space_char
from key_output import r_char, one_char, two_char, three_char, four_char, five_char
from key_output import p_char, e_char, c_char_, t_char, cons_char, ret_char

from screen_input import grab_window
from config import *
from utils import *

from findOffsets.outputOffsets import *

save_name = "test"
folder_name = "/test/"
starting_value = 1

hwin_cs2 = win32gui.FindWindow(0, ('Counter-Strike 2'))
if(hwin_cs2):
    pid=win32process.GetWindowThreadProcessId(hwin_cs2)
    handle = pymem.Pymem()
    handle.open_process_from_id(pid[1])
    csgo_entry = handle.process_base
    print('CS2 was found')
else:
    print('CS2 wasnt found')
    os.system('pause')
    sys.exit()
    
list_of_modules=handle.list_modules()

while(list_of_modules!=None):
    tmp = next(list_of_modules)
    if(tmp.name == 'client.dll'):
        off_client_dll = tmp.lpBaseOfDll
        print('client.dll was found')
        break
    if(tmp.name=="engine.dll"):
        print('found engine.dll')
        off_enginedll=tmp.lpBaseOfDll
        break


    