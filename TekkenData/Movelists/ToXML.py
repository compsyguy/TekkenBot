import sys
import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom

if len(sys.argv) != 3:
    print("Usage: ToXML.py CSVfile, XMLfile")
    sys.exit()

Char = ET.parse(sys.argv[2])
root = Char.getroot()

with open(sys.argv[1], 'r', newline='') as csvfile:
    movereader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row in movereader:
        move = root.find(".//moves/move[id='" + row[0] + "']")
        if(move != None):
            move.find(".//command").text = row[2]
        #print(row[2])
        
        
filename = sys.argv[2]
#copyfile(filename, os.path.join(self.directory, "xml backups", self.CharName + "-" + self.CharXml.getroot().attrib['version'] + ".xml"))
#self.CharXml.getroot().attrib['version'] = str(int(time.time()))
f = open(filename, "w")
# print(ET.tostring(Char))
xmlFile = xml.dom.minidom.parseString(ET.tostring(Char.getroot(), 'utf-8'))
f.write(xmlFile.toprettyxml(indent="", newl=""))
f.close()        