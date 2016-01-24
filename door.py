"""
SMART HOUSE SECURITY - FACE RECOGNITION
RASPBERRY PI TRAINER - [INTERMEDIATE LEVEL]

This program was compiled and tested using RASPBERRY PI 2 B running RASPBIAN JESSIE.
This program is about checking if the user is allowed to enter by capturing their faces and comparing it to the existing Training Data Sets.
The training model is from the OPENCV 3.0.0 library which does the Machine Learning algorithms to recognize a human face.

Date Created: December 12, 2015
Created by: Harvey Oroceo, BSCpE
"""
import sys # Include this if this script can't be run properly.
sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2 # Include OPENCV 3.0.0 library

import config # Include config.py script
import face # Include face.py script
import hardware # Include hardware.py class
import os # Include os in order to enable Terminal-Based commands.

import select # Include for I/O

def is_letter_input(letter):
	# Utility function to check if a specific character is available on stdin.
	# Comparison is case insensitive.
	if select.select([sys.stdin,],[],[],0.0)[0]:
		input_char = sys.stdin.read(1)
		return input_char.lower() == letter.lower()
	return False


if __name__ == '__main__':
	# Load training data into model
	print 'Loading training data...'
	model = cv2.face.createEigenFaceRecognizer()
	model.load(config.TRAINING_FILE)
	print 'Training data loaded!'
	
	# Initialize camera and door.
	camera = config.get_camera()
	door = hardware.Door()
	# Move box to locked position.
	door.lock()
	print 'Running Face Detection Software'
	print 'Press button to lock (if unlocked), or unlock if the correct face is detected.'
	print 'Press and Enter c for Manual Button Press.'
	print 'Press Ctrl-C to quit.'
	while True:
		# Check if capture should be made.
		# TODO: Check if button is pressed.
		if door.is_button_up() or is_letter_input('c') :
			if not door.is_locked:
				# Lock the door if it is unlocked
				door.lock()
				print 'Door is now locked.'
			else:
				print 'Button pressed, looking for face...'
				os.system("mpg123 holdstill.mp3")
				# Check for the positive face and unlock if found.
				image = camera.read()
				# Convert image to grayscale.
				image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
				# Get coordinates of single face in captured image.
				result = face.detect_single(image)
				if result is None:
					print 'Could not detect single face!  Check the image in capture.pgm' \
						  ' to see what was captured and try again with only one face visible.'
					continue
				x, y, w, h = result
				# Crop and resize image to face.
				crop = face.resize(face.crop(image, x, y, w, h))
				# Test face against model.
				label, confidence = model.predict(crop)
				print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
					'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', 
					confidence)
				if label == config.POSITIVE_LABEL and confidence < config.POSITIVE_THRESHOLD:
					print 'Recognized face!'
					os.system("mpg123 accessgranted.mp3")
					door.unlock()
				else:
					print 'Did not recognize face!'
					os.system("mpg123 accessdenied.mp3")
