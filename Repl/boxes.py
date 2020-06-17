from tkinter import *
from tkinter import messagebox
import random, time

class Box: # PRICE 50 Diamonds
	def __init__(self, shop):
		self.shop = shop
		self.gifts = [{"keys":(1,2)}, {"coins":(5,20)}]
	def show(self):
		self.img = PhotoImage(file="../Data/Images/chest.gif", master=self.shop.game.tk)
		self.id_x = self.shop.game.canvas.create_image(20, 400, anchor="nw",  image=self.img, tags="chest")
		self.id_y = self.shop.game.canvas.create_text(20, 480, anchor="nw", text="Costs 50 dm", tags="chest", font="Calibri 9 bold", fill="purple")
		self.id = "chest"
		self.shop.game.canvas.tag_bind(self.id, "<Button-1>", self.open)
	def open(self, event):
		if self.shop.game.diamonds < 50:
			messagebox.showerror("Error", "You don't have enough diamonds")
			return
		else:
			self.shop.game.diamonds -= 50
			self.shop.game.canvas.itemconfig(self.shop.game.diamondstxt, text="Diamonds: {0}".format(self.shop.game.diamonds))
		tk = Toplevel(self.shop.game.tk)
		tk.title("Opening...")
		n = random.randint(1,3)
		done = [0, 0]
		self.shop.game.play_sound("{0}/chest.mp3".format(self.shop.game.soundspath))
		for x in range(n):
			item = random.choice(self.gifts)
			k = list(item.keys())[0]
			n_i = random.randint(item[k][0], item[k][1])
			if k == "coins":
				done[1] += n_i
			elif k == "keys":
				done[0] += n_i
			txt = "{0} x{1}".format(k, n_i)
			l = Label(tk, text=txt).pack()
			tk.update()
			time.sleep(1)
		text = ""
		s = 0
		for i in done:
			text += "{0} x{1} ".format("keys" if s % 2 == 0 else "coins", i)
			s += 1
		l = Label(tk, text="Total: {0}".format(text)).pack()
		
		def okf():
			self.shop.game.coins += done[1]
			self.shop.game.keys += done[0]
		#	print(self.shop.game.keys)
			tk.destroy()
			
		ok = Button(tk, text="OK", command=okf)
		ok.pack()
