import os

os.system("pip3 install playsound")

import time, playsound
class SoundPlayer:
	def __init__(self, path, game):
		self.path = path
		self.game = game
	def play(self):
		if self.game.settings_button.dict["audio"]:
			playsound.playsound(self.path)
