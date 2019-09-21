import requests
import json
import sys
import time
from urllib.parse import urlencode

############################################################
# Helper Functions

def pprint(text):
  s = str(text)
  sys.stdout.write(s + '\n')
  sys.stdout.flush()

def login(auth):
  login = {}
  login['name'] = auth['name']
  login['pass'] = auth['pass']
  l = json.dumps(login)

  req = requests.post(auth['location'], data=l)

  auth['head'] = {}
  auth['cookie'] = {}
  if req.status_code == 200:
    r = json.loads(req.text)
    auth['head']['X-CSRF-Token'] = r['csrf_token']
    auth['head']['Accept'] = 'application/json'
    auth['head']['Content-Type'] = 'application/json'
    auth['cookie'] = req.cookies.get_dict()
    return auth
  else:
    pprint("RemoteConf Login failed. Message from Server:")
    pprint(req.text)
    return False

############################################################
# Script Settings

auth = {}
auth['location'] = "https://tekken.academy/user/login?_format=json"
auth['name'] = ""
auth['pass'] = ""

post_data = {}
#post_data['_links'] = {}
#post_data['_links']['type'] = {}
#post_data['_links']['type']['href'] = "https://tekken.academy/rest/type/node/article"
post_data['title'] = [{"value":"Asdf"}]
post_data['type'] = [{'target_id': "move"}]
post_data['field_move_command'] = [{"value":"1,2,3"}]
post_data['field_move_for_character'] = [{"target_id": 7}]
get_data = {}

############################################################
# Log in and run test posts

auth = login(auth)

# Test POST
pd = json.dumps(post_data)
#print(pd)
pst = requests.post('https://tekken.academy/node?_format=json', data=pd, headers=auth['head'], cookies=auth['cookie'])
pprint(pst.text)





