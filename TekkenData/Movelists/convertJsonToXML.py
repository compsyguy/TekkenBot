import json
import sys
import random
import os.path
import xml.etree.ElementTree as ET
import xml.dom.minidom
#import lxml.etree as ET
#from xml.etree.ElementTree import ElementTree

if len(sys.argv) != 4:
    print("Usage: convertJsonToXML.py file charId CharName")
    sys.exit()

if os.path.isfile(sys.argv[3] + ".xml"):
    print("XML movelist files already exists.")
    sys.exit()

f = open(sys.argv[1])
j = json.load(f)
Char = ET.Element("character", {"id":sys.argv[2], "name":sys.argv[3]})
CharMoves = ET.SubElement(Char, "moves")
id = 1
Quiz = ET.Element("quiz", {"name":"Punishable", "type":"FrameQuiz", "description":"A quiz of the character's punishable moves"})
QuizMoves = ET.SubElement(Quiz, "moves")

StartUpList = []
OnBlockList = []
OnHitList = []
OnCHList = []

for move in j["moves"]:
    CharMove = ET.SubElement(CharMoves, "move")
    MoveId = ET.SubElement(CharMove, "id")
    MoveId.text = str(id)
    id = id+1
    MoveName = ET.SubElement(CharMove, "name")
    MoveName.text = move["notation"]
    #print(MoveName.text)
    MoveCommand = ET.SubElement(CharMove, "command")
    #Not trying to guess the move command anymore, but leaving in for reference
    #commands = move["notation"].split(",")
    #commandString = ''
    #buttons = ["1", "2", "3", "4", "1+2", "1+3", "1+4", "2+3", "2+4", "3+4"]
    #
    #for i in range(len(commands)):
    #    commands[i] = commands[i].strip()
    #    if commands[i] in buttons:
    #        commands[i] = '+' + commands[i]
    #    else:
    #        commands[i] = commands[i]
    #
    #
    #MoveCommand.text = ", 5, ".join(commands)
    MoveCommand.text = " "
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
            if tag.strip() == "Tail spin":
                #print("TS")
                ET.SubElement(MoveTags, "TailSpin")
            elif tag.strip() == "Power crush":
                #print("PC")
                ET.SubElement(MoveTags, "PowerCrush")
            elif tag.strip() == "Power Crush":
                #print("PC")
                ET.SubElement(MoveTags, "PowerCrush")
            elif tag.strip() == "Rage art":
                ET.SubElement(MoveTags, "RageArt")
            elif tag.strip() == "Rage drive":
                ET.SubElement(MoveTags, "RageDrive")
            elif tag.strip() == "Wall bounce":
                ET.SubElement(MoveTags, "WallBounce")
            elif tag.strip() == "":
                pass
            else:
                #print(tag.strip())
                ET.SubElement(MoveTags, tag.strip())


GamePlans = ET.SubElement(Char, "gameplans")

GamePlan = ET.SubElement(GamePlans, "gameplan")
GPID = ET.SubElement(GamePlan, "id")
GPID.text = "1"
GPName = ET.SubElement(GamePlan, "name")
GPName.text = "All Moves"
GPMoves = ET.SubElement(GamePlan, "moves")
AllMoves = Char.findall(".//move/id")
for id in AllMoves:
    GPMove = ET.SubElement(GPMoves, "id")
    GPMove.text = id.text

GamePlan = ET.SubElement(GamePlans, "gameplan")
GPID = ET.SubElement(GamePlan, "id")
GPID.text = "2"
GPName = ET.SubElement(GamePlan, "name")
GPName.text = "Punishable Moves"
GPMoves = ET.SubElement(GamePlan, "moves")
PunishableMoves = Char.findall(".//move/tags/Punishable/../../id")
NumAnswers = 7
for id in PunishableMoves:
    GPMove = ET.SubElement(GPMoves, "id")
    GPMove.text = id.text

    QuizMove = ET.SubElement(QuizMoves, "move")
    ET.SubElement(QuizMove, "id").text = str(id.text)
    QuizAnswers = ET.SubElement(QuizMove, "WrongAnswers")

    QuizStartup = ET.SubElement(QuizAnswers, "StartUp")
    answers = []
    for i in range(NumAnswers):
        answer = random.choice(StartUpList)
        while (not answer) or (answer in answers) or (answer == Char.find('.//move[id="' + id.text + '"]/StartUp').text):
            answer = random.choice(StartUpList)
        answers.append(answer)
    #answers = random.sample(StartUpList, NumAnswers)
    for i in range(NumAnswers):
        AnswerValue = ET.SubElement(QuizStartup, "Value")
        AnswerValue.text = answers[i]

    QuizBlock = ET.SubElement(QuizAnswers, "BlockFrame")
    answers = []
    for i in range(NumAnswers):
        answer = random.choice(OnBlockList)
        while (not answer) or (answer in answers) or (answer == Char.find('.//move[id="' + id.text + '"]/BlockFrame').text):
            answer = random.choice(OnBlockList)
        answers.append(answer)
    #answers = random.sample(OnBlockList, NumAnswers)
    for i in range(NumAnswers):
        AnswerValue = ET.SubElement(QuizBlock, "Value")
        AnswerValue.text = AnswerValue.text = answers[i]

    QuizHit = ET.SubElement(QuizAnswers, "HitFrame")
    answers = []
    for i in range(NumAnswers):
        answer = random.choice(OnHitList)
        while (not answer) or (answer in answers) or (answer == Char.find('.//move[id="' + id.text + '"]/HitFrame').text):
            answer = random.choice(OnHitList)
        answers.append(answer)
    #answers = random.sample(OnHitList, NumAnswers)
    for i in range(NumAnswers):
        AnswerValue = ET.SubElement(QuizHit, "Value")
        AnswerValue.text = AnswerValue.text = answers[i]

    QuizCH = ET.SubElement(QuizAnswers, "CounterHitFrame")
    answers = []
    for i in range(NumAnswers):
        answer = random.choice(OnCHList)
        while (not answer) or (answer in answers) or (answer == Char.find('.//move[id="' + id.text + '"]/CounterHitFrame').text):
            answer = random.choice(OnCHList)
        answers.append(answer)

#    answers = random.sample(OnCHList, NumAnswers)
    for i in range(NumAnswers):
        AnswerValue = ET.SubElement(QuizCH, "Value")
        AnswerValue.text = AnswerValue.text = answers[i]

#GPMove = ET.SubElement(GPMoves, "id")
#GPMove.text = "1"
                
f = open(sys.argv[3] + ".xml", "w")
# print(ET.tostring(Char))
xmlString = ET.tostring(Char)
#print(xmlString[37300:37400])
xmlFile = xml.dom.minidom.parseString(xmlString)

f.write(xmlFile.toprettyxml())
f.close()

#f = open(sys.argv[3] + "-quiz.xml", "w")
#xmlFile = xml.dom.minidom.parseString(ET.tostring(Quiz))
#f.write(xmlFile.toprettyxml())
#f.close()