from MoveInfoEnums import InputDirectionCodes
from MoveInfoEnums import InputAttackCodes
from TekkenEncyclopedia import TekkenEncyclopedia
from TekkenGameState import TekkenGameReader
from TekkenGameState import BotSnapshot

class ControllerFrame(object):
    def __init__(self, inputs):
        self.Controller = {'f': False, 
                      'd': False, 
                      'u': False,
                      'b': False, 
                      '1': False, 
                      '2': False, 
                      '3': False, 
                      '4': False}
    
        for input in inputs:
            if(input in self.Controller):
                self.Controller[input] = True
        
    def compare(self, c):
        diff = {}
        Found = False
        for input in self.Controller:
            if(self.Controller[input] == c.Controller[input]):
                #input was unchanged
                diff[input] = "same"
            elif(self.Controller[input] and not c.Controller[input]):
                #input was released
                #print("Released")
                diff[input] = "released"
                Found = True
            elif(not self.Controller[input] and c.Controller[input]):
                #input was pressed
                diff[input] = "pressed"
                #print("Pressed")
                Found = True
        
        return {"Found": Found, "Differences": diff}

    def getHeldInput(self, input):
        if(input.isalpha()):
            return input.upper()
        if(input.isnumeric()):
            return "+" + input + "*"

    def getReleaseInput(self, input):
        if(input.isalpha()):
            return "-" + input.upper()
        if(input.isnumeric()):
            return "+" + input + "-"
    
    def getInput(self, input):
        if(input.isalpha()):
            return input
        if(input.isnumeric()):
            return "+" + input
            
    def getCommand(self):
        directions = ""
        buttons = ""
        for input in self.Controller:
            if(input.isalpha()):
                directions = directions + input
            if(input.isdigit()):
                if(len(buttons) == 0):
                    buttons = buttons + "+" + input
        return directions + buttons
                    

