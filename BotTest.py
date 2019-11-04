"""
A simple bot that presses buttons when emerging from block or hit stun.

"""
import time
import random
import csv
import xml.etree.ElementTree as ET
import NotationParser
import movelist
import tkinter
from AcademyBot import AcademyBot
from TekkenGameState import TekkenGameState
from BotData import BotBehaviors
from NotationParser import ParseMoveList
from MatchRecorder import MatchRecorder
from CharacterData import *
from MoveInfoEnums import *
from movelist import MoveList


class BotTest(AcademyBot):

    def __init__(self, botCommands):
        super().__init__(botCommands)
        self.Command = None
        self.Delay = 60
        self.LastMoveName = None
#        self.FrameLastAction = 0
#        self.frameCounter = 0
        self.LastBotMoveName = None
        self.LastPlayerMoveName = None
        
    def Update(self, gameState: TekkenGameState):
        successfulUpdate = super().Update(gameState)
        if(self.overlay != None):
            self.overlay.WriteToOverlay("Stance: " + str(self.Stance))
#        print("Botmove: " + self.BotMove)
#        if self.LastMoveName != self.BotMove:
#            self.LastMoveName = self.BotMove
        #self.botCommands.AddCommand(self.botCommands.ForwarddashSmall())
        BotBehaviors.BlockAllAttacks(gameState, self.botCommands)
        currentPlayerMoveName = gameState.GetCurrentOppMoveName()
        if(currentPlayerMoveName != self.LastPlayerMoveName):
            char_id = gameState.stateLog[-1].opp.char_id
            self.LastPlayerMoveName = currentPlayerMoveName
            print(str(char_id) + ": " + self.LastPlayerMoveName)
        
        ###Testing
        test = self.OppMovelist.getMoveById(5)
        if(self.OppMovelist.DidMoveJustHappen(self.BotMoveHistory, test)):
            print("Move happened")
        return successfulUpdate
            
        #if self.botCommands.IsAvailable():
            #BotBehaviors.BlockAllAttacks(gameState, self.botCommands)
            #Check to see if the bot is standing




