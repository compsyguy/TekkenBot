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
import win32.user32 as user32

class AcademyBot(Bot):
    def __init__(self, botCommands):
        super().__init__(botCommands)
        self.frameCounter = 0
        self.FrameLastAction = 0        
        self.distance = 0
        self.gameplan = None
        self.Movelist = None
        self.OppMovelist = None
        self.Stance = None
        self.overlay = None
        self.recorder = None
        self.BotMove = None
        self.BotMoveHistory = []

    def Update(self, gameState: TekkenGameState):
        #BotBehaviors.Basic(gameState, self.botCommands)
        if self.gameplan == None :
            char_id = gameState.GetBotCharId()
            print("Testing Char ID: " + str(char_id))
            if char_id != None:
                self.gameplan = GetGameplan(char_id)
                self.Movelist = MoveList(char_id)
                self.useMoves = self.Movelist.allMoves
                self.Movelist.getGameplan(1)
                self.OppMovelist = MoveList(gameState.stateLog[-1].opp.char_id)

        if gameState.WasFightReset():
            self.botCommands.ClearCommands()
            
        #print("Side: " + str(gameState.stateLog[-1].opp.current_side))

        if gameState.IsGameHappening():
            self.frameCounter += 1
            self.distance = gameState.GetDist()
            self.BotMove = gameState.GetCurrentBotMoveName()        
            self.AppendBotMove(gameState.GetCurrentOppMoveName())
            Stance = self.Movelist.GetStanceFromGameMove(self.BotMove)
            if(Stance != None):
                self.Stance = Stance            
        
    def AppendBotMove(self, Move):
        if(len(self.BotMoveHistory) > 600):
            self.BotMoveHistory.pop(0)
        if((not self.BotMoveHistory) or (self.BotMoveHistory[-1] != Move)):
            self.BotMoveHistory.append(Move)
            
    def DidKeyGetPressed(self, KeyCode):
        return(user32.get_async_key_state(KeyCode) & 0x1)

    def HitList(self):
        return (HitOutcome.COUNTER_HIT_STANDING, HitOutcome.COUNTER_HIT_CROUCHING, HitOutcome.NORMAL_HIT_STANDING, HitOutcome.NORMAL_HIT_CROUCHING, HitOutcome.NORMAL_HIT_STANDING_LEFT, HitOutcome.NORMAL_HIT_CROUCHING_LEFT, HitOutcome.NORMAL_HIT_STANDING_BACK, HitOutcome.NORMAL_HIT_CROUCHING_BACK, HitOutcome.NORMAL_HIT_STANDING_RIGHT, HitOutcome.NORMAL_HIT_CROUCHING_RIGHT)