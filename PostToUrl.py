# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 23:26:00 2016

@author: joe_b
"""

import grovepi
import requests
import json
import lcd
import mote

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

myMote = mote.Mote( 0, "Simon", "My new Simon" )
#myMote.addCapability( mote.Capability( "Button 1", 2, 1 ) )
#myMote.addCapability( mote.Capability( "Button 2", 3, 1 ) )
myMote.addCapability( mote.Capability( "Green LED", 2, 2 ) )

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