"""
A simple bot that presses buttons when emerging from block or hit stun.

"""
import time
import random
import csv
import xml.etree.ElementTree as ET
import NotationParser
import movelist
from Bot import Bot
from TekkenGameState import TekkenGameState
from BotData import BotBehaviors
from NotationParser import ParseMoveList
from MatchRecorder import MatchRecorder
from CharacterData import *
from MoveInfoEnums import *
from movelist import MoveList
from GUI_TestOverlay import GUI_TestOverlay

class debugbot(Bot):

    def __init__(self, botCommands):
        super().__init__(botCommands)
        self.inputDelay = 0
        self.inputDelayCode = None
        self.gameplan = None
        self.overlay = GUI_TestOverlay(self, self)
        self.overlay.WriteToOverlay("Test")
#        self.gameState = TekkenGameState()

    def Update(self, gameState: TekkenGameState):
        successfulUpdate = gameState.Update()
        if gameState.IsGameHappening():
			#debugging
#            if(self.botSimpleState != gameState.stateLog[-1].bot.simple_state.name):
#                self.botSimpleState = gameState.stateLog[-1].bot.simple_state.name
            #print("Bot Simple State: " + gameState.stateLog[-1].bot.simple_state.name)
            self.overlay.WriteToOverlay("Bot Simple State: " + gameState.stateLog[-1].bot.simple_state.name)
        
        BotBehaviors.Basic(gameState, self.botCommands)

        if gameState.WasFightReset():
            self.botCommands.ClearCommands()
            self.gameplan = None

        if self.gameplan == None :
            char_id = gameState.GetBotCharId()
            if char_id != None:
                self.gameplan = GetGameplan(char_id)
        
        if self.botCommands.IsAvailable():            
            BotBehaviors.BlockAllAttacks(gameState, self.botCommands)


    def DetermineIfAction(self):
        if self.frameCounter - self.FrameLastAction > (1*60):
            self.FrameLastAction = self.frameCounter
            return True
        return False
    def SetFrameTrapCommandFromNotationString(self, notation: str):
				
        try:
            self.response = ParseMoveList(">, " + notation + ", >>")
            #print(self.response)
        except:
            print("Could not parse move: " + str(notation))

    def Record(self):
        self.recorder = MatchRecorder()

    def Stop(self):
        notation = self.recorder.GetInputAsNotation()
        #commands = self.recorder.GetInputAsCommands()
        #self.botCommands.ClearCommands()
        #self.botCommands.AddCommand(commands)
        self.recorder = None
        return notation

def getMoves(char_id):
    directory = "TekkenData/Movelists/"
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):
            #print(os.path.join(directory, filename))
            data_file = ET.parse(os.path.join(directory, filename))
            char_root = data_file.getroot()
            if int(char_id) == int(char_root.attrib['id']):
                print('Move list located: ' + char_root.attrib['name'])
#                for move in char_root.findall("./moves/move"):
#                    print(move.findall("command")[0].text)
                return char_root[0]
    print("Movelist not found for char_id: " + str(char_id) + " Using default Movelist.")
    return 

def getPunishableMoves(moves):
    punishableMoves = []
    for move in moves:
        if move.find("tags/Punishable") is not None:
            punishableMoves.append(move)
    return punishableMoves

def getCommand(move):
    command = move.find("command")
    return command.text