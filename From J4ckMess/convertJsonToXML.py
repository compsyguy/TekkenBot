import json
import sys
import random
import os.path
import xml.etree.ElementTree as ET
import xml.dom.minidom

if len(sys.argv) != 4:
    print("Usage:"+sys.argv[0]+" jsonfile charId CharName")
    sys.exit()

if os.path.isfile(sys.argv[3] + ".xml"):
    print("Old XML file erased.")

f = open(sys.argv[1])
j = json.load(f)
Char = ET.Element("character", {"id":sys.argv[2], "name":sys.argv[3].capitalize(), "version":1})
CharMoves = ET.SubElement(Char, "moves")
id = 1

StartUpList = []
OnBlockList = []
OnHitList = []
OnCHList = []
ids=[]

def get_dic(character):
    """ both files must have same lines length, function merge commands with move names """
    move_dic={}
    listorder=open(character+"_orderedlist.txt",'r')
    movelist=open(character+"_move_commands.txt",'r')

    listorder=listorder.read().splitlines()
    movelist=movelist.read().splitlines()
    for i in range(len(listorder)) :
        move_dic[listorder[i]]=movelist[i]
    return move_dic

for move in j["moves"]:
    CharMove = ET.SubElement(CharMoves, "move")
    MoveId = ET.SubElement(CharMove, "id")
    MoveId.text = str(id)
    id = id+1
    MoveName = ET.SubElement(CharMove, "name")
    MoveName.text = move["notation"]
    #print(MoveName.text)
    MoveCommand = ET.SubElement(CharMove, "command")
    dic=get_dic(sys.argv[3].capitalize())
    if MoveName.text in dic.keys():
        MoveCommand.text=dic[MoveName.text]
        ids.append(str(id-1))
        print(ids)
        #print(MoveCommand.text,"\n")
        #print(MoveName.text,"\n")
    else :
        commands = move["notation"].split(",")
        commandString = ''
        buttons = ["1", "2", "3", "4", "1+2", "1+3", "1+4", "2+3", "2+4", "3+4"]

        for i in range(len(commands)):
            commands[i] = commands[i].strip()
            if commands[i] in buttons:
                commands[i] = '+' + commands[i]
            else:
                commands[i] = commands[i]


        MoveCommand.text = ", 5, ".join(commands)
        #if len(MoveName.text)<=4:
            #ids.append(str(id-1))



    MoveHitLevel = ET.SubElement(CharMove, "hitLevel")
    MoveHitLevel.text = move["hit_level"]

    MoveDamage = ET.SubElement(CharMove, "damage")
    MoveDamage.text = move["damage"]

    MoveStartUp = ET.SubElement(CharMove, "StartUp")
    StartUpList.append(move["speed"])
    MoveStartUp.text = move["speed"]

    MoveBlockFrame = ET.SubElement(CharMove, "BlockFrame")
    OnBlockList.append(move["on_block"])
    MoveBlockFrame.text = move["on_block"]

    MoveHitFrame = ET.SubElement(CharMove, "HitFrame")
    OnHitList.append(move["on_hit"])
    MoveHitFrame.text = move["on_hit"]

    MoveCounterHitFrame = ET.SubElement(CharMove, "CounterHitFrame")
    OnCHList.append(move["on_ch"])
    MoveCounterHitFrame.text = move["on_ch"]

    MoveTags = ET.SubElement(CharMove, "tags")
    ET.SubElement(MoveTags, "NeedsWork")
    try:
        b = int(move["on_block"])
        if b <= -10:
            TagPunish = ET.SubElement(MoveTags, "Punishable")
            TagPunish.text = move["on_block"]

        else:
            ET.SubElement(MoveTags, "Safe")
    except:
        try:
            frameRange = move["on_block"].split("~")
            if(len(frameRange) == 2):

                frameRange[0] = int(frameRange[0])
                frameRange[1] = int(frameRange[1])
                if(max(frameRange) < -10):
                    TagPunish = ET.SubElement(MoveTags, "Punishable")
                    TagPunish.text = str(max(frameRange))
        except:
            pass


    pass

    if move["notes"]:
        tags = move["notes"].split(",")
        for tag in tags:
            tag=tag.strip()
            #print(tag)
            if tag == "Tail spin" or tag == "Tail Spin":
                #print("TS")
                ET.SubElement(MoveTags, "TailSpin")
            elif tag == "Power crush" or tag == "Power Crush":
                #print("PC")
                ET.SubElement(MoveTags, "PowerCrush")
            elif tag == "Rage art" or tag == "Rage Art":
                ET.SubElement(MoveTags, "RageArt")
            elif tag == "Homing" or tag == "homing":
                ET.SubElement(MoveTags, "Homing")
            elif tag == "wb!" or tag == "Wb!":
                ET.SubElement(MoveTags, "WallBounce")
            elif tag == "Notes" or tag == "notes":
                ET.SubElement(MoveTags, "Notes")
            else:
                ET.SubElement(MoveTags,tag.replace(" ",""))

            """ Try except necessary to handle it right """

GamePlans = ET.SubElement(Char, "gameplans")
GamePlan = ET.SubElement(GamePlans, "gameplan")
GPID = ET.SubElement(GamePlan, "id")
GPID.text = "1"
GPName = ET.SubElement(GamePlan, "name")
GPMoves = ET.SubElement(GamePlan, "moves")
#PunishableMoves = Char.findall(".//move/tags/Punishable/../../id")
#print(len(ids))
for id in ids: #add only to gameplans moves that has been captured
    GPMove = ET.SubElement(GPMoves, "id")
    GPMove.text = id

GPMove = ET.SubElement(GPMoves, "id")
GPMove.text = "1"

f = open(sys.argv[3].capitalize() + ".xml", "w")
# print(ET.tostring(Char))
xmlFile = xml.dom.minidom.parseString(ET.tostring(Char))
f.write(xmlFile.toprettyxml())
f.close()
