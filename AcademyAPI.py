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
        #self.login = {}
        self.session = requests.session()
        
        self.auth = {}
        self.auth['location'] = self.BaseURL + "user/login?_format=json"
        self.auth['head'] = {}
        self.auth['head']['Accept'] = 'application/json'
        self.auth['head']['Content-Type'] = 'application/json'
        
        self.CookieFile = "auth.cookie"
        self.PostData = {}
        
        self.TwoFields = [{'xml': 'name', 'web': 'field_move_command'},
                     {'xml': 'command', 'web': 'field_move_bot_command'},
                     {'xml': 'hitLevel', 'web': 'field_hit_level'}, 
                     {'xml': 'damage', 'web': 'field_move_damage'},
                     {'xml': 'StartUp', 'web': 'field_move_start_up'},
                     {'xml': 'BlockFrame', 'web': 'field_move_block_frame'},
                     {'xml': 'HitFrame', 'web': 'field_move_hit_frame'},
                     {'xml': 'CounterHitFrame', 'web': 'field_move_counter_hit_frame'}
                    ]
        
        self.TagsAndProperties = [{'property': 'Rage Art', 'tag': 'RageArt'},
                                  {'property': 'Tail Spin', 'tag': 'TailSpin'},
                                  {'property': 'Rage Drive', 'tag': 'RageDrive'},
                                  {'property': 'Power Crush', 'tag': 'PowerCrush'},
                                  {'property': 'Wall Bounce', 'tag': 'WallBounce'},
                                  {'property': 'Homing', 'tag': 'Homing'}
                                 ]
        
        
    def GetLoginCredentials(self):
        self.auth['name'] = input("Enter Your Username: ")
        self.auth['pass'] = getpass()
    
    def login(self):
        login = {}
        login['name'] = self.auth['name']
        login['pass'] = self.auth['pass']
        l = json.dumps(login)
        
        req = self.session.post(self.auth['location'], data=l)
        
        self.auth['head'] = {}
        self.auth['cookie'] = {}
        
        if req.status_code == 200:
            r = json.loads(req.text)
            self.auth['head']['X-CSRF-Token'] = r['csrf_token']
            self.auth['head']['Accept'] = 'application/json'
            self.auth['head']['Content-Type'] = 'application/json'
            self.auth['cookie'] = req.cookies.get_dict()
            pickle.dump(self.auth['cookie'], open(self.CookieFile, "wb"))
            return True
        else:
            return False
            
    def IsLoggedIn(self):
        if(os.path.exists(self.CookieFile)):
            with open(self.CookieFile, 'rb') as f:
                self.session.cookies.update(pickle.load(f))
            
            req = self.session.get("https://tekken.academy/session/token")
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

    ##########################
    # ConvertTagsToProperties(self, tags)
    #
    # Converts the tags from the XML movelist to be used in the website move node's properties field.
    #
    # Parameters:
    # tags: the XML node that contains the tags
    #
    # Returns: the the data that will go in the properties field
    #########################
    def ConvertTagsToProperties(self, tags):
        Properties = []
        for tag in self.TagsAndProperties:
            if tags.find(tag['tag']) != None:
                Properties.append({'value': tag['property']})
        
