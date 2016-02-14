import time
import grovepi
import random
import lcd
#from enum import Enum

#192.168.0.102
#LightChoice = Enum('LightChoice', 'red blue')

followSens = 7
lightShow = 2
grovepi.pinMode(followSens,"INPUT")
grovepi.pinMode(lightShow,"OUTPUT")

fadenum = 0.01
colors = { 'red' : 0 , 'green' : 32 , 'blue' : 64 }

def init_state( r , g , b ):
	colors =  { 'red' : r , 'green' : g, 'blue' : b } 
	lcd.setRGB(colors['red'],colors['green'],colors['blue']) #set the light to red initially
	return colors

lev = range(128) #generate a list 0-128 to allow control of  LCD light level

def fade(level,color,sleep_time):
	if color=="red":
		for l in level:
			lcd.setRGB(level[l],0,0)
			time.sleep(sleep_time) #long enough to notice color change
	elif color=="green":
		for l in level:
			lcd.setRGB(0,level[l],0)
			time.sleep(sleep_time) #long enough to notice color change
	elif color=="blue":
		for l in level:
			lcd.setRGB(0,0,level[l])
			time.sleep(sleep_time) #long enough to notice color change
	elif color=="yellow":
		for l in level:
			lcd.setRGB(level[l],level[l],0)
			time.sleep(sleep_time) #long enough to notice color change
	elif color=="bluegreen":
		for l in level:
			lcd.setRGB(0,level[l],level[l])
			time.sleep(sleep_time) #long enough to notice color change
	elif color=="purple":
		for l in level:
			lcd.setRGB(level[l],0,level[l])
			time.sleep(sleep_time) #long enough to notice color change
	elif color=="white":
		for l in level:
			lcd.setRGB(level[l],level[l],level[l])
			time.sleep(sleep_time) #long enough to notice color change

def cycle(sleep_time):
	fade(lev,"red",sleep_time)
	fade(lev,"yellow",sleep_time)
	fade(lev,"green",sleep_time)
	fade(lev,"bluegreen",sleep_time)
	fade(lev,"blue",sleep_time)
	fade(lev,"purple",sleep_time)
	fade(lev,"white",sleep_time)
	
def whiteflash():
	flash = (128 - grovepi.ultrasonicRead(followSens))

	if flash > colors['red'] and colors['red'] > 0 :
		r = flash
	else:
		r = colors['red']		
	if flash > colors['green'] and colors['green'] > 0 :
		g = flash
	else:
		g = colors['green']	
	if flash > colors['blue'] and colors['blue'] > 0:
		b = flash
	else:
		b = colors['blue']
	
	lcd.setRGB( r , g , b )
	
def multiply():
	flash = (128 - grovepi.ultrasonicRead(followSens))
	multiplier = flash * 0.2
	
	flash_red = colors['red'] * multiplier
	flash_green = colors['green'] * multiplier
	flash_blue = colors['blue'] * multiplier
	
	if flash_red >= 128 :
		r = 128
	elif flash_red > colors['red'] :
		r = flash_red
	else:
		r = colors['red']
	
	if flash_green >= 128 :
		g = 128
	elif flash_green > colors['green'] :
		g = flash_green
	else:
		g = colors['green']	
	
	if flash_blue >= 128 :
		b = 128
	elif flash_blue > colors['blue'] :
		b = flash_blue
	else:
		b = colors['blue']
	
	lcd.setRGB( r , g , b )
	
def darken():
	shade = grovepi.ultrasonicRead(followSens)
	
	if shade < colors['red']:
		r = shade
	else:
		r = colors['red']		
	if shade < colors['green']:
		g = shade
	else:
		g = colors['green']	
	if shade < colors['blue']:
		b = shade
	else:
		b = colors['blue']
	
	lcd.setRGB( r , g , b )

def filter_cycle ():			
	sens_flag = True
	while sens_flag:
		try:
			value = grovepi.ultrasonicRead(followSens)
			print( "Sensor = " + str(value))
			if value<150:			# Read the sensor value.
				cycle(fadenum)		# If we get a sensation of relative proximity, do a little dance.
				time.sleep(fadenum*896)
				print('Got sensor movement')
				init_state( colors['red'] , colors['green'] , colors['blue']  )
				# sens_flag=False
		except TypeError:
			print(TypeError)
		except IOError:
			print(IOError)

def filter_whiteflash ():			
	sens_flag = True
	while sens_flag:
		try:
			value = grovepi.ultrasonicRead(followSens)
			print( "Sensor = " + str(value))
			if value>128:			# Read the sensor value.
				init_state( colors['red'] , colors['green'] , colors['blue']  )
			else:
				whiteflash()		# If we get a sensation of relative proximity, do a little dance.
		except TypeError:
			print(TypeError)
		except IOError:
			print(IOError)
			
def filter_multiply ():			
	sens_flag = True
	while sens_flag:
		try:
			value = grovepi.ultrasonicRead(followSens)
			print( "Sensor = " + str(value))
			if value>128:			# Read the sensor value.
				init_state( colors['red'] , colors['green'] , colors['blue']  )
			else:
				multiply()		# If we get a sensation of relative proximity, do a little dance.
		except TypeError:
			print(TypeError)
		except IOError:
			print(IOError)
			
def filter_darken ():			
	sens_flag = True
	while sens_flag:
		try:
			shade = grovepi.ultrasonicRead(followSens)
			print( "Sensor = " + str(shade))
			if shade>128:			# Read the sensor value.
				init_state( colors['red'] , colors['green'] , colors['blue']  )
			else:
				darken()		# If we get a sensation of relative proximity, do a little dance.
		except TypeError:
			print(TypeError)
		except IOError:
			print(IOError)
			

init_state( 64 , 2, 1 )
filter_cycle()
