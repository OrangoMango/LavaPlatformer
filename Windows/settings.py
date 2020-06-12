from tkinter import *
from tkinter import messagebox
import os, json

class Settings:
	def __init__(self, game):
		self.game = game
		try:
			self.load_data()
		except:
			self.dict = {"popups":{"value":1, "levels":1, "jobs":1}, "audio":1}
	def show_button(self):
		self.image = PhotoImage(file="../Data/Images/settings.gif", master=self.game.tk)
		self.id = self.game.canvas.create_image(150, 430, image=self.image, anchor="nw")
		self.game.canvas.tag_bind(self.id, "<Button-1>", self.show_settings)
		
	def save_data(self):
		os.chdir(self.game.path4job)
		with open("settings.json", "w") as f:
			json.dump(self.dict, f, indent=4)
		
	def load_data(self):
		os.chdir(self.game.path4job)
		with open("settings.json", "r") as f:
			self.dict = json.load(f)
		
	def show_settings(self, event):
		tk = Tk()
		tk.title("LavaPlatformer settings")
		
		popups = LabelFrame(tk, text="Pop-ups")
		popups.pack()
		
		allow = StringVar(master=tk)
		allow.set(str(self.dict["popups"]["value"]))
		
		def act():
			if int(allow.get()):
				c1.config(state="normal")
				c2.config(state="normal")
			else:
				c1.config(state="disabled")
				c2.config(state="disabled")
		
		sh = Checkbutton(popups, text="Show popups", variable=allow, command=act, onvalue="1", offvalue="0")
		sh.pack()
		Label(popups, text=" ").pack()
		
		c1var = IntVar(master=tk)
		c1var.set(self.dict["popups"]["levels"])
		c2var = IntVar(master=tk)
		c2var.set(self.dict["popups"]["jobs"])
		
		c1 = Checkbutton(popups, text="Level passed", state="disabled" if not self.dict["popups"]["value"] else "normal", variable=c1var, onvalue=1, offvalue=0)
		c1.pack()
		c2 = Checkbutton(popups, text="Job completed", state="disabled" if not self.dict["popups"]["value"] else "normal", variable=c2var, onvalue=1, offvalue=0)
		c2.pack()
		
		def save():
			#print(os.getcwd())
			self.dict["popups"]["value"] = int(allow.get())
			self.dict["popups"]["levels"] = c1var.get()
			self.dict["popups"]["jobs"] = c2var.get()
			self.dict["audio"] = audiovar.get()
			#print(self.dict)
			self.save_data()
			tk.destroy()
		
		def cancel():
			tk.destroy()
		
		audiovar = IntVar(master=tk)
		audiovar.set(self.dict["audio"])
		
		audio = Checkbutton(tk, text="Allow sounds", variable=audiovar, onvalue=1, offvalue=0)
		audio.pack()
		
		b = Button(tk, text="SAVE", command=save)
		b.pack()
		b2 = Button(tk, text="CANCEL", command=cancel)
		b2.pack()