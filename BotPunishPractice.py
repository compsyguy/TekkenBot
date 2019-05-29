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
from TekkenEncyclopedia import TekkenEncyclopedia


class BotPunishPractice(AcademyBot):

    def __init__(self, botCommands):
        super().__init__(botCommands)
        self.recorder = None
        self.queue = []
        self.lastMove = None
        self.NumCorrectPunished = 0
        self.CountOfAttempts = 0
        self.exit = False
        self.LastBotMoveName = None
        
        self.cyclopedia_p2 = TekkenEncyclopedia(False, False)
        self.cyclopedia_p1 = TekkenEncyclopedia(True, False)
        
        
    def Update(self, gameState: TekkenGameState):
        super().Update(gameState)

        self.cyclopedia_p1.Update(gameState)
        self.cyclopedia_p2.Update(gameState)
            
        print(self.cyclopedia_p1.FrameData)
        #print(gameState.GetOppMoveId())
            
        if self.botCommands.IsAvailable() and gameState.IsForegroundPID():
#            BotMove = gameState.GetCurrentBotMoveName()
#            if BotMove != self.LastBotMoveName:
#                self.LastBotMoveName = BotMove
#                print("Bot Move:" + BotMove)
            
            #if gameState.DidBotStartGettingPunishedXFramesAgo(30):
            #print(gameState.stateLog[-1].bot.hit_outcome)
            #if gameState.GetFramesSinceBotTookDamage() < 15:
            
            if gameState.stateLog[-1].bot.hit_outcome in self.HitList():
                if self.lastMove:
                    print("Punished")
#                    self.NumCorrectPunished = self.NumCorrectPunished + 1
#                    self.Movelist.removeMoveFromGameplan(self.lastMove)
                self.lastMove = None
#                if not self.Movelist.gameplan:
#                    self.exit = True
#                    print("Percentage of punishes: " + str((float(self.NumCorrectPunished) / float(self.CountOfAttempts)) * 100) + "%")
#                    print("Total Punished: " + str(self.NumCorrectPunished))
#                    print("Total Attempts: " + str(self.CountOfAttempts))
            
            BotBehaviors.BlockAllAttacks(gameState, self.botCommands)
            #Check to see if the bot is standing
            if gameState.stateLog[-1].bot.simple_state != (SimpleMoveStates.STANDING):
                self.FrameLastAction = self.frameCounter
                #print(gameState.stateLog[-1].bot.simple_state)
            else:
                if  self.distance > 1500:
                    self.botCommands.AddCommand(self.botCommands.ForwarddashSmall())
                elif self.DetermineIfAction():
                    #print(self.distance)
                    #self.botCommands.AddCommand(random.choice(self.punishableMoves))
                    #print(random.choice(self.punishableMoves))
                    if len(self.queue) == 0:
                        
                        self.lastMove = self.Movelist.getNextGameplanMove()
                        if(self.overlay != None):
                            self.overlay.WriteToOverlay(self.Movelist.getMoveName(self.lastMove) + "\t" + self.Movelist.getMoveOnBlock(self.lastMove))
                            self.FrameLastAction = self.frameCounter

                        self.queue.append(self.lastMove)
                        self.queue.append(self.lastMove)
                        self.queue.append(self.lastMove)
                    else:
                        self.lastMove = self.queue.pop(0)
                        #move = self.Movelist[-1]
                        #command = move.getMoveCommand
                        command = self.Movelist.getMoveCommand(self.lastMove)
                        print("Move: " + self.Movelist.getMoveName(self.lastMove) + "\nID: " + self.Movelist.getMoveId(self.lastMove) + "\n") 
                        #print(ParseMoveList(command))
                        if command is not None:
                            self.botCommands.AddCommand(ParseMoveList(command))
                            self.CountOfAttempts = self.CountOfAttempts + 1


                        
    def HitList(self):
        return (HitOutcome.COUNTER_HIT_STANDING, HitOutcome.COUNTER_HIT_CROUCHING, HitOutcome.NORMAL_HIT_STANDING, HitOutcome.NORMAL_HIT_CROUCHING, HitOutcome.NORMAL_HIT_STANDING_LEFT, HitOutcome.NORMAL_HIT_CROUCHING_LEFT, HitOutcome.NORMAL_HIT_STANDING_BACK, HitOutcome.NORMAL_HIT_CROUCHING_BACK, HitOutcome.NORMAL_HIT_STANDING_RIGHT, HitOutcome.NORMAL_HIT_CROUCHING_RIGHT)
        
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