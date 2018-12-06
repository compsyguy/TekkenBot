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


class BotTestCommand(AcademyBot):

    def __init__(self, botCommands):
        super().__init__(botCommands)
        self.Command = None
        self.Delay = 60
        self.LastMoveName = None
#        self.FrameLastAction = 0
#        self.frameCounter = 0
        
    def Update(self, gameState: TekkenGameState):
        super().Update(gameState)
        if self.LastMoveName != self.BotMove:
            self.LastMoveName = self.BotMove
            #print(self.BotMove)
            
            
        if self.botCommands.IsAvailable():
            BotBehaviors.BlockAllAttacks(gameState, self.botCommands)
            #Check to see if the bot is standing
            if gameState.stateLog[-1].bot.simple_state != (SimpleMoveStates.STANDING):
                self.FrameLastAction = self.frameCounter
            else:
                if  self.distance > 1500:
                    self.botCommands.AddCommand(self.botCommands.ForwarddashSmall())
                elif self.DetermineIfAction():
                    if self.Command is not None:
                        if(isinstance(self.Command, list)):
                            Command = self.Command.pop(0)
                        else:
                            Command = self.Command
                        print(Command)
                        self.overlay.WriteToOverlay(Command)
                        self.botCommands.AddCommand(ParseMoveList(Command))
                        
    def DetermineIfAction(self):
        if self.frameCounter - self.FrameLastAction > (self.Delay):
            self.FrameLastAction = self.frameCounter
            return True
        return False


    def Stop(self):
        #notation = self.recorder.GetInputAsNotation()
        #commands = self.recorder.GetInputAsCommands()
        #self.botCommands.ClearCommands()
        #self.botCommands.AddCommand(commands)
        #self.recorder = None
        return notation

