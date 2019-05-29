"""
The parent class for academy bots.

"""
from Bot import Bot
import time
import xml.etree.ElementTree as ET
import NotationParser
import movelist
import tkinter
from TekkenGameState import TekkenGameState
from NotationParser import ParseMoveList
from movelist import MoveList
from BotData import BotBehaviors
from CharacterData import *
from MoveInfoEnums import *

class AcademyBot(Bot):
    def __init__(self, botCommands):
        super().__init__(botCommands)
        self.frameCounter = 0
        self.FrameLastAction = 0        
        self.distance = 0
        self.gameplan = None
        self.Movelist = None
        self.Stance = None
        self.overlay = None
        self.recorder = None
        self.BotMove = None

    def Update(self, gameState: TekkenGameState):
        BotBehaviors.Basic(gameState, self.botCommands)
        if self.gameplan == None :
            char_id = gameState.GetBotCharId()
            print("Testing Char ID: " + str(char_id))
            if char_id != None:
                self.gameplan = GetGameplan(char_id)
                self.Movelist = MoveList(char_id)
                self.useMoves = self.Movelist.allMoves
                self.Movelist.getGameplan(1)

        if gameState.WasFightReset():
            self.botCommands.ClearCommands()
            self.gameplan = None

        if gameState.IsGameHappening():
            self.frameCounter += 1
            self.distance = gameState.GetDist()
            self.BotMove = gameState.GetCurrentBotMoveName()            
            Stance = self.Movelist.GetStanceFromGameMove(self.BotMove)
            if(Stance != None):
                self.Stance = Stance            
        
