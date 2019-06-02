import time

from pynput.keyboard import Key, Listener, Controller
from FeatureVector import *

import bcs_parameters as parameters

key_press_time = 0
key_release_time = 0
text = ""
inputLen = 0
keyboard = Controller()
vector = FeatureVector()


def on_press(key):
	"""
	:param key: the key being pressed

	event listener for key down events
	"""

	global text
	global vector
	global key_press_time
	key_press_time = time.time()

	to_append = str(key)[2:-1]
	if len(to_append) == 1:
		text = text + to_append

	vector.append_delay(int(str((key_press_time - key_release_time) * 1000).split(".")[0]))


def on_release(key):
	"""
	:param key: the key being released

	event listener for key up event
	"""

	global vector
	global inputLen
	inputLen = inputLen + 1
	global key_release_time
	key_release_time = time.time()

	if key == Key.tab:
		return False
	
	if key != Key.enter:
		vector.append_duration(int(str((key_release_time - key_press_time) * 1000).split(".")[0]))


def clear_keyboard_buffer(input_len):
	"""
	:param input_len: the length of already entered input

	clear the console buffer in order to prevent leaking the password to the console
	and also maintain a clear console structure ^^
	"""

	while input_len > 0:
		keyboard.press(Key.backspace)
		keyboard.release(Key.backspace)
		input_len = input_len - 1
	

def read_input(rounds):
	"""
	:param rounds: how often an input should be read
	:return: lists of features and passwords entered

	read the password / user input for a specified number of times
	"""

	global text
	global vector
	passwords = []
	features = ""
	
	for i in range(0, rounds):
		vector = FeatureVector()
		text = ""

		with Listener(on_press=on_press, on_release=on_release) as listener:
			listener.join()
	
		passwords.append(text)	
		features = features + vector.get_features_string() + "\n"

	return features, passwords
