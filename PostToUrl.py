# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:26:00 2016

@author: joe_b
"""

import requests
import json
from enum import Enum
import urllib2

class IoTypes(Enum):
    DigitalIn = 1
    DigitalOut = 2
    AnalogIn = 3
    AnalogOut = 4
    I2C = 5
    RPISER = 6
    SERIAL = 7


class Capability(dict):
    id = 0
    name = "button"
    port = 0
    ioType = IoTypes.AnalogIn
    def __init__(self, id, name, port, ioType):
        self.name = name 
        self.port = port
        self.ioType = ioType
    
class Mote:
    id = 0
    name = "Simon"
    description = "Simon Game in Main Hall"
    capabilities = []
    def __init__(self, id, name, description,capabilities=[]):
        self.id = id
        self.name = name
        self.description = description
    
    def addCapability( self, capability ):
        self.capabilities.append( capability )
    
#    def to_JSON(self):
#        json_string = json.dumps([ob.__dict__ for ob in myMote.capabilities])
#        return json.dumps(self, default=lambda o: o.__dict__, 
#            sort_keys=True, indent=4)
    
    #def toDict(self):

    
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
myMote.addCapability( Capability( 0, "Button 1", 2, 1 ) )
myMote.addCapability( Capability( 1, "Button 2", 3, 1 ) )

#json_string = json.dumps([ob.__dict__ for ob in myMote.capabilities], cls=EnumEncoder)
#print json_string

myJson =  myMote.to_JSON()
print "<snip>"
print myJson
print "</snip>"
# post = json.dumps(myMote)

# myJson = {     "description": "My new Simon",      "id": 0,      "name": "Simon" ,"capabilities": '[{"ioType": 1, "name": "Button 1", "port": 2}, {"ioType": 1, "name": "Button 2", "port": 3}]' }
foo = requests.post('http://192.168.0.101:1337/add_listener', data=myJson )
print(foo.text)


#req = urllib2.Request('http://192.168.0.101:1337/add_listener?params='  )
#req.add_header('Content-Type', 'application/json')
#
#response = urllib2.urlopen(req, myJson)
#print response