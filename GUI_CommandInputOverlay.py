import GUI_Overlay
from tkinter import *
from tkinter.ttk import *
from MoveInfoEnums import InputDirectionCodes
from MoveInfoEnums import InputAttackCodes
from TekkenEncyclopedia import TekkenEncyclopedia
from TekkenGameState import TekkenGameReader
from TekkenGameState import BotSnapshot
i=0
j=0
in_move=0
garbage=0
maxframe=0
a=0
b=''
u=0
ipt=['','',0,0]
f = open('outputplayback.txt','w')
inputs=[]
direction=''
button=''
frames_to_hold=1

symbol_map = {
        InputDirectionCodes.u : 'u',
        InputDirectionCodes.uf: 'uf',
        InputDirectionCodes.f: 'f',
        InputDirectionCodes.df: 'df',
        InputDirectionCodes.d: 'd',
        InputDirectionCodes.db: 'db',
        InputDirectionCodes.b: 'b',
        InputDirectionCodes.ub: 'ub',
        InputDirectionCodes.N: 'N',
        InputDirectionCodes.NULL: 'NULL'

    }

double_buttons={'12' : '1+2',
                '13' : '1+3',
                '14' : '1+4',
                '23' : '2+3',
                '24' : '2+4',
                '34' : '3+4',
                '1234' :'1+2+3+4',
                '134' :'1+3+4',
                '234' :'2+3+4',
                }

class TextRedirector(object):
    def __init__(self, canvas, height):
        pass

    def write(self, str):
        pass


class GUI_CommandInputOverlay(GUI_Overlay.Overlay):


    symbol_map = {

        #InputDirectionCodes.u: '⇑',
        #InputDirectionCodes.uf: '⇗',
        #InputDirectionCodes.f: '⇒',
        #InputDirectionCodes.df: '⇘',
        #InputDirectionCodes.d: '⇓',
        #InputDirectionCodes.db: '⇙',
        #InputDirectionCodes.b: '⇐',
        #InputDirectionCodes.ub: '⇖',
        #InputDirectionCodes.N: '★',

        InputDirectionCodes.u : 'u',
        InputDirectionCodes.uf: 'uf',
        InputDirectionCodes.f: 'f',
        InputDirectionCodes.df: 'df',
        InputDirectionCodes.d: 'd',
        InputDirectionCodes.db: 'db',
        InputDirectionCodes.b: 'b',
        InputDirectionCodes.ub: 'ub',
        InputDirectionCodes.N: 'N',
        InputDirectionCodes.NULL: 'NULL'

    }


    def __init__(self, master, launcher):


        GUI_Overlay.Overlay.__init__(self, master, (1200, 86), "Tekken Bot: Command Input Overlay")

        self.launcher = launcher

        self.canvas = Canvas(self.toplevel, width=self.w, height=self.h, bg='black', highlightthickness=0, relief='flat')

        self.canvas.pack()

        self.length = 60
        self.step = self.w/self.length
        for i in range(self.length):
            self.canvas.create_text(i * self.step + (self.step / 2), 8, text = str(i), fill='snow')
            self.canvas.create_line(i * self.step, 0, i * self.step, self.h, fill="red")

        self.canvas

        self.redirector = TextRedirector(self.canvas, self.h)\

        self.stored_inputs = []
        self.stored_cancels = []


    def update_state(self):
        
        self.launcher.gameState.stateLog[-1].is_player_player_one = True #TURN ANALYSE 2P SIDE

        GUI_Overlay.Overlay.update_state(self)
        if self.launcher.gameState.stateLog[-1].is_player_player_one: #player one player two
            input = self.launcher.gameState.stateLog[-1].bot.GetInputState()
            cancelable = self.launcher.gameState.stateLog[-1].bot.is_cancelable
            bufferable = self.launcher.gameState.stateLog[-1].bot.is_bufferable
            parry1 = self.launcher.gameState.stateLog[-1].bot.is_parry_1
            parry2 = self.launcher.gameState.stateLog[-1].bot.is_parry_2
        else:
            input = self.launcher.gameState.stateLog[-1].opp.GetInputState()
            cancelable = self.launcher.gameState.stateLog[-1].opp.is_cancelable
            bufferable = self.launcher.gameState.stateLog[-1].opp.is_bufferable
            parry1 = self.launcher.gameState.stateLog[-1].opp.is_parry_1
            parry2 = self.launcher.gameState.stateLog[-1].opp.is_parry_2
        frame_count = self.launcher.gameState.stateLog[-1].frame_count

        #print(input)
        self.update_input(input, self.color_from_cancel_booleans(cancelable, bufferable, parry1, parry2))

