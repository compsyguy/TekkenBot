"""
A simple bot that presses buttons when emerging from block or hit stun.

"""
import time
import random
import csv
import xml.etree.ElementTree as ET
import NotationParser
import movelist
from AcademyBot import AcademyBot
from TekkenGameState import TekkenGameState
from BotData import BotBehaviors
from NotationParser import ParseMoveList
from MatchRecorder import MatchRecorder
from CharacterData import *
from MoveInfoEnums import *
from movelist import MoveList

class BotPunishTest(AcademyBot):

    def __init__(self, botCommands):
        super().__init__(botCommands)
        self.inputDelay = 0
        self.inputDelayCode = None
        self.elapsedTime = time.time()
        self.punishableMoves = None
        self.Movelist = None
        self.useMoves = None
        self.queue = []
        self.lastMove = None
        self.NumCorrectPunished = 0
        self.CountOfAttempts = 0
        self.exit = False

    def Update(self, gameState: TekkenGameState):
        super().Update(gameState)
 
        self.Movelist.shuffleGameplan()
        
        if self.botCommands.IsAvailable():

            if gameState.stateLog[-1].bot.hit_outcome in self.HitList():
                if self.lastMove:
                    print("Punished")
                    self.NumCorrectPunished = self.NumCorrectPunished + 1
                    self.Movelist.removeMoveFromGameplan(self.lastMove)
                self.lastMove = None
                if not self.Movelist.gameplan:
                    self.exit = True
                    print("Percentage of punishes: " + str((float(self.NumCorrectPunished) / float(self.CountOfAttempts)) * 100) + "%")
                    print("Total Punished: " + str(self.NumCorrectPunished))
                    print("Total Attempts: " + str(self.CountOfAttempts))
            
            BotBehaviors.BlockAllAttacks(gameState, self.botCommands)
            
            #Check to see if the bot is standing
            if gameState.stateLog[-1].bot.simple_state != (SimpleMoveStates.STANDING):
                self.FrameLastAction = self.frameCounter
            else:
                if  self.distance > 1500:
                    self.botCommands.AddCommand(self.botCommands.ForwarddashSmall())
                elif self.DetermineIfAction():
                    if len(self.queue) == 0:
                        self.lastMove = self.Movelist.getNextGameplanMove()
                    else:
                        self.lastMove = self.queue.pop(0)
                    command = self.Movelist.getMoveCommand(self.lastMove, 0)
                    print("Move: " + self.Movelist.getMoveName(self.lastMove) + "\nID: " + self.Movelist.getMoveId(self.lastMove) + "\n") 
                    if command is not None:
                        self.botCommands.AddCommand(ParseMoveList(command))
                        self.CountOfAttempts = self.CountOfAttempts + 1


    def DetermineIfAction(self):
        if self.frameCounter - self.FrameLastAction > (1*60):
            self.FrameLastAction = self.frameCounter
            return True
        return False