#        if(tags.find('RageArt') != None):
#            Properties.append({'value': 'Rage Art'})
#        
#        if(tags.find('TailSpin') != None):
#            Properties.append({'value': 'Tail Spin'})
#        
#        if(tags.find('RageDrive') != None):
#            Properties.append({'value': 'Rage Drive'})
#        
#        if(tags.find('PowerCrush') != None):
#            Properties.append({'value': 'Power Crush'})
#
#        if(tags.find('WallBounce') != None):
#            Properties.append({'value': 'Wall Bounce'})
#        
#        if(tags.find('Homing') != None):
#            Properties.append({'value': 'Homing'})

        return Properties

    def ConvertPropertiesToTags(self, Tags, Properties):
        if len(Properties) != 0:
            print(Properties)
            PropertiesList = []
            for Propertiy in Properties:
                PropertiesList.append(Propertiy['value'])
                
            for tag in self.TagsAndProperties:
                if tag['property'] in PropertiesList:
                    MoveTag = ET.SubElement(Tags, tag['tag'])
                    MoveTag.text = tag['property']

    ########################
    # DoesMoveExistInSite(self, Character, Move)
    #
    # Finds out if a move from the XML movelist exists in the website
    #
    # Parameters:
    # Character: The character name on the website
    # Move: The XML node that contains the move. 
    #
    # Returns: The website move if it exists, otherwise returns None
    #######################
    def DoesMoveExistInSite(self, Character, Move):
        movelist = self.GetMovesFromAPIForCharacter(Character)
        for move in movelist:
            if(move['field_move_command'][0]['value'] == Move.find('.//name').text):
                return move
        
        return None
        
        
    ######################
    # GetMovesFromAPIForCharacter(self, Character)
    #
    # Get Moves from the website for a character by the character name on the website
    #
    # Parameters:
    # Character: The character name on the website
    #
    # Returns: a json object of the character moves
    ######################
    def GetMovesFromAPIForCharacter(self, Character):
        urlCharacter = Character.replace(" ", "-")
        movelistJson = self.session.get(self.BaseURL + 'character/' + urlCharacter + '/movelist/json')
        movelist = json.loads(movelistJson.text)
        return movelist
    
    
    ######################
    # AddMoveForCharacter(self, WebCharID, moveXML)
    #
    # Adds a move to the website based on the WebID and the XML of the move from the movelist object
    #
    # Parameters:
    # WebCharID: The NID of the character on the website. 
    # moveXML: The XML node that contains the move. The new Web NID would be added to the move node. Would need to save the movelist after the fact.
    #####################
    def AddMoveForCharacter(self, WebCharID, moveXML):
        
        if(moveXML.find('.//APINid') != None):
            raise Exception('Move has an API Nid already, it should be in the Website already.')
        else:
            
            post_data = {}
            post_data['title'] = [{"value":moveXML.find(".//name").text}]
            post_data['type'] = [{'target_id': "move"}]
            post_data['field_hit_level'] = [{'value': moveXML.find(".//hitLevel").text}]
            post_data['field_move_block_frame'] = [{'value': moveXML.find(".//BlockFrame").text}]
            post_data['field_move_command'] = [{"value":moveXML.find(".//name").text}]
            post_data['field_move_counter_hit_frame'] = [{"value":moveXML.find(".//CounterHitFrame").text}]
            post_data['field_move_damage'] = [{"value":moveXML.find(".//damage").text}]
            post_data['field_move_for_character'] = [{"target_id": WebCharID}]
            post_data['field_move_hit_frame'] = [{"value":moveXML.find(".//HitFrame").text}]
            
            post_data['field_move_properties'] = self.ConvertTagsToProperties(moveXML.find(".//tags"))
            post_data['field_move_start_up'] = [{"value":moveXML.find(".//StartUp").text}]
            post_data['field_move_xml_id'] = [{"value":moveXML.find(".//id").text}]
            post_data['field_move_bot_command'] = [{"value":moveXML.find(".//command").text}]
            
            gameIdsArray = []
            gameIds = moveXML.findall(".//gameIds/gameId")
            for id in gameIds:
                gameIdsArray.append({"value": id.text})
            post_data['field_move_game_ids'] = gameIdsArray
            
            
            pd = json.dumps(post_data)
            #print(pd)
            
            #pd = self.ConvertXMLMoveToWeb(moveXML)
            
            pst = self.session.post('https://tekken.academy/node?_format=json', data=pd, headers=self.auth['head'], cookies=self.auth['cookie'])
            response = json.loads(pst.text)
            id = ET.SubElement(moveXML, "APINid")
            print(response)
            id.text = str(response['nid'][0]['value'])
            #return response['nid'][0]['value']

    ######################
    # UpdateMoveForCharacter(self, WebCharID, moveXML)
    #
    # Updates a move on the website based on the WebID and the XML of the move from the movelist object
    #
    # Parameters:
    # WebCharID: The NID of the character on the website. 
    # moveXML: The XML node that contains the move. 
    #####################
    def UpdateMoveForCharacter(self, WebCharID, moveXML):
        if(moveXML.find('.//APINid') == None):
            raise Exception("Move doesn't have an API NID.")
        else:
            pd = self.ConvertXMLMoveToWeb(moveXML)
            
            pst = self.session.patch(self.BaseURL + 'node/' + moveXML.find('.//APINid').text + '?_format=json', data=pd, headers=self.auth['head'], cookies=self.auth['cookie'])
            response = json.loads(pst.text)
            
            #print(response)
    ######################
    # ConvertXMLMoveToWeb(self, moveXML)
    #
    # Converts the data from the XML to what the Website API expects
    #
    # Parameters:
    # moveXML: The XML node that contains the move. 
    #####################       
    def ConvertXMLMoveToWeb(self, moveXML):
        post_data = {}
        post_data['title'] = [{"value":moveXML.find(".//name").text}]
        post_data['type'] = [{'target_id': "move"}]
        
        for type in self.TwoFields:
            post_data[type['web']] = [{"value": moveXML.find(".//" + type['xml']).text}]
            
        post_data['field_move_properties'] = self.ConvertTagsToProperties(moveXML.find(".//tags"))
        
        gameIdsArray = []
        gameIds = moveXML.findall(".//gameIds/gameId")
        for id in gameIds:
            gameIdsArray.append({"value": id.text})
        post_data['field_move_game_ids'] = gameIdsArray
        
        return(json.dumps(post_data))


    def AddCharacterToWeb(self, movelist):
        attribs = movelist.CharXml.getroot().attrib
        
        post_data = {}
        post_data['type'] = [{'target_id': "characters"}]
        
        post_data['title'] = [{"value": attribs['fullname']}]
        post_data['body'] = [{"value": "Description goes here"}]
        post_data['field_tekken_character_id'] = [{"value": attribs['id']}]
        
        pd = json.dumps(post_data)
        pst = self.session.post('https://tekken.academy/node?_format=json', data=pd, headers=self.auth['head'], cookies=self.auth['cookie'])
        response = json.loads(pst.text)
        
    ####################
    # GetWebCharacters(self)
    #
    # Returns all the characters as json objects of the website's characters
    ####################
    def GetWebCharacters(self):
        characterJson = self.session.get(self.BaseURL + 'characters/json')
        #print(characterJson.text)
        characters = json.loads(characterJson.text)
        return characters
    
    ####################    
    # GetWebCharacterByID(self, CharID)
    # 
    # Returns a json object representative of the website's character for the supplied internal Tekken ID
    #
    # Parameters:
    # CharID: The internal Tekken ID for the character
    ####################
    def GetWebCharacterByID(self, CharID):
        characters = self.GetWebCharacters()
        for character in characters:
            if(character['field_tekken_character_id'][0]['value'] == CharID):
                return character

    def IsMovePropertyDifferentFromWeb(self, Web, WebField, XML, XMLField):
        if (XML.find(".//" + XMLField).text != None) and (len(Web[WebField]) == 1): #Both Fields have something in them
            if XML.find(".//" + XMLField).text == Web[WebField][0]['value']: #Both Fields are the same
                return False
            else:
                return True
        elif(XML.find(".//" + XMLField).text != None) != (len(Web[WebField]) == 1): #One Field is empty, the other isn't
            return True
        #Both fields are empty
        return False


    def AddAPIMoveToXML(self, APIMove, movelist):
        XMLIds = movelist.GetAllMoveIds()   
        XMLMoves = movelist.CharXml.getroot().find(".//moves")
        NewMove = ET.SubElement(XMLMoves, 'move')
        ID = ET.SubElement(NewMove, 'id')
        
        for i in range(0, len(XMLIds)):
            XMLIds[i] = int(XMLIds[i])
        ID.text = str(max(XMLIds) + 1)
        
        for Field in self.TwoFields:
            print(Field['xml'] + "\t" + Field['web'] + "\t" + str(APIMove[Field['web']]))
            tag = ET.SubElement(NewMove, Field['xml'])
            if len(APIMove[Field['web']]) != 0:
                tag.text = str(APIMove[Field['web']][0]['value'])
        
        Tags = ET.SubElement(NewMove, 'tags')
        self.ConvertPropertiesToTags(Tags, APIMove['field_move_properties'])
        
        #print(max(XMLIds))



    ########################
    # UpdateXMLFromAPI(self, movelist):
    #
    # Updates the local XML movelist. 
    #
    # TODO: Check for added/removed moves
    # Parameters: 
    # movelist: The movelist should already be loaded with a character's movelist.
    ########################
    def UpdateXMLFromAPI(self, movelist):
        WebMovelist = self.GetMovesFromAPIForCharacter(movelist.FullName)
        FoundDifferences = False
        for WebMove in WebMovelist:
            if WebMove['field_move_xml_id']:
                Move = movelist.getMoveById(WebMove['field_move_xml_id'][0]['value'])
                
                if(WebMove['field_move_command'][0]['value'] == Move.find('.//name').text):
                    for field in self.TwoFields:
                        if self.IsMovePropertyDifferentFromWeb(WebMove, field['web'], Move, field['xml']):
                            Move.find('.//' + field['xml']).text = WebMove[field['web']][0]['value']
                            FoundDifferences = True
                            
                    
                    
                    for tag in self.TagsAndProperties:
                        FoundProperty = False
                        FoundTag = False
                        
                        tags = Move.find('.//tags')
                        for property in WebMove['field_move_properties']:
                            if property['value'] == tag['property']: #if property exists in webmove
                                FoundProperty = True                                
                        if tags.find('.//' + tag['tag']) != None: #if property exists in xml
                            FoundTag = True
                    
                        if FoundProperty and not FoundTag:
                            ET.SubElement(tags, tag['tag'])
                            FoundDifferences = True
                        if not FoundProperty and FoundTag:
                            tags.remove(tags.find('.//' + tag['tag']))
                            FoundDifferences = True
                        
    #                WebMove['field_move_properties'][0]['value'] = self.ConvertTagsToProperties(moveXML.find(".//tags"))
                    
    #                gameIdsArray = []
    #                gameIds = moveXML.findall(".//gameIds/gameId")
    #                for id in gameIds:
    #                    gameIdsArray.append({"value": id.text})
    #                WebMove['field_move_game_ids'][0]['value'] = gameIdsArray
            else:
                self.AddAPIMoveToXML(WebMove, movelist)
                #print(WebMove['field_move_command'][0]['value'] + " has no XMLId")
                
        if FoundDifferences:
            movelist.Save()

    def AddCharacterAndMovesToWeb(self, TekkenCharID):
        WebChar = self.GetWebCharacterByID(TekkenCharID)
        if WebChar == None:
            m = MoveList(TekkenCharID)
            self.AddCharacterToWeb(m)
            WebChar = self.GetWebCharacterByID(TekkenCharID)
            ids = m.GetAllMoveIds()
            for id in ids:
                move = m.getMoveById(id)
                self.AddMoveForCharacter(WebChar['nid'][0]['value'], move)
    
            m.Save()
        
        else:
            print(WebChar['nid'][0]['value'])
        
if __name__ == "__main__":

    a = AcademyAPI()
    if a.IsLoggedIn() != True:
        a.GetLoginCredentials()
        if a.login() != True:
            sys.exit("Error: Not logged in.")

    #print(a.GetWebCharacterByID(19)['menu_link'])
    
    CharID = 51
    
    a.AddCharacterAndMovesToWeb(CharID)
    
    
    #a.AddAPIMoveToXML(None, m)
    #move = m.getMoveById(10)

       
    
    
    #a.UpdateXMLFromAPI(m)
    #move = m.getMoveById(4)
    
    
    
    
    #ids = m.GetAllMoveIds()
    #for id in ids:
    #    move = m.getMoveById(id)
    #    a.UpdateMoveForCharacter(7, move)
        
    #move = m.getMoveById(2)
    #print(a.DoesMoveExistInSite("Nina Williams", move))
    
    #a.AddMoveForCharacter(7, move)
    #m.Save()
    
    