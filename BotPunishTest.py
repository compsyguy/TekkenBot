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

class BotPunishTest(Bot):

    def __init__(self, botCommands):
        super().__init__(botCommands)
        self.SetFrameTrapCommandFromNotationString("+4")
        self.recorder = None
        self.inputDelay = 0
        self.inputDelayCode = None
#        self.gameState = TekkenGameState()
        self.frameCounter = 0
        self.FrameLastAction = 0
        self.elapsedTime = time.time()
        self.distance = 0
        self.gameplan = None
        self.punishableMoves = None
        self.allMoves = None
        self.useMoves = None
        self.queue = []
        self.lastMove = None
        self.NumCorrectPunished = 0
        self.CountOfAttempts = 0
        self.exit = False

    def Update(self, gameState: TekkenGameState):
        successfulUpdate = gameState.Update()
        if gameState.IsGameHappening():
            self.frameCounter += 1
            self.distance = gameState.GetDist()

        if not self.recorder == None:
            self.recorder.Update(gameState)

        BotBehaviors.Basic(gameState, self.botCommands)

        if gameState.WasFightReset():
            self.botCommands.ClearCommands()
            self.gameplan = None

        if self.gameplan == None :
            char_id = gameState.GetBotCharId()
            if char_id != None:
                self.gameplan = GetGameplan(char_id)
                #self.punishableMoves = self.gameplan.GetPunishableMoves()
                #self.allMoves = getMoves(char_id)
				#self.useMoves = getPunishableMoves(self.allMoves)
                self.allMoves = MoveList(char_id)
                self.useMoves = self.allMoves.allMoves
                self.allMoves.getGameplan(1)
                self.allMoves.shuffleGameplan()
        
        if self.botCommands.IsAvailable():
            #if gameState.DidBotStartGettingPunishedXFramesAgo(30):
            #gameState.IsOppAbleToAct()
            #if gameState.stateLog[-1].bot.IsPunish() or gameState.stateLog[-1].bot.IsBeingJuggled():
            if gameState.stateLog[-1].bot.hit_outcome in self.HitList():
            #if gameState.GetFramesSinceBotTookDamage() < 30:
                if self.lastMove:
                    print("Punished")
                    self.NumCorrectPunished = self.NumCorrectPunished + 1
                    self.allMoves.removeMoveFromGameplan(self.lastMove)
                self.lastMove = None
                if not self.allMoves.gameplan:
                    self.exit = True
                    print("Percentage of punishes: " + str((float(self.NumCorrectPunished) / float(self.CountOfAttempts)) * 100) + "%")
                    print("Total Punished: " + str(self.NumCorrectPunished))
                    print("Total Attempts: " + str(self.CountOfAttempts))
            
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
                        self.lastMove = self.allMoves.getNextGameplanMove()
                        #move = self.allMoves.getMoveById(18)
                        #self.queue.append(move)
                        #self.queue.append(move)
                    else:
                        self.lastMove = self.queue.pop(0)
                    #move = self.allMoves[-1]
                    #command = move.getMoveCommand
                    command = self.allMoves.getMoveCommand(self.lastMove, 0)
                    print("Move: " + self.allMoves.getMoveName(self.lastMove) + "\nID: " + self.allMoves.getMoveId(self.lastMove) + "\n") 
                    #print(ParseMoveList(command))
                    if command is not None:
                        self.botCommands.AddCommand(ParseMoveList(command))
                        self.CountOfAttempts = self.CountOfAttempts + 1


    def DetermineIfAction(self):
        if self.frameCounter - self.FrameLastAction > (1*60):
            self.FrameLastAction = self.frameCounter
            return True
        return False
        
    def HitList(self):
        return (HitOutcome.COUNTER_HIT_STANDING, HitOutcome.COUNTER_HIT_CROUCHING, HitOutcome.NORMAL_HIT_STANDING, HitOutcome.NORMAL_HIT_CROUCHING, HitOutcome.NORMAL_HIT_STANDING_LEFT, HitOutcome.NORMAL_HIT_CROUCHING_LEFT, HitOutcome.NORMAL_HIT_STANDING_BACK, HitOutcome.NORMAL_HIT_CROUCHING_BACK, HitOutcome.NORMAL_HIT_STANDING_RIGHT, HitOutcome.NORMAL_HIT_CROUCHING_RIGHT)
        
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