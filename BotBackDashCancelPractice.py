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
import MoveStates
from AcademyBot import AcademyBot
from TekkenGameState import TekkenGameState
from BotData import BotBehaviors
from NotationParser import ParseMoveList
from MatchRecorder import MatchRecorder
from CharacterData import *
from MoveInfoEnums import *
from movelist import MoveList


class BotBackDashCancelPractice(AcademyBot):

    def __init__(self, botCommands):
        super().__init__(botCommands) #Initialize Super class
        self.recorder = None #No need for a recorder
        #self.queue = [] 
        self.lastMove = None #Used to check changing movenames
        #self.NumCorrectPunished = 0 
        #self.CountOfAttempts = 0
        self.exit = False
        self.MoveFrameCount = 0 #Used to count the number of frames we've been on a move
        #self.LastBotMoveName = None
        self.States = MoveStates.MoveStates() #The Data structure to hold appropriate states
        self.States.LoadBDC() #Load the BDC states
        
    def Update(self, gameState: TekkenGameState):
        super().Update(gameState) #Update the game state
        if(self.lastMove != self.BotMove): #If the move has changed
            self.MoveFrameCount = 0 #This is the first frame we're on this move
            print("MoveName:\t" + self.BotMove)
            self.lastMove = self.BotMove #Update the last move so we can track it changing again
            if(self.States.MoveToEdge(self.lastMove)): #If the current move is allowed, print the message for that move.
                print("Message:\t" + self.States.Message)
                self.overlay.WriteToOverlay("Good")
            else:
                if(self.States.FailMessage != ""):
                    self.overlay.WriteToOverlay(self.States.FailMessage)
                else:
                    self.overlay.WriteToOverlay("Failed")
        else: #We're still in the same move
            self.MoveFrameCount += 1 #count the number of frames we're on this move
            if(self.BotMove == self.States.Start.StateName and self.MoveFrameCount > 60): #If we're still on the initial state for 1 second, restart
                self.States.GoToStart()
                self.overlay.WriteToOverlay("Starting Over")


        

                        


