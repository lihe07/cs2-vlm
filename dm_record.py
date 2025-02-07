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

offsets = requests.get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
client_dll = requests.get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client_dll.json').json()

dwLocalPlayerPawn = offsets['client.dll']['dwLocalPlayerPawn']
m_iHealth = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_iHealth']
m_iObserverMode = client_dll['client.dll']['classes']['CPlayer_ObserverServices']['fields']['m_iObserverMode']



while True:
    try:
        pm = pymem.Pymem("cs2.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        break
    except:
        pass

pm = pymem.Pymem("cs2.exe")
client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

SAVE_TRAIN_DATA = True
IS_PAUSE = False # pause saving of data
n_loops = 0 # how many frames looped 
training_data=[]
hwin_cs2 = win32gui.FindWindow(0, ('Counter-Strike 2'))
img_small = grab_window(hwin_cs2, game_resolution=csgo_game_res, SHOW_IMAGE=False)

while True:
    loop_start_time = time.time()
    n_loops += 1

    time.sleep(1)
    keys_pressed = key_check()
    if 'Q' in keys_pressed:
        # exit loop
        print('exiting...')
        break

    curr_vars={}
    
    player = pm.read_ulonglong(client + dwLocalPlayerPawn)
    obs_mode = pm.read_bytes(player + m_iObserverMode, 1)
    obs_mode_int = int.from_bytes(obs_mode, byteorder='little')
    print('obs_mode (int):', obs_mode_int)
    curr_vars['health'] = pm.read_int(player + m_iHealth)
    print('health', curr_vars['health'])
    