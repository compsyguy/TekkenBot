import sys
import csv
import xml.etree.ElementTree as ET


if len(sys.argv) != 2:
    print("Usage: ToCSV.py file")
    sys.exit()
    

Char = ET.parse(sys.argv[1])
root = Char.getroot()    

print(root.attrib['name'])

OutputFile = "csv/" + root.attrib['name'] + ".csv" 

with open(OutputFile, 'w', newline='') as csvfile:
    MoveWriter = csv.writer(csvfile, delimiter=',')
    MoveWriter.writerow(["Move ID", "Move", "Command", "hitLevel", "BlockFrame", "Punishable", "Duckable"])
    for move in root.findall('moves/move'):
        if(len(move.findall("tags/Punishable")) > 0):
            Punishable = True
        else:
            Punishable = False
            
        if(len(move.findall("tags/DuckableString")) > 0):
            Duckable = True
        else:
            Duckable = False
        MoveWriter.writerow([move.findall("id")[0].text, move.findall("name")[0].text, move.findall("command")[0].text, move.findall("hitLevel")[0].text, move.findall("BlockFrame")[0].text, Punishable, Duckable])
