"""
A stop gap for testing punisher bot until we get a nicer, unifed bot interface

"""

import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
import requests
from movelist import MoveList
from tkinter import *
from tkinter.ttk import *
from _TekkenBotLauncher import TekkenBotLauncher
from BotFrameTrap import BotFrameTrap
from BotPunisher import BotPunisher
from BotPunishPractice import BotPunishPractice 
from BotPunishTest import BotPunishTest
from BotTestCommand import BotTestCommand
from BotTest import BotTest
from BotBackDashCancelPractice import BotBackDashCancelPractice
from GUI_CommandRecorder import GUI_CommandRecorder
import sys
from GUI_TestOverlay import GUI_TestOverlay
#from GUI_CommandInputOverlay2 import GUI_CommandInputOverlay
from CommandRecorder import CommandRecorder

class GUI_TekkenAcademy(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.wm_title("Tekken Bot")
        self.geometry(str(720) + 'x' + str(720))

        Style().theme_use('alt')
        self.menu = Menu(self)
        self.configure(menu=self.menu)
        
        self.tekken_bot_menu = Menu(self.menu)
        self.tekken_bot_menu.add_command(label="Punish Practice Bot", command=self.switchToPractice)
        self.tekken_bot_menu.add_command(label="Punish Test Bot", command=self.switchToPunishTestBot)
#        self.tekken_bot_menu.add_command(label="Back Dash Cancel", command=self.switchToBDCBot)
#        self.tekken_bot_menu.add_command(label="Test Bot", command=self.switchToTest)
        self.tekken_bot_menu.add_command(label="Stop Bots", command=self.stopBot)
#        self.tekken_bot_menu.add_command(label="Update Movelists", command=self.updateMovelists)
#        self.tekken_bot_menu.add_command(label="Edit Movelists", command=self.editMovelists)
        self.tekken_bot_menu.add_command(label="Test Movelist", command=self.testMoveList)
        self.tekken_bot_menu.add_command(label="Clear History", command=self.clearHistory)
        self.tekken_bot_menu.add_command(label="Record", command=self.record)
        self.tekken_bot_menu.add_command(label="GUI Record", command=self.gui_record)
        self.tekken_bot_menu.add_command(label="Print Record", command=self.printrecord)
        self.menu.add_cascade(label="Tekken Bot", menu=self.tekken_bot_menu)

        #self.launcher = TekkenBotLauncher(BotPunishTest , False)
        self.launcher = None
        self.overlay = None
        self.recorder = None
        #self.overlay.update_location()

        #Overlay text redirection
        self.text = Text(self, wrap="word")
        self.stdout = sys.stdout
        self.var_print_frame_data_to_file = BooleanVar(value=False)
        sys.stdout = TextRedirector(self.text, sys.stdout, self.write_to_overlay, self.var_print_frame_data_to_file, "stdout")
        self.stderr = sys.stderr
        sys.stderr = TextRedirector(self.text, sys.stderr, self.write_to_error, "stderr")
        self.text.tag_configure("stderr", foreground="#b22222")
        
        self.text.grid(row = 2, column = 0, columnspan=2, sticky=N+S+E+W)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

		
        try:
            with open("TekkenData/tekken_acadamy_readme.txt") as fr:
                lines = fr.readlines()
            for line in lines: print(line)
        except:
            print("Error reading readme file.")
        #self.overlay.hide()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_launcher(self):
        try:
            self.update()
        finally:
            self.stopBot
            
        self.after(5, self.update_launcher)

    def update(self):
        successful_update = False
        if(self.launcher != None):
            if (self.launcher.gameState.IsForegroundPID() and self.overlay != None):
                self.overlay.show()
            successful_update = self.launcher.Update()
        if(self.overlay != None):
            self.overlay.update_location()
        if(self.recorder != None and successful_update):
            self.recorder.update_state()
        
    def record(self):
        self.launcher = TekkenBotLauncher(BotTest, True)
        self.recorder = CommandRecorder(self.launcher)
        
    def gui_record(self):
        self.launcher = TekkenBotLauncher(GUI_CommandRecorder, True)
        self.launcher.botBrain.gameState = self.launcher.gameState
    
    def printrecord(self):
        #self.recorder.print_f()
        self.recorder.parse('Recorded')
    
    def switchToPractice(self):
        print("Switching to Practice")
        self.launcher = TekkenBotLauncher(BotPunishPractice, False)
        self.overlay = GUI_TestOverlay(self, self.launcher, (1000, 35), (450, 170))
        self.launcher.botBrain.overlay = self.overlay
        self.overlay.WriteToOverlay("Switching to Practice")

    def switchToPunishTestBot(self):
        print("Switching to Punish Test Bot")
        self.launcher = TekkenBotLauncher(BotPunishTest, False)
        self.overlay = GUI_TestOverlay(self, self.launcher, (1000, 35), (450, 170))
        self.launcher.botBrain.overlay = self.overlay
        
    def switchToBDCBot(self):
        print("Switching to BDC Practice Bot")
        self.launcher = TekkenBotLauncher(BotBackDashCancelPractice, True)
        self.overlay = GUI_TestOverlay(self, self.launcher, (1000, 35), (450, 170))
        self.launcher.botBrain.overlay = self.overlay
        self.overlay.WriteToOverlay("Switching to Back Dash Cancelling Practice")

    def switchToTest(self):
        print("Switching to Test Bot")
        self.launcher = TekkenBotLauncher(BotTest, False)
        self.overlay = GUI_TestOverlay(self, self.launcher, (1000, 35), (450, 170))
        self.launcher.botBrain.overlay = self.overlay

    def testMoveList(self):
        print("Switching to Test Movelist")
        self.launcher = TekkenBotLauncher(BotTestCommand, False)
        self.overlay = GUI_TestOverlay(self, self.launcher, (1000, 35), (450, 170))
        self.launcher.botBrain.overlay = self.overlay

#        character=self.launcher.gameState.stateLog[-1].bot.character_name
        character = "Akuma"
        charId = self.GetCharacterId(character)
        movelist = MoveList(charId)
        moves = movelist.GetAllMoveIds()
        moveCommands = []
        for id in moves:
            print(id)
            move = movelist.getMoveById(id)
            moveCommands.append(movelist.getMoveCommand(move))
            
        self.launcher.botBrain.Command = moveCommands
        self.launcher.botBrain.Delay = 60

    def stopBot(self):
        print("Stopping Bots")
        self.launcher = None

    def updateMovelists(self):
        dir = "TekkenData\Movelists"
        for filename in os.listdir(dir):
            if filename.endswith(".xml"):
                data_file = ET.parse(os.path.join(dir, filename))
                char_root = data_file.getroot()
                try:
                    url = 'http://www.seattletekken.com/modules/academy/src/characters/'
                    char = data_file.getroot().attrib['name']
                    r = requests.get(url + char + '/movelist/movelist.xml')
                except:
                    raise Exception("Can't load xml from website for " + char)

                if r.ok:
                    new_file = ET.fromstring(r.text)
                    if new_file.attrib['version'] > data_file.getroot().attrib['version']:
                        try:
                            os.rename(os.path.join(dir, filename), os.path.join(dir, "xml backups", char + "-" + data_file.getroot().attrib['version'] + ".xml"))
                            print("Retrieved updated movelist for " + char)
                        except:
                            raise Exception("Can't backup file")

                        xmlFile = xml.dom.minidom.parseString(ET.tostring(new_file))
                        f = open(os.path.join(dir, filename), "w")
                        f.write(xmlFile.toprettyxml(newl=''))
                        f.close()

                    else:
                        print("Movelist for " + char + " already at current version.")
                    
    def editMovelists(self):
        self.launcher = TekkenBotLauncher(BotTestCommand, False)
        self.overlay = GUI_TestOverlay(self, self.launcher, (1000, 35), (450, 170))
        self.launcher.botBrain.overlay = self.overlay

        win = Toplevel()
#        canvas = Canvas(win, bd=0, width=720, height=720)
#        canvas.grid(row=0, column=0, sticky=N+S+E+W)

#        frame = Frame(canvas, relief=SUNKEN, width=720, height=720)
#        frame.grid_rowconfigure(0, weight=1)
#        frame.grid_columnconfigure(0, weight=1)
#        frame.grid_propagate(0)

        #frame.pack()
#        frame.grid(row=0, column=1, sticky=N+W)

        i = 0
        self.CharIDLabel = Label(win, text="Character ID")
        self.CharIDLabel.grid(row=i, column=0)
        self.CharChoice = StringVar(win)
        self.chars = self.GetCharacterNamesWithIds()
        self.CharChoice.set('Alisa')
        self.CharID = OptionMenu(win, self.CharChoice, *self.chars)
        self.CharID.grid(row=i, column=1, sticky=W)
#        self.CharIDBox = Text(win, height=1, width=10)
#        self.CharIDBox.grid(row=i, column=1, sticky=W)
        self.CharNameBox = Text(win, height=1, width=30)
        self.CharNameBox.grid(row=i, column=2, sticky=W)
        self.CharNameBox.configure(state="disabled")
        self.LoadMovelistBtn = Button(win, text="Load Movelist", command=self.load_movelist)
        self.LoadMovelistBtn.grid(row=i, column=3)
        i = i +1

        self.MoveIDLabel = Label(win, text="Move")
        self.MoveIDLabel.grid(row=i, column=0)

#        self.MoveIdVar = StringVar(win)
#        self.MoveId = OptionMenu(win, self.MoveIdVar, ['Please select character'])
#        self.MoveId.grid(row=i, column=1, sticky=W)
        self.MoveIDBox = Text(win, height=1, width=10)
        self.MoveIDBox.grid(row=i, column=1, sticky=W)
        self.MoveNameBox = Text(win, height=1, width=30)
        self.MoveNameBox.grid(row=i, column=2, sticky=W)    
        self.MoveNameBox.configure(state="disabled")
        self.LoadMoveBtn = Button(win, text="Load Move", command=self.load_move)
        self.LoadMoveBtn.grid(row=i, column=3)
        i = i + 1

        self.CommandLabel = Label(win, text="Command")
        self.CommandLabel.grid(row=i, column=0)
        self.CommandBox = Text(win, height=1, width=50)
        self.CommandBox.grid(row=i, column=1, columnspan=2, sticky=W)
        self.CommandBox.insert(END, '+1')
        i = i + 1

        self.DelayLabel = Label(win, text="Delay")
        self.DelayLabel.grid(row=i, column=0)
        self.DelayBox = Text(win, height=1, width=50)
        self.DelayBox.grid(row=i, column=1, columnspan=2, sticky=W)
        self.DelayBox.insert(END, '60')
        i = i + 1

        self.TestButton = Button(win, text="Test", command = self.test_command)
        self.TestButton.grid(row=i, column=0)
        self.StopButton = Button(win, text="Stop", command=self.stopBot)
        self.StopButton.grid(row=i, column=1)
        self.ShortcutsButton = Button(win, text="Command Shortcuts", command=self.show_shortcuts)
        self.ShortcutsButton.grid(row=i, column=2)
        self.SaveButton = Button(win, text="Save MoveList", command=self.save_move)
        self.SaveButton.grid(row=i, column=3)
        i = i + 1
    
    def CommandChanged(self):
        print("Command Changed")

    def save_move(self):
        #print("Not currently saving")
        self.movelist.Save()

    def load_move(self):
        try:
            self.CommandBox.delete("1.0", END)
            self.EditMove = self.movelist.getMoveById(self.MoveIDBox.get("1.0", 'end-1c'))
            self.CommandBox.insert(END, self.movelist.getMoveCommand(self.EditMove, 1))
            self.MoveNameBox.configure(state="normal")
            self.MoveNameBox.delete("1.0", END)
            self.MoveNameBox.insert("1.0", self.movelist.getMoveName(self.EditMove))
            self.MoveNameBox.configure(state="disabled")
        except:
            print("Cannot load move")

    def load_movelist(self):
        #try:
            self.movelist = MoveList(self.chars[self.CharChoice.get()])
            #self.MoveId['menu'].delete(0, 'end')
            #moves = self.movelist.GetAllMoveIdsAndNames()
            #for move in moves:
                #self.MoveId['menu'].add_command(label=move, command=_setit(var, move))

            #self.movelist = MoveList(self.CharIDBox.get("1.0", 'end-1c'))
            self.CharNameBox.configure(state="normal")
            self.CharNameBox.delete("1.0", END)
            self.CharNameBox.insert("1.0", self.movelist.CharXml.getroot().attrib['name'])
            self.CharNameBox.configure(state="disabled")
        #except:
            #print("Cannot load movelist")

    def show_shortcuts(self):
        short = Toplevel()
        SCText = Text(short)
        SCText.pack()
        SCText.insert(END, "Commands are spearated by commas, If you put a number with no +, it will wait that many frames\n")
        SCText.insert(END, "EX: f+1, 5, +2\tWill hit f+1, wait 5 frames then hit 2\n")
        SCText.insert(END, "+1, +2, +3, +4:\tTap the button\n")
        SCText.insert(END, "*:\tHold the following button\n")
        SCText.insert(END, "dp:\tf,d,df\n")
        SCText.insert(END, "qcb:\td,db,b\n")
        SCText.insert(END, "qcf:\td,df,f\n")
        SCText.insert(END, "pewgf:\tf,N,df\n")
        SCText.insert(END, "ewgf:\tf,N,d,df\n")
        SCText.insert(END, "iWS:\tInstant While Standing\n")
        SCText.insert(END, "WS:\tWhile Standing\n")
        SCText.insert(END, "UF:\tJump Forward\n")
        SCText.insert(END, "ff[x]:\tFF + button where x is the delay after hitting ff\n")
        SCText.insert(END, "SSU:\tSide Step Up\n")
        SCText.insert(END, "wr:\tInstant While Running\n")
        SCText.insert(END, "rel:\tRelease All\n")
        SCText.insert(END, "-U:\tRelease Up\n")
        SCText.insert(END, "-D:\tRelease Down\n")
        SCText.insert(END, "-B:\tRelease Back\n")
        SCText.insert(END, "-F:\tRelease Forward\n")
        SCText.insert(END, "u:\tTap up\n")
        SCText.insert(END, "U:\tHold up\n")
        SCText.insert(END, "d:\tTap down\n")
        SCText.insert(END, "D:\tHold down\n")
        SCText.insert(END, "f:\tTap Forward\n")
        SCText.insert(END, "F:\tHold Forward\n")
        SCText.insert(END, "b:\tTap Back\n")
        SCText.insert(END, "B:\tHold Back\n")
        
    
    def test_command(self):
        print("Switching to Test Command")
        if self.launcher == None:
            self.launcher = TekkenBotLauncher(BotTestCommand, False)
        self.launcher.botBrain.overlay = self.overlay
        self.launcher.botBrain.Command = self.CommandBox.get("1.0", 'end-1c')
        self.launcher.botBrain.Delay = int(self.DelayBox.get("1.0", 'end-1c'))
        if self.CommandBox.edit_modified():
            print("Modified")
            self.movelist.updateMoveCommand(self.EditMove, self.CommandBox.get("1.0", 'end-1c'))
            self.CommandBox.edit_modified(False)
        

    def write_to_overlay(self, string):
        if self.overlay == None:
            self.stdout.write(string)
        
    def clearHistory(self):
        self.text.config(state=NORMAL)
        self.text.delete('1.0', END)
        self.text.configure(state="disabled")
        self.text.see('end')
        
    def write_to_error(self, string):
        self.stderr.write(string)    
    
    def on_closing(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        self.destroy()

    def GetCharacterId(self, char):
        ids = self.GetCharacterNamesWithIds()
        return ids[char.capitalize()]

    def GetCharacterNamesWithIds(self):
        return {'None':-99,
                'Akuma':32, 
                'Alisa':19, 
                'Asuka':12, 
                'Bob':31, 
                'Bryan':7, 
                'Claudio':20, 
                'Devil Jin':13,
                'Dragunov':16,
                'Eddy':35,
                'Eliza':36,
                'Feng':14,
                'Geese':43,
                'Gigas':25,
                'Heihachi':8,
                'Hwoarang':4,
                'Jack7':11,
                'Jin':6,
                'Josie':24,
                'Katarina':21,
                'Kazumi':26,
                'Kazuya':9,
                'King':2,
                'Kuma':33,
                'Lars':18,
                'Law':1, 
                'Lee':30, 
                'Leo':17,
                'Lili':15,
                'Lucky Chloe':22,
                'Master Raven':29,
                'Miguel':37,
                'Nina':28,
                'Noctis':44,
                'Paul':0,
                'Shaheen':23,
                'Steve':10,
                'Xiaoyu':5,
                'Yoshimitsu':3
                }
        
class TextRedirector(object):
    def __init__(self, widget, stdout, callback_function, var_print_frame_data_to_file,tag="stdout"):
        self.widget = widget
        self.stdout = stdout
        self.tag = tag
        self.callback_function = callback_function
        self.var_print_frame_data_to_file = var_print_frame_data_to_file

    def write(self, str):

        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
        self.widget.see('end')
        self.callback_function(str)

    def flush(self):
        pass       
        
if __name__ == '__main__':
    app = GUI_TekkenAcademy()
    app.update_launcher()
    app.mainloop()