# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:26:00 2016

@author: joe_b
"""

import requests
import json
from enum import Enum

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
    ioType = 1
    def __init__(self, id, name, port, ioType):
        self.id = id
        self.name = name 
        self.port = port
        self.ioType = ioType
    
class Mote:
    id = 0
    name = "Simon"
    description = "Simon Game in Main Hall"
    capabilities = []
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
    
    def __addCapability__( self, capability ):
        self.capabilities.append( capability )
    
    def to_JSON(self):
        json_string = json.dumps([ob.__dict__ for ob in myMote.capabilities])
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
            
myMote = Mote( 0, "Simon", "My new Simon" )
myMote.capabilities.append(Capability( 0, "Button", 2, 1 ))

json_string = json.dumps([ob.__dict__ for ob in myMote.capabilities])

print json_string
print myMote.to_JSON()

# post = json.dumps(myMote)

data = myMote.to_JSON()
foo = requests.post('http://192.168.0.106:1337/echo/', params=data)
print(foo.text)