#/bin/python
#bopit remote code - teamHnnnng
#comments are the documentation >.>

#imports - gpio, time for pwm, serial because serial
import RPi.GPIO as GPIO
import time as time
import serial as serial 
# pygame - for sounds
import pygame

#init audio
pygame.mixer.init()

#define pin layouts as we'd expect the board to look - https://pinout.xyz/
GPIO.setmode(GPIO.BOARD)

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



# Start your engines please
pwm1.start(0)
pwm2.start(0)
pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(0) 

pattern = 0
freq = 50.0
dc = 0

# Next, a disgusting while command to read the buffer continously
buf = ''
while 1:
    buf += ser.read(1)
    if buf == twist:
        # twist it = pattern change
	freq = freq * 2
	pwm1.ChangeFrequency(freq) 
	pwm2.ChangeFrequency(freq) 
        pygame.mixer.music.load("twistit.wav")
	pygame.mixer.music.play()
        print buf
        buf = ''
    if buf == flick:
        # amplitude up
        if dc < 91: 
 	 dc = dc + 10 
        pwm1.ChangeDutyCycle(dc)
        pwm2.ChangeDutyCycle(dc)
        pygame.mixer.music.load("flickit.wav")
	pygame.mixer.music.play()
        print buf
        buf = ''
    if buf == spin:
        freq = freq / 2
	pwm1.ChangeFrequency(freq) 
	pwm2.ChangeFrequency(freq) 
        pygame.mixer.music.load("spinit.wav")
	pygame.mixer.music.play()
        print buf
        buf = ''
    if buf == bop1:
        # bop it = stop it
        dc = 0
	freq = 50.0
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
	pwm1.ChangeFrequency(freq) 
	pwm2.ChangeFrequency(freq) 
        pygame.mixer.music.load("bopit.wav")
	pygame.mixer.music.play()
        print buf

        buf = ''
    if buf == bop2:
        # bop it = stop it
        dc = 0
        freq = 50
        pwm1.ChangeDutyCycle(0)
        pwm2.ChangeDutyCycle(0)
	pwm1.ChangeFrequency(freq) 
	pwm2.ChangeFrequency(freq) 
        pygame.mixer.music.load("bopit.wav")
	pygame.mixer.music.play()
        print buf
        buf = ''
    elif buf == pull:
        # pull it -> speed down
	if dc > 9:
           dc = dc - 10 
        pwm1.ChangeDutyCycle(dc)
        pwm2.ChangeDutyCycle(dc)
        pygame.mixer.music.load("pullit.wav")
	pygame.mixer.music.play()
        print buf
        buf = ''

