from CommandRecorder import CommandRecorder
from tkinter import *
from tkinter.ttk import *
from AcademyBot import AcademyBot
from TekkenGameState import TekkenGameState
from _TekkenBotLauncher import TekkenBotLauncher
from NotationParser import ParseMoveList
from BotData import BotBehaviors

class GUI_CommandRecorder(AcademyBot):
        
    def __init__(self, bot_commands):
        super().__init__(bot_commands)
        self.GUI_Recorder = Toplevel()
        self.GUI_Recorder.wm_title("Command Recorder")
        self.GUI_Recorder.geometry(str(500) + 'x' + str(100))
        self.recorder = None
        
        self.recording = False
        self.playback = False
        
        #self.launcher = TekkenBotLauncher(AcademyBot, True)
        self.gameState = None
        
        self.InputLabel = Label(self.GUI_Recorder, text="Command")
        self.InputLabel.grid(row=0, column=0, padx=5, pady=5)
        
        self.InputBox = Text(self.GUI_Recorder, height=3, width=50)
        self.InputBox.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
        
        self.RecordButtonText = StringVar()
        self.RecordButtonText.set("Record")
        self.RecordBtn = Button(self.GUI_Recorder, textvariable=self.RecordButtonText, command=self.recordCallback)
        self.RecordBtn.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        
        #self.StopRecBtn = Button(self.GUI_Recorder, text="Stop Recording", command=self.stopRecording)
        #self.StopRecBtn.grid(row=1, column=1, padx=5, pady=5)
        
        self.TestBtn = Button(self.GUI_Recorder, text="Test Command", command=self.testCommand)
        self.TestBtn.grid(row=1, column=2, padx=5, pady=5)
        
        self.TestCommand = ""
        
    def Update(self, gameState: TekkenGameState):
        successfulUpdate = super().Update(gameState)
        if(self.recording):
            self.recorder.update_state()
        
        if(self.playback and self.botCommands.IsAvailable() and gameState.IsForegroundPID()):
#            if  self.distance > 1500:
#                self.botCommands.AddCommand(self.botCommands.ForwarddashSmall())
#            else:
            self.botCommands.AddCommand(ParseMoveList(self.testCommand))
            self.testCommand = ""
            self.playback = False

    def recordCallback(self):
        if not self.recording:
            self.record()
        else:
            self.stopRecording()
            
    def record(self):
        self.recording = True
        self.InputBox.delete("1.0", END)
        self.RecordButtonText.set("Stop Recording")
        self.recorder = CommandRecorder(self)
        
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
        self.RecordButtonText.set("Record")
        
    
    def testCommand(self):
        #print(ParseMoveList(self.InputBox.get("1.0", 'end-1c')))
        self.playback = True
        self.testCommand = self.InputBox.get("1.0", 'end-1c')
