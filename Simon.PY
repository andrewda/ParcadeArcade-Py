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
selection = 0
gameLength = 10
selectionLog = range(0,gameLength)
readyToPlay = False
while True:
	readyToPlay = (grovepi.ultrasonicRead(redSens) < 200) or (grovepi.ultrasonicRead(blueSens) < 200)
	if readyToPlay:
		try:
			for item in range(0,gameLength):
				if random.randint(1, 2) == 1:
					selectionLog[item] = 0
				else: 
					selectionLog[item] = 1
			for num in range(0,gameLength):
				for item in range(0, num):
					if selectionLog[item] == 0:
						grovepi.digitalWrite(red,1)
						grovepi.digitalWrite(blue,0)
						print "red picked"
					else:
						grovepi.digitalWrite(blue,1)
						grovepi.digitalWrite(red,0)
						print "blue picked"
					time.sleep(1)
					grovepi.digitalWrite(blue,0)
					grovepi.digitalWrite(red,0)
					time.sleep(1)
				waiting = True
				lost = False
				outOfTime = False
				for item in range(0, num):
					initTime = time.time()
					while(waiting and not lost and not outOfTime):
						outOfTime = (time.time() - initTime) > 10
						if (grovepi.ultrasonicRead(redSens)) < 20:
							if (selectionLog[item] == 0):
								print "Winner!"
								waiting = False
								grovepi.digitalWrite(red,1)
								time.sleep(1)
								grovepi.digitalWrite(red,0)
							else:
								print "Loser!"
								waiting = False
								lost = True
								grovepi.digitalWrite(blue,1)
								grovepi.digitalWrite(red,1)
								time.sleep(1)
								grovepi.digitalWrite(blue,0)
								grovepi.digitalWrite(red,0)
						if (grovepi.ultrasonicRead(blueSens)) < 20:
							if (selectionLog[item] == 1):
								print "Winner!"
								waiting = False
								grovepi.digitalWrite(blue,1)
								time.sleep(1)
								grovepi.digitalWrite(blue,0)
							else:
								print "Loser!"
								waiting = False
								lost = True
								grovepi.digitalWrite(red,1)
								grovepi.digitalWrite(blue,1)
								time.sleep(1)
								grovepi.digitalWrite(red,0)
								grovepi.digitalWrite(blue,0)
					waiting = True
		except TypeError:
				print(TypeError)
		except IOError:
				print(IOError)