class CommandRecorder(object):
    
    def __init__(self, launcher):
        self.launcher = launcher
        
        self.i=0
        self.j=0
        self.in_move=False
        self.garbage=0
        self.maxframe=0
        self.a=0
        self.b=''
        self.u=0
        self.ipt=['','',0,0]
        self.f = ""
        self.inputs=[]
        self.direction=''
        self.button=''
        self.frames_to_hold=1
        self.started = None
        self.MoveNames = []
        self.ExtraInfo = []
        
        self.symbol_map = {
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

        self.double_buttons={'12' : '1+2',
            '13' : '1+3',
            '14' : '1+4',
            '23' : '2+3',
            '24' : '2+4',
            '34' : '3+4',
            '1234' :'1+2+3+4',
            '134' :'1+3+4',
            '234' :'2+3+4',
        }
        
    def update_state(self):
        #if not self.launcher.gameState.stateLog:
        #    print("stateLog is empty")
        #    return
        
        self.launcher.gameState.stateLog[-1].is_player_player_one = True #TURN ANALYSE 2P SIDE

        if self.launcher.gameState.stateLog[-1].is_player_player_one: #player one player two
            input = self.launcher.gameState.stateLog[-1].bot.GetInputState()
            cancelable = self.launcher.gameState.stateLog[-1].bot.is_cancelable
            bufferable = self.launcher.gameState.stateLog[-1].bot.is_bufferable
            parry1 = self.launcher.gameState.stateLog[-1].bot.is_parry_1
            parry2 = self.launcher.gameState.stateLog[-1].bot.is_parry_2
            self.MoveNames.append(self.launcher.gameState.GetCurrentBotMoveName())
            
            self.ExtraInfo.append([self.launcher.gameState.GetCurrentBotMoveName(), self.launcher.gameState.stateLog[-1].opp.hit_outcome])
            
        else:
            input = self.launcher.gameState.stateLog[-1].opp.GetInputState()
            cancelable = self.launcher.gameState.stateLog[-1].opp.is_cancelable
            bufferable = self.launcher.gameState.stateLog[-1].opp.is_bufferable
            parry1 = self.launcher.gameState.stateLog[-1].opp.is_parry_1
            parry2 = self.launcher.gameState.stateLog[-1].opp.is_parry_2
            self.MoveNames.append(self.launcher.gameState.GetCurrentOppMoveName())
            
            self.ExtraInfo.append([self.launcher.gameState.GetCurrentOppMoveName(), self.launcher.gameState.stateLog[-1].bot.hit_outcome])
            
        frame_count = self.launcher.gameState.stateLog[-1].frame_count
               
        character=self.launcher.gameState.stateLog[-1].bot.character_name
#        if self.f == None:
#            self.f = open('.\\xml_maker\\'+character.capitalize()+'_outputplayback.txt','a')
        
        if(self.launcher.gameState.WasFightReset()):
#            print("Fight Reset")
 #       if input[0] == InputDirectionCodes.NULL : #Start of the playback #playback InputAttackCode.NULL
            print("In CommandRecorder->update_state restart move")
            self.i=0 #Frame number, reset from previous playback
            self.in_move = False #Previous move ended
            print("START RECORDING \n")

            """ N,''... inputs in between these blocks => Ignored """



        if( ( (input[0] != InputDirectionCodes.N) or (input[1] != InputAttackCodes.N) ) and (input[0] != InputDirectionCodes.NULL)):
            self.i+=1
            if not self.in_move :
                self.f = self.f + "#\n"
            self.in_move = True

            """ Allow to ignores neutral frames between a NULL input (start), and the very first input of one move """

            self.direction=self.symbol_map[input[0]]
            self.button=input[1].name.replace('x', '').replace('N', '') # Replace codes by understandable name


            if (self.direction == self.ipt[0] and self.button == self.ipt[1] and (self.i-self.ipt[2]) == 1):
                self.frames_to_hold+=1
            else :
                self.frames_to_hold=1


            self.ipt=[self.direction,self.button,self.i,self.frames_to_hold] #Saves the frame as a list of 4 items
            #print(self.ipt)
            #print(self.ipt)
            self.formatter(self.ipt[0],self.ipt[1],self.ipt[2],self.ipt[3])
            #i=i+1 #We move to next frame
            #i+=1

        elif( (self.in_move== True) and ( (input[0] == InputDirectionCodes.N) and (input[1] == InputAttackCodes.N) ) ):
            self.i+=1 #Neutrals between inputs (delay)

            """ This block gathers neutral inputs (N,'') between two inputs that aren't neutrals during the move """

            self.direction=self.symbol_map[input[0]]
            self.button=input[1].name.replace('x', '').replace('N', '') #N

            self.ipt=[self.direction,self.button,self.i]
            #print(ipt)
            self.formatter(self.ipt[0],self.ipt[1],self.ipt[2])

        
    def formatter(self, direction, button, frame, fth=1):
        """ Write a tuple of 3 elements : button or direction, frame interval, frame to hold """
        frame=str(frame)
        fth=str(fth)

        if len(button)>1:
            button=self.double_buttons[button]


        if ( (direction == 'N')  and (button == '') ) : #Neutral frames : N,''
            self.f = self.f + direction + ' ' + frame + ' ' + fth + "\n"

        elif ( (direction != 'N')  and (button != '') ) :
            self.f = self.f + direction + '+' + button + ' ' + frame + ' ' + fth + '\n'

        elif (button==''):
            self.f = self.f + direction + ' ' + frame + ' ' + fth + "\n" #df

        elif (direction=='N') :
            self.f = self.f + '+' + button + ' ' + frame + ' ' + fth + "\n" #+4

    def print_f(self):
        print(self.f)
        
    def update_location(self):
        pass
        
    def translate_input(self, i): #list of 3 elements
        #print(i)
        command=[]
        #print(i)
        i[1]=str(i[1])
        i[2]=str(i[2])
        if i[1] == '1' and i[0] != 'N' :
            command.append(i[0])
        elif i[0]=='N':
            command.append(i[1])
        elif i[2] == '1' : #frames to hold = 1, we do not have to handle uppercase or *
            command.append(i[0]+', '+i[1])
        else :
            if i[0] in ['+1','+2','+3','+4','+1+2','1+3','1+4','2+3','2+4','3+4'] :
                command.append(i[0]+"*"+", "+i[2]+", "+i[0]+"-")#"-"+i[0][1].upper())
            else :
                #print(i[0])
                if (i[0]=='d' or i[0]=='b' or i[0]=='u' or i[0]=='f') :#or (len(i[0]) < 4 and i[0][1]=='+') :
                    command.append(i[0].upper()+", "+i[2]+", "+"-"+i[0][0].upper())
                else :
                    #print(len(i[0]))
                    if i[0][1]=="+": #d+1+2
                        command.append(i[0].upper()+", "+i[2]+", "+"-"+i[0][0].upper())
                    else : #df+1+2
                        command.append(i[0].upper()+", "+i[2]+", "+"-"+i[0][0].upper()+", "+"1, -"+i[0][1].upper())

                """if i[0]=='df' or i[0]=='df':
                    command.append(i[0].upper()+", "+i[2]+", "+"-"+'d,1,-f'.upper()) #<<<<=
                elif i[0]=='ub' or i[0]=='db':
                    command.append(i[0].upper()+", "+i[2]+", "+"-"+'b,1,-b'.upper())
                else :
                    command.append(i[0].upper()+", "+i[2]+", "+"-"+i[0].upper())"""


        return command


    def command_translator(self, command):
            inputs=[]
            #print(command)
            for input in command:
                #print(input)
                cmd=self.translate_input(input)
                inputs.append(cmd)
            #inputs.append(cmd)
            #print('\n')
            return inputs
            #print(inputs)


    def calculate_delay(self, move):
        frames=[]
        
        for frame_value in move :
            frames.append(frame_value[1])
        #print(frames)
        for i in range(1,len(move)):
            move[i][1]=move[i][1]-frames[i-1]
        return move

    def process(self, items):
        if len(items) <= 1:
            return items.copy()

        result = []

        for (previous_first, previous_second, previous_third), (first, second, third) in zip(items, items[1:]):
            if first != previous_first or second > previous_second + 1:
                result.append([previous_first, previous_second, previous_third])

        result.append([first, second, third])
        return result

        """assert process([]) == []
        assert process([('+1', 1)]) == [('+1', 1)]
        assert process([('+1', 1), ('+1', 2)]) == [('+1', 2)]
        assert process([
            ('+1', 0), ('+1', 3),
            ('+2', 9), ('+2', 20), ('+2', 21), ('+2', 22), ('+2', 23)
        ]) == [
            ('+1', 0), ('+1', 3),
            ('+2', 9), ('+2', 23)
        ]"""

    def frames_to_int(self, list):
        #print(list)
        #print("\n\n\n")
        for i in list:
            #print(i)
            i[1]=int(i[1])
            i[2]=int(i[2])

        return list


    def move_process(self, movelist):
        if len(movelist)>1:
            #print(movelist)
            
            count = 0
            for frame in reversed(movelist):
                if(frame[0] == 'N'):
                    count = count + 1
                else:
                    break
            
            for i in range(count):
                movelist.pop()
            
            #HoldFrames = 0
            Command = ""
            NextFrame = 0
            LastActionFrame = 0
            #diff = False
            for i in range(len(movelist)):
                #print(str(i) + ": " + str(movelist[i]))
                    
                if(i > 0): #Previous Frame
                    PreviousFrame = ControllerFrame(movelist[i-1][0])
                else:
                    PreviousFrame = ControllerFrame("")
                    
                CurrentFrame = ControllerFrame(movelist[i][0]) #Current Frame
                
                if(i+2 > len(movelist)): #Next Frame
                    NextFrame = ControllerFrame("")
                else:
                    NextFrame = ControllerFrame(movelist[i+1][0])

                FoundDifferencePrevious = PreviousFrame.compare(CurrentFrame)
                FoundDifferenceNext = CurrentFrame.compare(NextFrame)

                
                
                #diff = False
                if(FoundDifferencePrevious['Found']):
                    for input in CurrentFrame.Controller:
                        if(FoundDifferencePrevious["Differences"][input] == "released"):
                            Command = Command + CurrentFrame.getReleaseInput(input)  + ", "
                            #diff = True
                
                for input in CurrentFrame.Controller:
                    if(not PreviousFrame.Controller[input] and CurrentFrame.Controller[input]): 
                        #Input was not pressed last frame, but is this frame. We need to press it.
                        if(not NextFrame.Controller[input]):
                            #Input will only be pressed for one frame
                            print("One Frame")
                            Command = Command + CurrentFrame.getInput(input)
                            #diff = True
                        else:
                            #Input will be held for more then one frame, get the held input
                            Command = Command + CurrentFrame.getHeldInput(input)
                            #diff = True
                
                    #HoldFrames = 0
                #else:
                    #HoldFrames = HoldFrames + 1
                    
                if(FoundDifferenceNext['Found']):
                    if(i - LastActionFrame != 0):
                        Command = Command + ", " + str(i - LastActionFrame) + ", "
                        LastActionFrame = i
                        
                """if(not FoundDifferenceNext['Found']): #no difference found, increment frame counter
                    HoldFrames = HoldFrames + 1
                else: #difference found, find out what it is and make the changes
                    for input in CurrentFrame.Controller:
                        #print(str(i) + ": " + input)
                        if(CurrentFrame.Controller[input]): #This input was pressed, we need to see if we need to hold it
                            if(HoldFrames == 1 and FoundDifferenceNext["Differences"][input] == "released"): #Input only held for 1 frame
                                Command = Command + CurrentFrame.getInput(input)
                            elif(FoundDifferencePrevious["Differences"][input] == "pressed"): #Must be no difference in this input, hold input
                                #print("Held")
                                Command = Command + CurrentFrame.getHeldInput(input)
                                
                    if(HoldFrames > 0):
                        Command = Command + ", " + str(HoldFrames) + ", "
                        HoldFrames = 0
                #print(str(i) + ": " + Command)
                """
                        
                #find how long to hold each input
                """for j in range(i+1, len(movelist)):
                    if(j == len(movelist)-1):
                        c2 = ControllerFrame('')
                    else:
                        c2 = ControllerFrame(movelist[j][0])
                    diff = c1.compare(c2)
                    
                    if(diff['Found']): #Found a difference, check to see if anything was released
                        HoldFrames = j - i
                        if(HoldFrames > 1): #we need to change the inputs to hold
                            #print("Frames > 1")
                            directions = ""
                            buttons = ""
                            for input in c1.Controller:
                                if(c1.Controller[input]):
                                    if(input.isalpha()):
                                        directions = directions + input.upper()
                                    if(input.isnumeric()):
                                        buttons = buttons + "+" + input
                            Command = Command + directions + buttons + "*, " + str(HoldFrames) + ", "
                        else: 
                            #print("Frames = 1")
                            directions = ""
                            buttons = ""
                            for input in c1.Controller:
                                if(c1.Controller[input]):
                                    if(diff["Differences"][input] == "released"): #input was 1 frame, don't need to do anything
                                        pass #directions = directions + input
                                    elif(diff["Differences"][input] == "pressed"): #input was at least 2 frames, set to hold
                                        if(input.isalpha()):
                                            directions = directions + input.upper()
                                        if(input.isnumeric()):
                                            buttons = buttons + "+" + input + "*"
                            #print("D: " + directions + " B: " + buttons)
                            if(len(directions) > 0 or len(buttons) > 1):
                                Command = Command + directions + buttons + ", 1, "
                        for input in c1.Controller:
                            if(diff["Differences"][input] == "released"):
                                if(input.isalpha()):
                                    Command = Command + "-" + input.upper() + ", "
                                if(input.isnumeric()):
                                    Command = Command + "+" + input + "-, "
                        NextFrame = j        
                        break"""
                
            #print(Command)
            return Command
            #movelist=self.frames_to_int(movelist)
            #movelist=self.process(movelist)
            ##print(movelist)
            #movelist.pop()# Last neutral input between two moves. Transition neutral garbage
            ##print(movelist)
            #movelist=self.calculate_delay(movelist)
            ##print('\n',movelist)
            #movelist=self.command_translator(movelist)

            """for i in range(len(movelist)) :
                if i==0:
                    print(movelist[i][0],end='')
                else :
                    print(",",movelist[i][0], end='')"""

            #return movelist

    def parser(self, playback):
        move=[]
        moves=[]
        for i in playback :
            if i[0]=='#':
                moves.append(self.move_process(move))
                move=[]
            else :
                move.append(i)
        return moves

    def parse(self, character):
#        f = open('.\\xml_maker\\'+character.capitalize()+'_outputplayback.txt','a') #add # at the end to finish the loop , or you can repeat to first move
        self.f = self.f + "#"
        
        char = open('xml_maker\\' + character + '_move' + '_commands.txt', 'w')
        #char.write(self.f)
    #fw = open('shaheenmv.txt','w')
        playbackrecord=[]
        move=[]
        cmd=[]
        
        for line in self.f.splitlines():
            #print(line)
            playbackrecord.append(line.rstrip().split(' '))

        playbackrecord=self.parser(playbackrecord)
        y=1
        for i in playbackrecord:
            #char.write(str(y)+' : ')
            if i != None :
                for j in i :
                    #print(j)
                    char.write(str(j[0])+', ')
                char.write('\n')
                y=y+1
        """for i in playbackrecord :
            if i == '#' :
                cmd=cmd(frames_to_int)
                print(process(cmd))
            else :
                cmd.append(i)"""
#        f.close()
        char.close()
