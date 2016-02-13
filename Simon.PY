import time
import grovepi
import random
import lcd
#from enum import Enum

#192.168.0.102
#LightChoice = Enum('LightChoice', 'red blue')

redSens = 8
blueSens = 7
red = 3
blue = 4
grovepi.pinMode(redSens,"INPUT")
grovepi.pinMode(blueSens,"INPUT")
grovepi.pinMode(red,"OUTPUT")
grovepi.pinMode(blue,"OUTPUT")
comTurn = True
seleccion = 0
gameLength = 9
seleccionLog = range(1,gameLength)
for num in range(1,gameLength):
	try:
		if comTurn:
			if random.randint(1, 2) == 1:
				grovepi.digitalWrite(red,1)
				grovepi.digitalWrite(blue,0)
				seleccion = 8 #LightChoice.red
				print "red picked"
			else: 
				grovepi.digitalWrite(blue,1)
				grovepi.digitalWrite(red,0)
				seleccion = 7#LightChoice.blue
				print "blue picked"
			seleccionLog[num] = seleccion
			time.sleep(2)
			grovepi.digitalWrite(blue,0)
			grovepi.digitalWrite(red,0)
			comTurn = False
		for item in range(1,num):
			waiting = True
			while(waiting):
				if (grovepi.ultrasonicRead(redSens)) < 20:
					if (seleccionLog[item] == 8):
						print "Winner!"
						waiting = False
					else:
						print "Loser!"
						waiting = False
				if (grovepi.digitalRead(blueSens)) ==1:
					if (seleccionLog[item] == 7):
						print "Winner!"
						waiting = False
					else:
						print "Loser!"
						waiting = False
	except TypeError:
		print(TypeError)
	except IOError:
			print(IOError)
