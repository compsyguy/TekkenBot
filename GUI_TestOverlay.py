import GUI_Overlay
from tkinter import *
from tkinter.ttk import *
from GUI_Overlay import CurrentColorScheme, ColorSchemeEnum
import time
from _FrameDataLauncher import FrameDataLauncher

class OverlayApp(Tk):
    def __init__(self):
        self.test = True
        Tk.__init__(self)
        self.wm_title("Tekken Bot Prime")
        self.count = 0
        self.launcher = FrameDataLauncher(False)
        self.overlay = GUI_TestOverlay(self, self.launcher)
        self.LastOutput = ""
        self.LastMove = ""
        self.overlay.update_location()
        self.CurrentStance = "Standing"
        self.NeutralStances = [
            'Universal_32769',
        ]
        
        self.FlamingoStances = [
            'Hw_lk00F',
            'Gpe_lk02LF',
        ]
        
        self.update_launcher()
        
    def on_closing(self):
        self.destroy()
        
    def update_stance(self):
        try:
            movename = self.launcher.gameState.GetCurrentBotMoveName()
        except:
            movename = ""
        if self.CurrentStance == "Standing":
            if movename in self.FlamingoStances:
                self.CurrentStance = "Flamingo"
                return True
        else:
            if movename in self.NeutralStances:
                self.CurrentStance = "Standing"
                return True
        return False
        
        
    def update_launcher(self):
        time1 = time.time()
        successful_update = self.launcher.Update()
        output = "Do 1,1,3,3\n"
        #output = self.launcher.gameState.GetCurrentBotMoveName()
        if(output != self.LastOutput):
            self.overlay.WriteToOverlay(output + "\n")
            self.LastOutput = output

        try: 
            movename = self.launcher.gameState.GetCurrentBotMoveName()
        except:
            movename = ""

        
        if self.update_stance():
            self.overlay.WriteToOverlay('Stance: ' + self.CurrentStance + '\n')
        
#        if movename != self.LastMove:
#            self.overlay.WriteToOverlay("Movename: " + movename + "\n")
#            self.LastMove = movename

#        if movename == "Hw_llkhlk":
#            self.overlay.WriteToOverlay("Congrats!!\n")
            
#        if len(output) > 0:
#            self.overlay.WriteToOverlay(output)
         
        if self.overlay != None:
            #self.overlay.update_location()
            if successful_update:
                self.overlay.update_state()
        #self.graph.update_state()
        time2 = time.time()
        elapsed_time = 1000 * (time2 - time1)
        if self.launcher.gameState.gameReader.HasWorkingPID():
            self.after(max(2, 8 - int(round(elapsed_time))), self.update_launcher)
        else:
            self.after(1000, self.update_launcher)

class GUI_TestOverlay(GUI_Overlay.Overlay):
    def __init__(self, master, launcher, size, position):

        GUI_Overlay.Overlay.__init__(self, master, size, "Tekken Bot: Test Overlay")

        #self.launcher = FrameDataLauncher(self.enable_nerd_data)
        self.launcher = launcher
        
        Grid.columnconfigure(self.toplevel, 0, weight=1)
        Grid.rowconfigure(self.toplevel, 0, weight=1)

        self.canvas = Canvas(self.toplevel, width=self.w, height=self.h, bg='white', highlightthickness=0, relief='flat')
        self.canvas.configure()
        self.canvas.pack()

        self.textbox_width = 10
        self.TextBox = Text(self.canvas, font=("Consolas, 20"), wrap=NONE, highlightthickness=0, pady=0, relief='flat', height=2)
        self.TextBox.grid(row=0, column=0, sticky=N + S + W + E)
        self.TextBox.configure(background=self.background_color)
        self.TextBox.configure(foreground=CurrentColorScheme.dict[ColorSchemeEnum.system_text])
        
        self.toplevel.geometry('%dx%d+%d+%d' % (size[0], size[1], position[0], position[1]))
        self.TextBox.configure(state="normal")
        self.TextBox.configure(state="disabled")
        #self.TextBox.insert("end", "Testing Overly Interface\n")
        self.TextBox.see("end")
        
        
    def WriteToOverlay(self, text):
        self.TextBox.configure(state="normal")
        #self.TextBox.delete("1.0", "2.0")
        self.TextBox.insert(INSERT, text + "\n")
        self.TextBox.see("end")
        self.TextBox.configure(state="disabled")
    
    def on_closing(self):
        self.destroy()
        
    def update_location(self):
        if not self.is_draggable_window:
            tekken_rect = self.launcher.gameState.gameReader.GetWindowRect()
            if tekken_rect != None:
                x = (tekken_rect.right + tekken_rect.left) / 2 - self.w / 2
                y = (tekken_rect.bottom - tekken_rect.top) / 6
                self.toplevel.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))
                if not self.overlay_visible:
                    self.show()
            else:
                if self.overlay_visible:
                    self.hide()
      
      
if __name__ == '__main__':
    app = OverlayApp()
    #app.update_launcher()
    app.mainloop()    