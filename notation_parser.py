def translate_input(i): #list of 3 elements
    print(i)
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


def command_translator(command):
        inputs=[]
        for input in command:
            #print(input)
            cmd=translate_input(input)
            inputs.append(cmd)
        #inputs.append(cmd)
        print('\n')
        return inputs
        #print(inputs)


def calculate_delay(move):
    frames=[]
    for frame_value in move :
        frames.append(frame_value[1])
    #print(frames)
    for i in range(1,len(move)):
        move[i][1]=move[i][1]-frames[i-1]
    return move

def process(items):
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

def frames_to_int(list):
    for i in list:
        i[1]=int(i[1])
        i[2]=int(i[2])

    return list


def move_process(movelist):
    if len(movelist)>1:
        movelist=frames_to_int(movelist)
        movelist=process(movelist)
        #print(movelist)
        movelist.pop()# Last neutral input between two moves. Transition neutral garbage
        #print(movelist)
        movelist=calculate_delay(movelist)
        #print('\n',movelist)
        movelist=command_translator(movelist)

        """for i in range(len(movelist)) :
            if i==0:
                print(movelist[i][0],end='')
            else :
                print(",",movelist[i][0], end='')"""

        return movelist

def parser(playback):
    move=[]
    moves=[]
    for i in playback :
        if i[0]=='#':
            moves.append(move_process(move))
            move=[]
        else :
            move.append(i)
    return moves

def main():
    character="kazuya"
    f = open('.\\xml_maker\\'+character.capitalize()+'_outputplayback.txt','a') #add # at the end to finish the loop , or you can repeat to first move
    f.write("#")
    f.close()
    f = open('.\\xml_maker\\'+character.capitalize()+'_outputplayback.txt','r')
    char = open(character+'_move'+'_commands.txt','w')
#fw = open('shaheenmv.txt','w')
    playbackrecord=[]
    move=[]
    cmd=[]
    for line in f:
        playbackrecord.append(line.rstrip().split(' '))

    playbackrecord=parser(playbackrecord)
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
    f.close()
    char.close()

main()
