from tkinter import *
from tkinter.ttk import *

class AssignCommandsToMoves(Tk):
    def __init__(self, character):
        Tk.__init__(self)
        self.wm_title("Assign Commands To Moves")
        self.geometry(str(720) + 'x' + str(720))

        self.character = character

        Style().theme_use('alt')
        self.TestButton = Button(self, text="Test", command = self.test_command)
        self.TestButton.place(x=20, y=20, width=120, height=25)

        self.Canvas = Canvas(self, width=500, height=650)
        self.Canvas.place(x=0, y=60)
        self.MovelistFrame = Frame(self.Canvas, width=500, height=650, relief=SUNKEN)
        #self.MovelistFrame.place(x=0, y=60)
        self.MovelistFrame.pack()
        self.scrollbar = Scrollbar(self.MovelistFrame, orient="vertical", command=self.Canvas.yview)
        self.Canvas.configure(yscrollcommand=self.scrollbar.set)
        #self.scrollbar.place(x=0, y=100)
        self.scrollbar.pack()

        for i in range(50):
            Box = Label(self.MovelistFrame, text="Test ")
            Box.place(x=15, y=(30 * i)+15)

        #self.protocol("WM_DELETE_WINDOW", self.on_closing)
    def test_command(self):
        pass

    
if __name__ == '__main__':
    app = AssignCommandsToMoves('Kazuya')
    app.mainloop()