###############################     RECORDER    ############################################

        character=self.launcher.gameState.stateLog[-1].bot.character_name
        f = open('.\\xml_maker\\'+character.capitalize()+'_outputplayback.txt','a')

        #global declarations are needed because this class is called iteratively by update()
        global in_move
        global i
        global garbage
        global j
        global maxframe
        global a
        global b
        global ipt
        global inputs
        global u
        global direction
        global button
        global frames_to_hold
        global started


        def formatter(direction,button,frame,fth=1):
            """ Write a tuple of 3 elements : button or direction, frame interval, frame to hold """
            frame=str(frame)
            fth=str(fth)

            if len(button)>1:
                button=double_buttons[button]


            if ( (direction == 'N')  and (button == '') ) : #Neutral frames : N,''
                f.write(direction+' '+frame+' '+fth+"\n")

            elif ( (direction != 'N')  and (button != '') ) :
                f.write(direction+'+'+button+' '+frame+' '+fth+'\n')

            elif (button==''):
                f.write(direction+' '+frame+' '+fth+"\n") #df

            elif (direction=='N') :
                f.write('+'+button+' '+frame+' '+fth+"\n") #+4



        if input[0] == InputDirectionCodes.NULL : #Start of the playback #playback InputAttackCode.NULL

            i=0 #Frame number, reset from previous playback
            in_move = False #Previous move ended
            print("START RECORDING \n")

            """ N,''... inputs in between these blocks => Ignored """



        if( ( (input[0] != InputDirectionCodes.N) or (input[1] != InputAttackCodes.N) ) and (input[0] != InputDirectionCodes.NULL)):
            i+=1
            if not in_move :
                f.write("#"+"\n")
            in_move = True

            """ Allow to ignores neutral frames between a NULL input (start), and the very first input of one move """

            direction=symbol_map[input[0]]
            button=input[1].name.replace('x', '').replace('N', '') # Replace codes by understandable name


            if (direction == ipt[0] and button == ipt[1] and (i-ipt[2]) == 1):
                frames_to_hold+=1
            else :
                frames_to_hold=1


            ipt=[direction,button,i,frames_to_hold] #Saves the frame as a list of 4 items
            print(ipt)
            formatter(ipt[0],ipt[1],ipt[2],ipt[3])
            #i=i+1 #We move to next frame
            #i+=1

        elif( (in_move== True) and ( (input[0] == InputDirectionCodes.N) and (input[1] == InputAttackCodes.N) ) ):
            i+=1 #Neutrals between inputs (delay)

            """ This block gathers neutral inputs (N,'') between two inputs that aren't neutrals during the move """

            direction=symbol_map[input[0]]
            button=input[1].name.replace('x', '').replace('N', '') #N

            ipt=[direction,button,i]
            #print(ipt)
            formatter(ipt[0],ipt[1],ipt[2])


###########################     END RECORDER     ################################


    def color_from_cancel_booleans(self, cancelable, bufferable, parry1, parry2):
        if parry1:
            fill_color = 'orange'
        elif parry2:
            fill_color = 'yellow'
        elif bufferable:
            fill_color = 'MediumOrchid1'
        elif cancelable:
            fill_color = 'SteelBlue1'
        else:
            fill_color = 'firebrick1'
        return fill_color

    def update_input(self, input, cancel_color):
        input_tag = "inputs"
        #print(input)
        self.stored_inputs.append(input)

        self.stored_cancels.append(cancel_color)
        if len(self.stored_inputs) >= self.length: #prend la window et store 60 inputs
            self.stored_inputs = self.stored_inputs[-self.length:]
            self.stored_cancels = self.stored_cancels[-self.length:]
            #print(self.stored_inputs)
            if input != self.stored_inputs[-2]:
                self.canvas.delete(input_tag)

                #print(self.stored_inputs)
                for i, (direction_code, attack_code, rage_flag) in enumerate(self.stored_inputs):
                    self.canvas.create_text(i * self.step + (self.step / 2), 30, text=GUI_CommandInputOverlay.symbol_map[direction_code], fill='snow',  font=("Consolas", 20), tag=input_tag)
                    self.canvas.create_text(i * self.step + (self.step / 2), 55, text=attack_code.name.replace('x', '').replace('N', ''), fill='snow',  font=("Consolas", 12), tag=input_tag)
                    x0 = i * self.step + 4
                    x1 = x0 + self.step - 8
                    self.canvas.create_rectangle(x0, 70, x1, self.h - 5, fill=self.stored_cancels[i], tag=input_tag)
