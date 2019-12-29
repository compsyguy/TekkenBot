from CommandRecorder import CommandRecorder
from tkinter import *
from tkinter.ttk import *
from AcademyBot import AcademyBot
from TekkenGameState import TekkenGameState
from _TekkenBotLauncher import TekkenBotLauncher
from NotationParser import ParseMoveList
from BotData import BotBehaviors
import win32.user32 as user32
import movelist

class GUI_CommandRecorder(AcademyBot):
        
    def __init__(self, bot_commands):
        super().__init__(bot_commands)
        self.GUI_Recorder = Toplevel()
        self.GUI_Recorder.wm_title("Command Recorder")
        self.GUI_Recorder.geometry(str(500) + 'x' + str(200))
        self.recorder = None
        
        self.recording = False
        self.playback = False
        
        #self.launcher = TekkenBotLauncher(AcademyBot, True)
        self.gameState = None
        
        #Command label
        self.InputLabel = Label(self.GUI_Recorder, text="Command")
        self.InputLabel.grid(row=0, column=0, padx=5, pady=5)
        #Command Input Box
        self.InputBox = Text(self.GUI_Recorder, height=3, width=50)
        self.InputBox.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        
        #Record Button
        self.RecordButtonText = StringVar()
        self.RecordButtonText.set("Record")
        self.RecordBtn = Button(self.GUI_Recorder, textvariable=self.RecordButtonText, command=self.recordCallback)
        self.RecordBtn.grid(row=1, column=0, columnspan=1, padx=5, pady=5)
        
        #Test Button
        self.TestBtn = Button(self.GUI_Recorder, text="Test Command", command=self.testCallback)
        self.TestBtn.grid(row=1, column=1, padx=5, pady=5)
        
        #Save Button
        self.SaveBtn = Button(self.GUI_Recorder, text="Save Movelist", command=self.saveMovelist)
        self.SaveBtn.grid(row=1, column=2, padx=5, pady=5)
        
        #Move Name Label
        self.MoveNameLabel = Label(self.GUI_Recorder, text="Move Names")
        self.MoveNameLabel.grid(row=2, column=0, padx=5, pady=5)
        
        self.MoveNameBox = Text(self.GUI_Recorder, height=3, width=50)
        self.MoveNameBox.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
        
        
        self.testCommand = ""
        
        self.movelistIndex = 0
        
        self.OverlayPrefix = ""
        
    def Update(self, gameState: TekkenGameState):
        successfulUpdate = super().Update(gameState)
        if(self.recording):
            self.recorder.update_state()
        
        self.checkKeyPresses()
        
        self.movelistIds = self.Movelist.GetAllMoveIds()
        self.workingMove = self.Movelist.getMoveById(self.movelistIds[self.movelistIndex])
        
        self.overlay.WriteToOverlay(self.OverlayPrefix + ": " + self.Movelist.getMoveName(self.workingMove))
        
        
        if(self.playback and self.botCommands.IsAvailable() and gameState.IsForegroundPID()):
#            if  self.distance > 1500:
#                self.botCommands.AddCommand(self.botCommands.ForwarddashSmall())
#            else:
            self.botCommands.AddCommand(ParseMoveList(self.testCommand))
            self.testCommand = ""
            self.playback = False

    def checkKeyPresses(self):
        if self.DidKeyGetPressed(ord('M')):
            self.testCallback()
        if self.DidKeyGetPressed(user32.VK_OEM_COMMA):
            self.previousWorkingMove()
        if self.DidKeyGetPressed(user32.VK_OEM_PERIOD):
            self.nextWorkingMove()
        if self.DidKeyGetPressed(user32.VK_OEM_2):
            self.recordCallback()


    def updateWorkingMove(self):
        self.workingMove = self.Movelist.getMoveById(self.movelistIds[self.movelistIndex])    
        self.InputBox.delete("1.0", END)
        command = self.workingMove.find('.//command').text
        if command != None:
            self.InputBox.insert(END, self.workingMove.find('.//command').text)
        else:
            self.InputBox.insert(END, "")
            
    def previousWorkingMove(self):
        if self.movelistIndex <= 0:
            self.movelistIndex = len(self.movelistIds) - 1
        else:
            self.movelistIndex -= 1
           
        self.updateWorkingMove()

    def nextWorkingMove(self):
        if self.movelistIndex >= len(self.movelistIds) - 1:
            self.movelistIndex = 0
        else:
            self.movelistIndex += 1
        
        self.updateWorkingMove()

    def recordCallback(self):
        if not self.recording:
            self.record()
        else:
            self.stopRecording()
            
    def record(self):
        self.recording = True
        self.InputBox.delete("1.0", END)
        self.MoveNameBox.delete("1.0", END)
        self.RecordButtonText.set("Stop Recording")
        self.recorder = CommandRecorder(self)
        self.OverlayPrefix = "Recording"
        
    def stopRecording(self):
        self.recording = False
        if(self.recorder != None):
            playbackrecord=[]
            for line in self.recorder.f.splitlines():
                playbackrecord.append(line.rstrip().split(' '))
                
            playbackrecord.append("#")
            #playbackrecord = self.recorder.parser(playbackrecord)
            #print(playbackrecord)
            move = self.recorder.move_process(playbackrecord)
            
            #move = playbackrecord
            #print(playbackrecord)
            #for i in playbackrecord:
            #    if i != None :
            #        for j in i :
            #            move += str(j[0]) + ', '
            #        move += '\n'
            
            
            if(move != None):
                self.InputBox.insert(END, move)
                
            
            
            extra_info = self.recorder.extra_process()
            first_line = True
            for info in extra_info:
                if first_line:
                    for type in info:
                        self.MoveNameBox.insert(END, type + "\t")
                    self.MoveNameBox.insert(END, "\n")
                    first_line = False
                    
                for type in info:
                    self.MoveNameBox.insert(END, str(info[type]) + "\t")
                    
                self.MoveNameBox.insert(END, "\n")
                                
        self.RecordButtonText.set("Record")
        self.OverlayPrefix = "Stopped Recording"
    
    def testCallback(self):
        #print(ParseMoveList(self.InputBox.get("1.0", 'end-1c')))
        self.playback = True
        self.testCommand = self.InputBox.get("1.0", 'end-1c')
        self.workingMove.find('.//command').text = self.testCommand
        self.OverlayPrefix = "Testing Recording"

    def saveMovelist(self):
        self.Movelist.Save()