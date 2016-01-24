"""
SMART HOUSE SECURITY - FACE RECOGNITION
RASPBERRY PI TRAINER - [INTERMEDIATE LEVEL]

This class is about the configuration of the hardware parts, like the Servo Motor and Push Button
This class handles the events for input and output of the Face Recognition.
The Raspberry Pi have two types of pin configurations, GPIO and BOARD.
We will be using the BOARD Configuration for our PINS.
We will be using the Servo Blaster Library for the Servo Control.
Push Button will act as INPUT and is connected to PIN 3 of the Raspberry Pi. (Refer to config.py)
Servo Motor will act as OUTPUT for the Door in the SMART HOUSE and is connected to PIN 7 of the Raspberry Pi.


Date Created: December 12, 2015
Created by: Harvey Oroceo, BSCpE
"""
import time # For delay

import RPi.GPIO as GPIO # GPIO Library
import os # For terminal-based commands

import config # Include the config script
import face # Include the face script

"""
Class to represent the state and encapsulate access to the hardware of the SMART HOUSE
"""
class Door(object):
        
        GPIO.setmode(GPIO.BOARD) # Use the P1 Header of the Raspberry Pi
	
	def __init__(self):
		GPIO.setup(config.BUTTON_PIN, GPIO.IN)
		self.button_state = GPIO.input(config.BUTTON_PIN)
		self.is_locked = None

	def lock(self):
                        """Lock the Door."""
                        os.system("echo P1-7=20% > /dev/servoblaster") # Close at 20% Servo Motor will heat up if the value is lower.
                        self.is_locked = True

	def unlock(self):
                        """Unlock the Door."""
                        os.system("echo P1-7=100% > /dev/servoblaster") # Open at 100%.
                        self.is_locked = False

	def is_button_up(self):
                                #Return True when the Push Button has transitioned between pressed and unpressed.
		old_state = self.button_state
		self.button_state = GPIO.input(config.BUTTON_PIN)

		# Check if transition from down to up
		if old_state == config.BUTTON_DOWN and self.button_state == config.BUTTON_UP:
			# Wait 20 milliseconds and measure again to debounce switch.
			time.sleep(20.0/1000.0)
			self.button_state = GPIO.input(config.BUTTON_PIN)
			if self.button_state == config.BUTTON_UP:
				return True
		return False
