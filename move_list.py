"""
move_list

This is a refactored move_list class. 
Included in this file is a move class.

The goal is to make using this less dependent on interacting with the XML directly.
"""

import xml.etree.ElementTree as ET
import xml.dom.minidom
import os
import NotationParser
from NotationParser import ParseMoveList

class input_directions(Enum):
    u = 0
    f = 1
    d = 2
    b = 3
    
class attack_buttons(Enum):
    lp = 1
    rp = 2
    lk = 3
    rk = 4
    rage_art = 5

class move_node:
    def __init__(self):
        self.char_id = 0                #The Internal Tekken Character ID the move belongs to
        self.directions[input_directions.u] = False            
        self.directions[input_directions.f] = False
        self.directions[input_directions.d] = False
        self.directions[input_directions.b] = False
        
        self.buttons[attack_buttons.lp] = False
        self.buttons[attack_buttons.rp] = False
        self.buttons[attack_buttons.lk] = False
        self.buttons[attack_buttons.rk] = False
        self.buttons[attack_buttons.rage_art] = False
        
        self.pointer_one = None
        self.pointer_two = None
        self.number_one = None
        self.number_two = None
        self.unknown_bool = None
        self.cancel_window_1 = None
        self.cancel_window_2 = None
        self.move_id = None
        self.active_codes = None    #see MovelistParser.py line 261: class ActiveCodes(Enum)
        
        self.move_name = ""
        
        self.cab_be_done_from_neutral = False #see MovelistParser.py line 137: if node.cancel_window_1 >= 0x7FFF:

class move:

    def __init__(self):
        self.char_id = 0                #The Internal Tekken Character ID the move belongs to
        self.xml_id = 0                 #The XML ID
        self.notation = ""              #The human readable noation for the move
        self.tekken_move_name = ""      #The internal Tekken Move NameError
        self.stance = ""                #The stance the move is in
        self.bot_command = ""           #The command for Tekken Bot's use
        self.bot_parsed_command = ""    #The parsed command that gets sent to the bot
        self.on_block = ""              #The frame advantage/disadvantage on block
        self.on_hit = ""                #The frame advantage/disadvantage on hit
        self.on_ch = ""                 #The frame advantage/disadvantage on counter hit
        self.hit_level = ""             #The hit level of the move
        self.damage = ""                #The damage of the move
        self.start_up = ""              #The start up frames of the move
        self.rage_art = False           #Flag for rage art
        self.rage_drive = False         #Flag for rage drive
        self.homing = False             #Flag for homing
        self.tail_spin = False          #Flag for tail spin
        self.api_nid = 0                #Tekken.academy API node id
        