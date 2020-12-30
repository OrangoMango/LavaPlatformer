from tkinter import messagebox
import re

class Statistics:
	def __init__(self, game):
		self.game = game
	def __del__(self):
		try:
			self.game.canvas.delete(self.t1)
			self.game.canvas.delete(self.back_button)
			self.game.canvas.delete(self.t2)
			self.game.canvas.delete(self.back_button_x)
		except:
			pass
	def show_button(self):
		self.id_out = self.game.canvas.create_rectangle(320, 430, 480, 480, fill="green", tags="statistics_button")
		self.id_in = self.game.canvas.create_text(330, 440, anchor="nw", text="STATISTICS", tags="statistics_button", font="Calibri 15 bold")
		self.id = "statistics_button"
		self.game.canvas.tag_bind(self.id, "<Button-1>", self.onclick)
	def onclick(self, event):
		self.t1 = self.game.canvas.create_rectangle(0,0, 500,500, fill="lightblue")
		#messagebox.showinfo("Statistics", self.game.statistics, master=self.game.tk)

		self.show_data()
		self.show_backbutton()
		self.game.canvas.tag_bind(self.back_button, "<Button-1>", self.back)
	def show_data(self):
		text = ""
		for key, value in self.game.statistics.items():
			text += re.sub("_", " ", key)+": "+str(value)+"\n"
		text += "coins: "+str(self.game.coins)
		self.t2 = self.game.canvas.create_text(30, 30, text=text, anchor="nw", font="Purisa 23 bold")
	def show_backbutton(self):
		self.back_button_x = self.game.canvas.create_rectangle(20, 420, 120, 480, fill="red", tags="backbutton")
		self.back_button_y = self.game.canvas.create_text(30,430, anchor="nw", font="Calibri 19 bold", tags="backbutton", text="BACK")
		self.back_button = "backbutton"
	def back(self, event):
		self.__del__()
		
