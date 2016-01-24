"""
SMART HOUSE SECURITY - FACE RECOGNITION
RASPBERRY PI TRAINER - [INTERMEDIATE LEVEL]

Webcam Camera class for OpenCV. This class allows you to capture a single image
from the webcam as an OpenCV image.

Date Created: December 12, 2015
Created by: Harvey Oroceo, BSCpE
"""

import io # Include for Stream Handling
import time # Include for Delay
import os # Include os in order to enable Terminal-Based commands.

import cv2 # Include OPENCV 3.0.0 library
import config # Include config.py script


class OpenCVCapture(object):
	def read(self):
		camera_port = 0 # Webcam port
		camera = cv2.VideoCapture(camera_port) # Capture using OpenCV

		def get_image():
                        retval, im = camera.read()
                        return im

                camera_capture = get_image()
                file = "/home/pi/image.jpg"
                cv2.imwrite(file, camera_capture)
                camera.release()

                return camera_capture
