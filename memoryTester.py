from TekkenGameState import TekkenGameReader
from collections import Counter
from contextlib import suppress

import ctypes as c
from ctypes import wintypes as w
import struct
import math

import ModuleEnumerator
import PIDSearcher
from MoveInfoEnums import *
from MemoryAddressEnum import *
from ConfigReader import ConfigReader
from MoveDataReport import MoveDataReport
import MovelistParser
import sys

k32 = c.windll.kernel32

OpenProcess = k32.OpenProcess
OpenProcess.argtypes = [w.DWORD,w.BOOL,w.DWORD]
OpenProcess.restype = w.HANDLE

ReadProcessMemory = k32.ReadProcessMemory
ReadProcessMemory.argtypes = [w.HANDLE,w.LPCVOID,w.LPVOID,c.c_size_t,c.POINTER(c.c_size_t)]
ReadProcessMemory.restype = w.BOOL

GetLastError = k32.GetLastError
GetLastError.argtypes = None
GetLastError.restype = w.DWORD

CloseHandle = k32.CloseHandle
CloseHandle.argtypes = [w.HANDLE]
CloseHandle.restype = w.BOOL

g = TekkenGameReader()
g.GetUpdatedState()
g.needReacquireModule = True
g.GetUpdatedState()
processHandle = OpenProcess(0x10, False, g.pid)




rollback_frame = 0
g.module_address = 5368709120
player_data_base_address = g.GetValueFromAddress(processHandle, g.module_address + g.player_data_pointer_offset, is64bit = True)
if player_data_base_address == 0:
    print(g.player_data_pointer_offset)
    if not g.needReaquireGameState:
        print("No fight detected. Gamestate not updated.")
    g.needReaquireGameState = True
    g.flagToReacquireNames = True
else:
    last_eight_frames = []
    second_address_base = g.GetValueFromAddress(processHandle, player_data_base_address, is64bit = True)
    for i in range(8):  # for rollback purposes, there are 8 copies of the game state, each one updatating once every 8 frames
        potential_second_address = second_address_base + (i * MemoryAddressOffsets.rollback_frame_offset.value)
        potential_frame_count = g.GetValueFromAddress(processHandle, potential_second_address +  GameDataAddress.frame_count.value)
        last_eight_frames.append((potential_frame_count, potential_second_address))

    if rollback_frame >= len(last_eight_frames):
        print("ERROR: requesting {} frame of {} long rollback frame".format(rollback_frame, len(last_eight_frames)))
        rollback_frame = len(last_eight_frames) - 1

    best_frame_count, player_data_second_address = sorted(last_eight_frames, key=lambda x: -x[0])[rollback_frame]

#        p1_bot = BotSnapshot()
#        p2_bot = BotSnapshot()

    player_data_frame = g.GetBlockOfData(processHandle, player_data_second_address, MemoryAddressOffsets.rollback_frame_offset.value)

    for offset_enum in range(0x00, 0xff):
        #p1_value = g.GetValueFromAddress(processHandle, player_data_second_address + data.value, IsDataAFloat(data))
        #p2_value = g.GetValueFromAddress(processHandle, player_data_second_address + MemoryAddressOffsets.p2_data_offset.value + data.value, IsDataAFloat(data))
        #with suppress(Exception):
        p1_value = g.GetValueFromDataBlock(player_data_frame, offset_enum, 0, IsDataAFloat(offset_enum))
        with suppress(Exception):
            print(CharacterCodes(p1_value).name)
        
            
        #p2_value = g.GetValueFromDataBlock(player_data_frame, offset_enum, MemoryAddressOffsets.p2_data_offset.value, IsDataAFloat(offset_enum))
#            p1_bot.player_data_dict[offset_enum] = p1_value
#            p2_bot.player_data_dict[offset_enum] = p2_value

    
#for offset in range(0x00, 0xFFFFF):
    #a = g.GetValueFromAddress(processHandle, g.module_address + int(offset), is64bit=False)
    #if a == 28:
       # print( hex(offset) + " Value: " + str(a))
    
