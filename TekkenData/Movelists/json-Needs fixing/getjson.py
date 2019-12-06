import requests
import html.parser
#import xml.etree.ElementTree as ET
import json
from bs4 import BeautifulSoup
import os.path
import sys

if len(sys.argv) != 3:
    print("Usage: getjson.py url CharName")
    sys.exit()

if os.path.isfile(sys.argv[2] + ".json"):
    print("json file already exists.")
    sys.exit()

headers = {
    'User-Agent': 'My User Agent 1.0',
}

r = requests.get(sys.argv[1], headers=headers)
#s = requests.session()
#response = s.get(sys.argv[1])
#print(r.text)
soup = BeautifulSoup(r.text, 'html.parser')
print(soup)

t = soup.find_all('table')
r = t[0].find_all('tr')
r.pop(0) #remove the header row

moves = []
for row in r:
    move = {}
    columns = row.find_all('td')
    move['notation'] = columns[0].text
    move['hit_level'] = columns[1].text
    move['damage'] = columns[2].text
    move['speed'] = columns[3].text
    move['on_block'] = columns[4].text
    move['on_hit'] = columns[5].text
    move['on_ch'] = columns[6].text
    move['notes'] = columns[7].text
    moves.append(move)

meta = {"ver": "0.4", "game": "t7", "character": sys.argv[2], "name": sys.argv[2], "type": "normal"}
char = {"moves": moves, "metadata":meta}
f = open(sys.argv[2] + ".json", "w")
f.write(json.dumps(char, sort_keys=False, indent=4, separators=(',', ': ')))