# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 19:41:47 2016

@author: joe_b
"""

DigitalIn = 1
DigitalOut = 2
AnalogIn = 3
AnalogOut = 4
I2C = 5
RPISER = 6
SERIAL = 7

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
            