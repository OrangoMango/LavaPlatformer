from tkinter import messagebox
from tkinter import colorchooser
from tkinter import *

import jobs, boxes, os

class Shop:
	
	def save(self):
		self.game.save_json_data(val=self.game.from_json["colors"]+[self.game.color] if not self.game.color in self.game.from_json["colors"] else self.game.from_json["colors"])
		self.game.load_json_statistics(True)
		self.game.canvas.itemconfig(self.game.player_shop.id, fill=self.game.selected)
		self.game.canvas.itemconfig(self.game.cointxt, text="Coins: {0}".format(self.game.coins))
		self.game.canvas.itemconfig(self.game.keystxt, text="Keys: {0}".format(self.game.keys))
	
	def __del__(self):
		try:
			self.game.canvas.delete(self.preview)
			self.game.canvas.delete(self.price)
			self.game.canvas.delete(self.purchease)
			self.game.canvas.delete(self.pricetxt)
			self.game.canvas.delete(self.purcheasetxt)
			self.game.canvas.delete(self.selection)
			self.game.canvas.delete(self.back)
			self.game.canvas.delete(self.t_1)
			self.game.canvas.delete(self.t_2)
			self.game.canvas.delete(self.t_3)
			self.game.canvas.delete(self.backtxt)
			self.game.canvas.delete(self.selectiontxt)
			self.game.canvas.delete(self.job_button.id)
			self.game.canvas.delete(self.box.id)
			self.game.canvas.delete(self.personaltxt)
		except:
			pass
		
		########SAVE DATA TO JSON#########
		
		self.save()
	
	def __init__(self, game, pt=""):
		self.game = game
		self.path = pt
		self.screen = True
		self.colors = ["black", "yellow", "light grey", "gray", "light slate gray", "dim gray", "lavender", "mint cream", "white", "antique white", "blanched almond", "peach puff", "navajo white", "lemon chiffon", "blue", "cornflower blue", "slate blue", "light slate blue", "royal blue", "deep sky blue", "turquoise", "dark green", "pale green", "spring green", "dark goldenrod", "orange", "red", "salmon", "pink", "deep pink", "purple", "SeaGreen2", "gold2", "SkyBlue1",   "lightblue"]
		self.prices = list(range(0,(len(self.colors)-1)*5, 5)) + [230]
		self.current = 0
		self.box = boxes.Box(self)
	def add_job(self):
		self.job_button = jobs.Job(self)
	#	self.job_button.save_progress()
	def show_button(self):
		#print(os.getcwd())
		os.chdir(self.path)
		self.image = PhotoImage(file=self.path+'Data/Images/shop.gif', master=self.game.tk)
		self.id_out = self.game.canvas.create_image(20, 400, anchor="nw", image=self.image, tags="shop_button")
		self.id = "shop_button"
		self.game.canvas.tag_bind(self.id, "<Button-1>", self.onclick)
	def onclick(self, event):
		#self.game.canvas.delete(self.id)
		self.t_1 = self.game.canvas.create_rectangle(0,0, 500, 500, fill="lightblue")
		self.option_skin_preview()
		
		self.job_button.show_button()
		self.box.show()
	
	def option_skin_preview(self):
		self.preview = self.game.canvas.create_rectangle(200, 100, 300, 200, fill=self.colors[self.current])
		self.price = self.game.canvas.create_rectangle(200, 250, 300, 285, fill="yellow")
		self.purchease = self.game.canvas.create_rectangle(150, 400, 350, 435, fill="green" if self.colors[self.current] not in self.game.from_json["colors"] else "gray")
		self.pricetxt = self.game.canvas.create_text(250, 270, text="$"+str(self.prices[self.current]), font="Calibri 14 bold", fill="red" if self.game.coins < self.prices[self.current] and not self.colors[self.current] in self.game.from_json["colors"] else "black")
		self.purcheasetxt = self.game.canvas.create_text(250, 420, text="PURCHEASE", font="Calibri 12 bold")
		self.t_3 = previous = self.game.canvas.create_text(150, 150, text="<", font="Calibri 40 bold")
		self.t_2 = next = self.game.canvas.create_text(350, 150, text=">", font="Calibri 40 bold")
		
		self.selection = self.game.canvas.create_rectangle(380, 10, 480, 45, fill="orange", tags="settingsbutton")
		self.selectiontxt1 = self.game.canvas.create_text(392, 15, anchor="nw", text="SELECTION", font="Calibri 12 bold", tags="settingsbutton")
		self.selectiontxt = "settingsbutton"
		self.back = self.game.canvas.create_rectangle(20, 10, 120, 50, fill="red", tags="backbutton")
		self.backtxt1 = self.game.canvas.create_text(25,15, anchor="nw", text="BACK", font="Calibri 17 bold", tags="backbutton")
		self.backtxt = "backbutton"
		self.personaltxt = self.game.canvas.create_text(175, 50, anchor="nw", text="", font="Calibri 12 bold")
		
		self.game.canvas.tag_bind(next, "<Button-1>", self.next)
		self.game.canvas.tag_bind(previous, "<Button-1>", self.previous)
		self.game.canvas.tag_bind(self.purcheasetxt, "<Button-1>", self.purchease_func)
		self.game.canvas.tag_bind(self.selectiontxt, "<Button-1>", self.show_selection)
		self.game.canvas.tag_bind(self.backtxt, "<Button-1>", self.back_func)
		
	def back_func(self, event):
		self.__del__()
		
	def next(self, event):
		if not self.screen:
			return
		if self.current != len(self.colors)-1:
			self.current += 1
		else:
			self.current = 0
		self.game.canvas.itemconfig(self.personaltxt, text="Personal Edit" if self.current == len(self.colors)-1 else "")
		self.game.canvas.itemconfig(self.preview, fill=self.colors[self.current])
		self.game.canvas.itemconfig(self.pricetxt, text="$"+str(self.prices[self.current]), fill="red" if self.game.coins < self.prices[self.current] and not self.colors[self.current] in self.game.from_json["colors"] else "black")
		self.game.canvas.itemconfig(self.purchease, fill="green" if self.colors[self.current] not in self.game.from_json["colors"] else "gray")
	def previous(self, event):
		if not self.screen:
			return
		if self.current != 0:
			self.current -= 1
		else:
			self.current = len(self.colors)-1
		self.game.canvas.itemconfig(self.personaltxt, text="Personal Edit" if self.current == len(self.colors)-1 else "")
		self.game.canvas.itemconfig(self.preview, fill=self.colors[self.current])
		self.game.canvas.itemconfig(self.pricetxt, text="$"+str(self.prices[self.current]), fill="red" if self.game.coins < self.prices[self.current] and not self.colors[self.current] in self.game.from_json["colors"] else "black")
		self.game.canvas.itemconfig(self.purchease, fill="green" if self.colors[self.current] not in self.game.from_json["colors"] else "gray")
		
	def purchease_func(self, event):
		if not self.screen:
			return
		if self.colors[self.current] in self.game.from_json["colors"]:
			messagebox.showerror("Error", "You already purcheased this color")
			return
			
		if self.game.coins < self.prices[self.current]:
			messagebox.showerror("Error", "You don't have enough coins")
		else:
			if self.current == len(self.colors)-1:
				cl = colorchooser.askcolor()
				if cl[1] == None:
					return
				#messagebox.showinfo("Info", cl)
				self.game.canvas.itemconfig(self.preview, fill=cl[1])
				now = cl[1]
				self.game.coins -= self.prices[self.current]
				self.game.color = now
			else:
			#self.game.cursor.execute("UPDATE data SET color = ?", ("red",))
				self.game.coins -= self.prices[self.current]
				self.game.color = self.colors[self.current]
				now = self.colors[self.current]
			self.save()
			self.game.statistics["skins_owned"] += 1
			messagebox.showinfo("Purchase", "You purcheased color {0}".format(now))
			self.game.canvas.itemconfig(self.purchease, fill="green" if self.colors[self.current] not in self.game.from_json["colors"] else "gray")
			
	def show_selection(self, event):
		self.screen = False
		tk = Toplevel(self.game.tk)
		
		def destroy():
			select()

		tk.protocol("WM_DELETE_WINDOW", destroy)
		v = StringVar(master=tk)
		v.set(self.game.from_json["selected"])
	#	print(v.get())
		rad = []
	#	print(self.game.from_json)
		for color in self.game.from_json["colors"]:
			r = Radiobutton(tk, text=color, variable=v, value=color)
			r.pack(side="left")
			rad.append(r)
			
		def select():
			#print(v.get())
			self.game.selected = v.get()
		#	print("Shop:", self.game.selected)
			self.screen = True
			tk.destroy()
			
		def cancel():
			self.screen = True
			tk.destroy()
			
		b = Button(tk, text="Select", command=select)
		b.pack()
		b2 = Button(tk, text="Cancel", command=cancel)
		b2.pack()
