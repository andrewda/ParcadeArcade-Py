# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:26:00 2016

@author: joe_b
"""

import grovepi
import requests
import json
import lcd

#from enum import Enum
#
#class IoTypes(Enum):
#    DigitalIn = 1
#    DigitalOut = 2
#    AnalogIn = 3
#    AnalogOut = 4
#    I2C = 5
#    RPISER = 6
#    SERIAL = 7

greenLed = 2
grovepi.pinMode( greenLed, "OUTPUT" )
grovepi.digitalWrite( greenLed, 1 )

lcd.setRGB( 128, 0, 0 ) # red

class Capability(dict):
    id = 0
    moteId = 0
    name = "button"
    port = 0
    ioType = 1
    def __init__(self, name, port, ioType):
        self.name = name 
        self.port = port
        self.ioType = ioType
        
    def toDict(self):
        x = { "name" : self.name, "port" : self.port, "ioType" : self.ioType, "moteId" : self.moteId}
        return x
    
class Mote:
    id = 0
    name = "Simon"
    description = "Simon Game in Main Hall"
    capabilities = []
    def __init__(self, name, description,capabilities=[]):
        self.name = name
        self.description = description
    
    def addCapability( self, capability ):
        self.capabilities.append( capability )
    
#    def to_JSON(self):
#        json_string = json.dumps([ob.__dict__ for ob in myMote.capabilities])
#        return json.dumps(self, default=lambda o: o.__dict__, 
#            sort_keys=True, indent=4)
    
    def toDict(self):
        x = { "name": self.name, "description" : self.description }
        #clist = [ ob.toDict() for ob in myMote.capabilities ]
        #x["capabilities"] = clist
        return x
        
    def to_JSON(self):        
        myStr = '"name": "' + self.name +'", '
        myStr += '"description": "' + self.description +'", ' 
        myStr += '"id": ' + str(self.id) +', '
        myStr += '"capabilities": ' + json.dumps([ob.__dict__ for ob in myMote.capabilities])
        #myStr += '}'
        myStr = myStr.replace('\n', ' ').replace('\r', '').replace( '\t', '' )
        return myStr
            
    def to_JSON2(self):
        json_string = ',"capabilities": ' + json.dumps([ob.__dict__ for ob in myMote.capabilities])
        self_string = json.dumps(self.__dict__, sort_keys=True, indent=4)
        q1 = self_string.find('[')
        q2 = self_string.find(']')
        p1 = self_string[:q1]
        p3 = self_string[q2+1:]
        mystring = (p1+json_string + "}").replace('\n', ' ').replace('\r', '').replace( '\t', '' )
        return mystring
            
class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return {"__enum__": str(obj)}
        return json.JSONEncoder.default(self, obj)

def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(globals()[name], member)
    else:
        return d
            
myMote = Mote( 0, "Simon", "My new Simon" )
#myMote.addCapability( Capability( "Button 1", 2, 1 ) )
#myMote.addCapability( Capability( "Button 2", 3, 1 ) )
myMote.addCapability( Capability( "Green LED", 2, 2 ) )

#json_string = json.dumps([ob.__dict__ for ob in myMote.capabilities], cls=EnumEncoder)
#print json_string

#myJson =  myMote.to_JSON()
#print "<snip>"
#print myMote.toDict()
#print "</snip>"
# post = json.dumps(myMote)

# myJson = {     "description": "My new Simon",      "id": 0,      "name": "Simon" ,"capabilities": '[{"ioType": 1, "name": "Button 1", "port": 2}, {"ioType": 1, "name": "Button 2", "port": 3}]' }
url = 'http://192.168.0.101:1337/add_listener'
header = {'content-type': 'application/json'}
foo = requests.post(url, params=myMote.toDict(), headers=header)
rslt = json.loads( foo.text)
id = rslt["response"]["id"]
myMote.id = id

for ob in myMote.capabilities:
    ob.moteId = id
    

grovepi.digitalWrite( greenLed, 0 )

addCapUrl = 'http://192.168.0.101:1337/add_capability'
clist = [ requests.post(addCapUrl, params=ob.toDict(), headers=header) for ob in myMote.capabilities ]

#foo = requests.post('http://192.168.0.101:1337/add_listener', params=myJson, headers )
print(myMote.id)

from flask import Flask, request
app = Flask(__name__)

@app.route("/", methods=['POST'])
def receive_json():
    content = request.get_json()
    if content is None:
        return "Unable to retrieve JSON\n"
    print(content)
    return "Success\n"

@app.route("/set", methods=['POST'])
def respond():
#    content = request.get_json()
#    print('foo: '+ str(content))
#    print('fum ' + str(request))
#    print('fie ' + str(request.data))
#    print('fiy ' + str(request.args))
#    print('bye ' + str(request.values))

    port = request.args["port"]
    value = request.args["value"]
    ioType = request.args["ioType"]
    
    print( 'port: ' + port )
    print( 'value: ' + value )
    print( 'ioType: ' + ioType )
    
    grovepi.digitalWrite( int(port), int(value) )
    
#    for ob in myMote.capabilities:
#        print ob.name + " " + ob.port + " " + ob.value
        
#        if int(port) == ob.port and int(ioType) == ob.ioType:     
#            grovepi.digitalWrite( ob.port, ob.value )
#            print "setting port: " + port + "  ioType: " + ioType
#        else:
#            print "port: " + port + "  ioType: " + ioType
    
    return "Success\n"


app.run(host = '0.0.0.0')