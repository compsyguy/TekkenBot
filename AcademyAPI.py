import requests
import json
import sys
import time
from urllib.parse import urlencode
from getpass import getpass
import pickle
import os.path
import xml.etree.ElementTree as ET

from movelist import MoveList

class AcademyAPI():
    def __init__(self):
        self.BaseURL = "https://tekken.academy/"
        self.TokenRUL = self.BaseURL + "session/token"
        self.login = {}
        self.session = requests.session()
        
        self.auth = {}
        self.auth['location'] = self.BaseURL + "user/login?_format=json"
        self.auth['head'] = {}
        self.auth['head']['Accept'] = 'application/json'
        self.auth['head']['Content-Type'] = 'application/json'
        
        self.CookieFile = "auth.cookie"
        self.PostData = {}
        
    def login(self, auth):
        self.login['name'] = self.auth['name']
        self.login['pass'] = self.auth['pass']
        l = json.dumps(self.login)
        
        req = self.session.post(auth['location'], data=l)
        
        auth['head'] = {}
        auth['cookie'] = {}
        if req.status_code == 200:
            r = json.loads(req.text)
            self.auth['head']['X-CSRF-Token'] = r['csrf_token']
            self.auth['head']['Accept'] = 'application/json'
            sekf.auth['head']['Content-Type'] = 'application/json'
            self.auth['cookie'] = req.cookies.get_dict()
            return True
        else:
            return False
            
    def IsLoggedIn(self):
        if(os.path.exists(self.CookieFile)):
            with open(self.CookieFile, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
            req = self.session.get("https://tekken.academy/session/token")
            #print(req.text)
            self.auth['head']['X-CSRF-Token'] = req.text
            self.auth['cookie'] = self.session.cookies.get_dict()
            
            return True
        else:
            return False

    def ConvertStringToDrupalArray(self, String, Separator, Key):
        split = String.split(Separator)
        a = []
        for s in split:
            a.append({Key: s})
            
        return a

    def AddMoveForCharacter(self, WebCharID, moveXML):
        
        post_data = {}
        post_data['title'] = [{"value":moveXML.find(".//name").text}]
        post_data['type'] = [{'target_id': "move"}]
        post_data['field_hit_level'] = self.ConvertStringToDrupalArray(moveXML.find(".//hitLevel").text, ",", "value")
        post_data['field_move_block_frame'] = self.ConvertStringToDrupalArray(moveXML.find(".//BlockFrame").text, "~", "value")
        post_data['field_move_command'] = [{"value":moveXML.find(".//name").text}]
        post_data['field_move_counter_hit_frame'] = self.ConvertStringToDrupalArray(moveXML.find(".//CounterHitFrame").text, "~", "value")
        post_data['field_move_damage'] = self.ConvertStringToDrupalArray(moveXML.find(".//damage").text, ",", "value")
        post_data['field_move_for_character'] = [{"target_id": WebCharID}]
        post_data['field_move_hit_frame'] = self.ConvertStringToDrupalArray(moveXML.find(".//HitFrame").text, "~", "value")
        
        #post_data['field_move_properties'] = self.ConvertStringToDrupalArray(moveXML.find(".//HitFrame").text, "~", "value")
        post_data['field_move_start_up'] = self.ConvertStringToDrupalArray(moveXML.find(".//StartUp").text, "~", "value")
        #post_data['field_tech_crouch_frames'] = self.ConvertStringToDrupalArray(moveXML.find(".//HitFrame").text, "~", "value")
        #post_data['field_tech_jump_frames'] = self.ConvertStringToDrupalArray(moveXML.find(".//HitFrame").text, "~", "value")
        
        pd = json.dumps(post_data)
        #print(pd)
        pst = self.session.post('https://tekken.academy/node?_format=json', data=pd, headers=self.auth['head'], cookies=self.auth['cookie'])
        print(pst.text)

a = AcademyAPI()
print(a.IsLoggedIn())

m = MoveList(28)
a.AddMoveForCharacter(7, m.getMoveById(91))