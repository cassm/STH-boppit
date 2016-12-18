#/bin/python
#bopit game code - teamHnnnng
#comments are the documentation >.>

#imports - gpio, time for pwm, serial because serial
import RPi.GPIO as GPIO
import time as time
import serial as serial 
# pygame - for sounds
import pygame
# random for randomness
import random

#init audio
pygame.mixer.init()

#define pin layouts as we'd expect the board to look - https://pinout.xyz/
GPIO.setmode(GPIO.BOARD)
dc = 40
#we'll take pin 40 for vibe 1
GPIO.setup(40, GPIO.OUT)
pwm1 = GPIO.PWM(40, 50)
#and 38 for 2
GPIO.setup(38, GPIO.OUT)
pwm2 = GPIO.PWM(38, 50)

# Here we define the serial port we're going to use. Hilariously, on the pi3 for
# the TTL lines this needs to be ttys0, as AMA0 becomes the bluetooth interface
# however this code is running on a pi2 and as this is being written in a
# hackathon, so I'm not going to write code identifying host device today. 
ser = serial.Serial(              
      port='/dev/ttyUSB0',
      baudrate = 115200,
      parity=serial.PARITY_NONE,
      stopbits=serial.STOPBITS_ONE,
      bytesize=serial.EIGHTBITS,
      timeout=1
      )

# Let's define a few commands
twist = 'T'
pull = 'P'
flick = 'F'
spin = 'S'
bop1 = '1'
bop2 = '2'
bop = (bop1,bop2)

options = (twist,pull,flick,spin,bop)


# Start your engines please
pwm1.start(0)
pwm2.start(0)
pwm1.ChangeDutyCycle(40) 
pwm2.ChangeDutyCycle(40) 
pattern = 0
freq = 50.0

buf = ''

#game code:
#twist, pull, bop1 p1
#flick, spin, bop2 p2
while 1:
  action = random.randint(0,4)
  if action == 0:
        pygame.mixer.music.load("twistit.wav")
	pygame.mixer.music.play()
        print options[action]
  elif action == 1: 
        pygame.mixer.music.load("pullit.wav")
	pygame.mixer.music.play()
        print options[action]
  elif action == 2:
        pygame.mixer.music.load("flickit.wav")
	pygame.mixer.music.play()
        print options[action]
  elif action == 3:
        pygame.mixer.music.load("spinit.wav")
	pygame.mixer.music.play()
        print options[action]
  else:
        pygame.mixer.music.load("bopit.wav")
	pygame.mixer.music.play()
        print options[action]
                          
# Next, a disgusting while command to read the buffer continously
  while 1:
    buf += ser.read(1)
    if action == 4:
        if buf == bop1:
           freq = freq * 2
           pwm1.ChangeFrequency(freq)
           break
        elif buf == bop1:
           freq = freq * 2
           pwm1.ChangeFrequency(freq)
           break
    elif buf == options[action]:
        # twist it = pattern change
	if dc < 91:
         dc = dc + 10
	pwm1.ChangeDutyCycle(dc) 
	pwm2.ChangeDutyCycle(dc) 
        buf = ''
 	break
    elif buf != '': 
        dc = 0
        freq = 50
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
	pwm1.ChangeFrequency(freq) 
	pwm2.ChangeFrequency(freq) 
        buf = ''
	break
