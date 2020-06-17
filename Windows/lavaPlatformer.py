from tkinter import *
from tkinter import messagebox
import tkinter.simpledialog as s
import time, sys, random, os, sqlite3, json, threading, requests
import shop, statistics, settings

from soundplayer import SoundPlayer

filept = os.path.abspath(os.listdir()[os.listdir().index("lavaPlatformer.py")])

class Game:
	def __init__(self, st=False, ktc=1):
		self.ktc = ktc
		self.version = 12.0
		self.pathuser = filept.split('\ '[0])[2]
		self.platform_number = 0
		self.ff_time = False
		self.golevels = []
		print("Downloading image content...")
		self.set_asset()
		print("Done")
		self.tk = Tk()
		self.tk.title("lavaPlatformer start-up")
	#	self.tk.geometry("500x500+10+200")
		x = Label(self.tk, text="Welcome on lavaPlatformer!")
		x.pack()
		self.p = PhotoImage(file="C:/Users/{0}/.lavaPlatformer/Data/showupimage.gif".format(self.pathuser))
		self.l = Label(self.tk, image=self.p)
		self.l.pack()
		self.name = s.askstring("Player name", "Enter player name:") if self.ff_time or st else None
		control = self.check_name()
		if not control and not os.path.exists("C:/Users/{0}/.lavaPlatformer/user.txt".format(self.pathuser)):
			messagebox.showerror("Error", "Invalid name, You can only use characters from a-z, A-Z, numbers and underscore. Your name can not exist two times")
			sys.exit()
		x.destroy()
		self.l.destroy()
		self.tk.resizable(0,0)
		self.tk.protocol("WM_DELETE_WINDOW", lambda: self.gameover(closing=True))
		self.tk.title("LavaPlatformer v{0}".format(self.version))
		self.canvas = Canvas(self.tk, width=500, height=500, bg="lightblue")
		self.canvas.pack()
		self.platforms = [] #List of platforms
		self.gameIsRunning = False
		self.color = "black"
		self.selected = self.color
		self.coins = 0
		self.diamonds = 0
		self.keys = 0
		self.lava_dist = 450.0
		self.timetxt = self.canvas.create_text(0,0, anchor="nw", text="Time: {0}".format(round(0-0, 2)), font="Purisa 14 bold", fill="blue")
		self.cointxt = self.canvas.create_text(0,35, anchor="nw", text="Coins: {0}".format(self.coins), font="Purisa 14 bold", fill="yellow")
		self.lavadisttxt = self.canvas.create_text(500,0, anchor="ne", text="Lava Distance: {0}".format(self.lava_dist), font="Purisa 14 bold", fill="red")
		self.diamondstxt = self.canvas.create_text(500,35, anchor="ne", text="Diamonds: {0}".format(self.diamonds), font="Purisa 14 bold", fill="purple")
		self.keystxt = self.canvas.create_text(500, 70, anchor="ne", text="Keys: {0}".format(self.keys), font="Purisa 14 bold", fill="green")
		self.shop = shop.Shop(self, pt="C:/Users/{0}/.lavaPlatformer/".format(self.pathuser))
		self.shop.show_button()
		self.statistics_menu = statistics.Statistics(self)
		self.statistics_menu.show_button()
		self.statistics = {
			"best_time" : 0,
			"platforms_jumped" : 0,
			"times_played" : 0,
			"best_job_level" : 0,
			"best_game_level" : 0,
			"skins_owned" : 1
		}
		self.maxtime = 0.0
	
	def filter_func(self, a):
		if a == 0:
			return True
		else:
			return False
	
	def play_sound(self, soundpath, loop=False):
		def play():
			if loop:
				while True:
					if self.gameIsRunning:
						s = SoundPlayer(soundpath, self)
						s.play()
			else:
				s = SoundPlayer(soundpath, self)
				s.play()
		t = threading.Thread(target=play)
		t.start()
	
	def ask_sounds(self):
		sounds = ["chest", "coin", "gameover", "level", "respawn", "start"]
		if not os.path.isdir("C:/Users/{0}/.lavaPlatformer/Data/Sounds".format(self.pathuser)):
			os.mkdir("C:/Users/{0}/.lavaPlatformer/Data/Sounds".format(self.pathuser))

			for sound in sounds:
				r = requests.get("https://github.com/OrangoMango/LavaPlatformer/raw/master/Data/Sounds/{0}.mp3".format(sound))
				open("C:/Users/{0}/.lavaPlatformer/Data/Sounds/{1}.mp3".format(self.pathuser, sound), "wb").write(r.content)
		self.soundspath = "C:/Users/{0}/.lavaPlatformer/Data/Sounds".format(self.pathuser)
	
	def save_user(self):
		if not os.path.exists("C:/Users/{0}/.lavaPlatformer/user.txt".format(self.pathuser)):
			with open("C:/Users/{0}/.lavaPlatformer/user.txt".format(self.pathuser), "w") as f:
				f.write(self.name)
		else:
			with open("C:/Users/{0}/.lavaPlatformer/user.txt".format(self.pathuser)) as f:
				self.name = f.read().rstrip("\n")
				
	def check_name(self):
		try:
			if self.name in os.listdir("C:/Users/{0}/.lavaPlatformer".format(self.pathuser)):
				return False
		except:
			pass
		if self.name == "" or self.name == None or len(self.name) > 15:
			return False
		l = list(self.name)
		words = "abcdefghijklmnopqrstuvwxyz0123456789_"
		for ch in l:
			if not ch in list(words)+list(words.upper()):
				return False
		return True

	def at_start(self):
		def start(e):
			self.play_sound("{0}/start.mp3".format(self.soundspath))
			self.canvas.delete(txt)
			self.canvas.delete(self.shop.id)
			self.canvas.delete(self.statistics_menu.id)
			self.canvas.delete(self.settings_button.id)
			self.shop.job_button.jobs[0]["Jump on platforms"]["progress"] = 0
			self.shop.job_button.jobs[1]["Go on transparent platforms"]["progress"] = 0
			self.shop.job_button.jobs[2]["Get coins"]["progress"] = 0
			self.gameIsRunning = True
			self.time1 = round(time.time(), 2)
			self.time2 = round(time.time(), 2)
		tap_to_start = '''
		      TAP TO
		      START
		'''
		txt = self.canvas.create_text(-50, 250, anchor="center", text=tap_to_start, font="Calibri 45 bold", fill="gray")
		self.canvas.tag_bind(txt, "<Button-1>", start)
	
	def load_json_statistics(self, save=False):
		if os.path.exists("statistics.json") and not save:
			with open("statistics.json", "r") as f:
				data = json.load(f)
				#print(data)
				self.statistics = data
		else:
			with open("statistics.json", "w") as f:
				json.dump(self.statistics, f, indent=4)
		if save:
			self.statistics["times_played"] += 1
			os.chdir(os.path.abspath(filept+"/.."))
			os.chdir("C:/Users/{0}/.lavaPlatformer/{1}".format(self.pathuser, self.name))
			with open("statistics.json", "w") as f:
				json.dump(self.statistics, f, indent=4)
	
	def save_json_data(self, val=None, ff=False, load=False):
		if load:
			with open("colors.json", "r") as colors_f:
				data = json.load(colors_f)
				self.selected = data["selected"]
				self.from_json = data
			#	print("Main:", self.selected)
			return
		if os.path.exists("colors.json") and ff:
			with open("colors.json", "r") as colors_f:
				data = json.load(colors_f)
				self.from_json = data
				self.color = data["colors"][data["colors"].index(self.color)]
		else:
			os.chdir(os.path.abspath(filept+"/.."))
			os.chdir("C:/Users/{0}/.lavaPlatformer/{1}".format(self.pathuser, self.name))
			with open("colors.json", "w") as colors_f:
				data = {
					"colors" : val,
					"selected" : self.selected
				}
				self.from_json = data
				json.dump(data, colors_f, indent=4)
	
	def set_asset(self):
		user = self.pathuser
		path = ""#.format(user)
		#os.chdir(path)
		if not os.path.isdir("C:/Users/{0}/.lavaPlatformer".format(user)):
			os.mkdir("C:/Users/{0}/.lavaPlatformer".format(user))
			self.ff_time = True
		if not os.path.isdir("C:/Users/{0}/.lavaPlatformer/Data".format(user)):
			os.mkdir("C:/Users/{0}/.lavaPlatformer/Data".format(user))
			r = requests.get("https://github.com/OrangoMango/LavaPlatformer/raw/master/Data/showupimage.gif", allow_redirects=True)
			open("C:/Users/{0}/.lavaPlatformer/Data/showupimage.gif".format(user), "wb").write(r.content)
		#	os.system("cp "+"Data/showupimage.gif "+" C:/Users/{0}/.lavaPlatformer/Data/showupimage.gif".format(user))
		if not os.path.isdir("C:/Users/{0}/.lavaPlatformer/Data/Images".format(user)):
			os.mkdir("C:/Users/{0}/.lavaPlatformer/Data/Images".format(user))
			r = requests.get("https://github.com/OrangoMango/LavaPlatformer/raw/master/Data/Images/chest.gif")
			open("C:/Users/{0}/.lavaPlatformer/Data/Images/chest.gif".format(user), "wb").write(r.content)
			r = requests.get("https://github.com/OrangoMango/LavaPlatformer/raw/master/Data/Images/jobs.gif")
			open("C:/Users/{0}/.lavaPlatformer/Data/Images/jobs.gif".format(user), "wb").write(r.content)
			r = requests.get("https://github.com/OrangoMango/LavaPlatformer/raw/master/Data/Images/settings.gif")
			open("C:/Users/{0}/.lavaPlatformer/Data/Images/settings.gif".format(user), "wb").write(r.content)
			r = requests.get("https://github.com/OrangoMango/LavaPlatformer/raw/master/Data/Images/shop.gif")
			open("C:/Users/{0}/.lavaPlatformer/Data/Images/shop.gif".format(user), "wb").write(r.content)
	
	def setup_directory(self):
		user = self.pathuser
		path = ""#.format(user)
		#os.chdir(path)
		self.save_user()
		if not os.path.exists(path+"C:/Users/{0}/.lavaPlatformer/".format(user)+self.name):
			os.mkdir(path+"C:/Users/{0}/.lavaPlatformer/".format(user)+self.name)
			print("Downloading sounds...")
			self.ask_sounds()
			print("Done")
		self.path4job = path+"C:/Users/{0}/.lavaPlatformer/{1}/".format(user, self.name)
		os.chdir(path+"C:/Users/{0}/.lavaPlatformer/{1}/".format(user, self.name))
		if not os.path.exists("../path.txt"):
			with open("../path.txt", "w") as f:
				f.write(self.soundspath)
		else:
			with open("../path.txt", "r") as f:
				self.soundspath = f.read().rstrip("\n")
		var = False
		if os.path.exists("data.db"):
			var = True
			connection = sqlite3.connect("data.db")
			cursor = connection.cursor()
			sql = "SELECT * FROM data"
			cursor.execute(sql)
			for d in cursor:
				self.coins = int(d[0])
				self.diamonds = int(d[1])
				self.keys = int(d[2])
			self.canvas.itemconfig(self.cointxt, text="Coins: {0}".format(self.coins))
			self.canvas.itemconfig(self.diamondstxt, text="Diamonds: {0}".format(self.diamonds))
			self.canvas.itemconfig(self.keystxt, text="Keys: {0}".format(self.keys))
			connection.close()
			os.remove("data.db")
	#	print("OK")
		self.connection = sqlite3.connect("data.db")
		self.cursor = self.connection.cursor()
		sql = "CREATE TABLE data(coins INTEGER, diamonds INTEGER, keys INTEGER)"
		self.cursor.execute(sql)
		if not var:
			#print("Here")
			self.save_json_data(val=[self.color], ff=True)
		else:
			self.save_json_data(load=True)
		self.load_json_statistics()
		self.shop.add_job()
		self.settings_button = settings.Settings(self)
		self.settings_button.show_button()
	#	self.connection.close()
	
	def mainloop(self):
		self.time1 = time.time()
		self.time2 = time.time()
		ok = True
		while True:
			if self.gameIsRunning:
				try:
					self.time2 = time.time()
					self.canvas.itemconfig(self.timetxt, text="Time: {0}".format(round(self.time2-self.time1, 2)))
					self.canvas.itemconfig(self.cointxt, text="Coins: {0}".format(self.coins))
					self.canvas.itemconfig(self.lavadisttxt, text="Lava Distance: {0}".format(self.lava_dist))
					self.canvas.itemconfig(self.diamondstxt, text="Diamonds: {0}".format(self.diamonds))
					self.canvas.itemconfig(self.keystxt, text="Keys: {0}".format(self.keys))
					self.canvas.tag_raise(self.timetxt)
					self.canvas.tag_raise(self.cointxt)
					self.canvas.tag_raise(self.lavadisttxt)
					self.canvas.tag_raise(self.diamondstxt)
					self.canvas.tag_raise(self.keystxt)
					l.draw()
					p.draw()
					self.tk.update()
				except:
					break
				time.sleep(0.01)
			else:
				if ok:
					self.maxtime = round(self.time2-self.time1, 2)
					ok = False
				try:
					self.tk.update()
				except:
					break
				time.sleep(0.01)
				
	def gameover(self, errortype="Game Over", closing=False):
		ktc = self.ktc
		self.play_sound("{0}/gameover.mp3".format(self.soundspath))
		if not closing:
			messagebox.showerror("Game Over", errortype)
			if errortype == "Lava touched you!" or errortype == "You hit the floor too hard":
				ask = messagebox.askyesno("Respawn", "Do you want to use %s keys to continue?" % ktc)
				if ask:
					if self.keys < ktc:
						messagebox.showerror("Error", "You don't have enough keys")
						ktc = 1
						self.ktc = ktc
					else:
						self.keys -= ktc
						self.play_sound("{0}/respawn.mp3".format(self.soundspath))
						ktc += 1
						self.ktc = ktc
						self.canvas.itemconfig(self.keystxt, text="Keys: {0}".format(self.keys))
						p.damage = 0
						if errortype == "Lava touched you!":
							self.canvas.move(l.id, 0, -350)
						return
				else:
					ktc = 1
					self.ktc = ktc
			else:
				ktc = 1
				self.ktc = ktc
		#print(p.damage)
		self.maxtime = round(self.time2-self.time1, 2)
		sql = "INSERT INTO data VALUES(?, ?, ?)"
		self.cursor.execute(sql, (self.coins, self.diamonds, self.keys))
		self.connection.commit()
		self.connection.close()
		self.save_json_data(val=self.from_json["colors"]+[self.color] if not self.color in self.from_json["colors"] else self.from_json["colors"])
		if self.statistics['best_time'] < self.maxtime:
			self.statistics['best_time'] = self.maxtime
		self.load_json_statistics(True)
		self.shop.job_button.save_progress()
		try:
			self.tk.destroy()
		except:
			pass
		self.gameIsRunning = False
		if not closing:
			main(ktc=ktc, st = True if errortype=="Game must be restarted after creating" else False)
		else:
			sys.exit(0)

class Profile:
	def __init__(self, game):
		self.game = game
		self.tk = Tk()
		self.tk.title("Profiles")
		self.profiles = self.get_profiles()
		self.var = StringVar(master=self.tk)
		#self.var.set("Orango")
		self.var.set(self.getCurrentUser())
		self.rdb = []

		self.profiles_frame = LabelFrame(self.tk, text="Profiles")
		self.profiles_frame.pack()

	def show_interface(self):
		for prf in self.profiles:
			r = Radiobutton(self.profiles_frame, text=prf,  variable=self.var, value=prf)
			r.pack()
			self.rdb.append(r)
		self.ok = Button(self.tk, text="SELECT", command=self.select)
		self.ok.pack()
		self.new = Button(self.tk, text="CREATE", command=self.create)
		self.new.pack()
		self.dele = Button(self.tk, text="DELETE", command=self.delete)
		self.dele.pack()
	def delete(self):
		s = self.var.get()
		if s == self.getCurrentUser():
			messagebox.showerror("Error", "Could not delete current profile", master=self.tk)
			return
	#	for i in os.listdir(self.game.path4job+"../{0}/".format(s)):
		#	os.remove(i)
		os.system("rmdir /s /q "+self.game.path4job+"../{0}/".format(s))
	#	self.game.gameover(closing=True)
		messagebox.showinfo("Info", "Profile deleted", master=self.tk)
		self.tk.destroy()
	def create(self):
		os.remove(self.game.path4job+"../user.txt")
		self.tk.destroy()
		self.game.gameover(errortype="Game must be restarted after creating")
	def getCurrentUser(self):
		with open(self.game.path4job+"../user.txt", "r") as f:
			return f.read()
	def select(self):
		s = self.var.get()
		with open(self.game.path4job+"../user.txt", "w") as f:
			f.write(s)
		messagebox.showinfo("Info", "User {0} selected".format(s), master=self.tk)
		self.tk.destroy()
		self.game.gameover(errortype="Game must be restarted")
	def get_profiles(self):
		data = []
#		print(os.listdir(self.game.path4job+"../"))
		os.chdir(os.path.abspath(filept+"/../"))
		for i in os.listdir(self.game.path4job+"../"):
			if not i.endswith(".txt") and not i == "Data":
				data.append(i)
		return data
			
class Player:
	def __init__(self, game, lava):
		self.lava = lava
		self.on_platform_OS = "computer" #TO SET TO COMPUTER
		self.game = game
		self.id_x = self.game.canvas.create_rectangle(40, 115, 75, 150, fill=self.game.selected, tags="Player")
		self.name = self.game.canvas.create_text(58, 100, anchor="center", text=self.game.name, tags="Player")
		self.id = "Player"
		self.game.tk.bind("<KeyPress>" if self.on_platform_OS == "computer" else "<Motion>", self.move)
		self.x, self.y = 0, 0
		self.damage = 0
		self.level = 1
		self.game.canvas.tag_bind(self.id, "<Button-1>", self.switch)
	def switch(self, event):
		if self.game.gameIsRunning == False:
			#tk = Toplevel(self.game.tk)
			prf = Profile(self.game)
			prf.show_interface()
	def move(self, event):
		if not self.game.gameIsRunning:
			return
		if self.on_platform_OS == "android":
			x, y = event.x, event.y
			k = None
		elif self.on_platform_OS == "computer":
			k = event.char
			x, y = 0, 0
		#print(k)
		pos = self.game.canvas.coords(self.id)
		if  ((x >= 250 and self.on_platform_OS == "android") or (k == "d" and self.on_platform_OS == "computer")) and pos[2] <= 500:
			self.game.canvas.move(self.id, 13 if self.on_platform_OS == "computer" else 5, 0)
		elif ((x < 250 and self.on_platform_OS == "android") or  (k == "a" and self.on_platform_OS == "computer")) and pos[0] >= 0:
			self.game.canvas.move(self.id, -13 if self.on_platform_OS == "computer" else -5, 0)
	def draw(self):
		self.game.canvas.move(self.id, self.x, self.y)
		x = 0
	#	print("length", len(self.game.platforms))
		for platform in self.game.platforms:
		#	print(platform.last, x)
			pl_pos = self.game.canvas.coords(platform.id)
			pos = self.game.canvas.coords(self.id)
			if self.damage >= 80:
				self.game.gameover(errortype="You fell into the void")
			if (((pos[3] >= pl_pos[1] and pos[3] <= pl_pos[3]) \
				 and (pos[2] >= pl_pos[0] and pos[2] <= pl_pos[2]+15)) \
				 or ((pos[0] >= pl_pos[0] and pos[0] <= pl_pos[2]) and (pos[3] >= pl_pos[1] and pos[3] <= pl_pos[3]))):
				if platform.type == "death":
					self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["progress"] += 0.5
					if self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["progress"] == self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["number"]:
						self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["number"] += 2
						self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["reward"] += 5
						self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["level"] += 1
						self.game.diamonds += self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["reward"] - 5
						self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["progress"] = 0
						self.game.play_sound("{0}/level.mp3".format(self.game.soundspath))
						if self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["level"] > self.game.statistics["best_job_level"]:
							self.game.statistics["best_job_level"] = self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["level"]
						if self.game.settings_button.dict["popups"]["value"] == 1 and self.game.settings_button.dict["popups"]["jobs"] == 1:
							messagebox.showinfo("Info", "You passed next job level in \"Go on transparent platforms\" reward is {0} diamonds".format(self.game.shop.job_button.jobs[1]["Go on transparent platforms"]["reward"]-5)) #HERE
						
					self.game.canvas.move(platform.id, 0, -10)
					self.lava.fall = False
					platform.touched = True
					continue
				if self.damage >= 25:
					self.game.gameover(errortype="You hit the floor too hard")
				else:
					self.damage = 0
			#	print(platform.id_number)
				self.lava.fall = True
				if not platform.touched:
					self.game.golevels.append(platform.id_number % 10)
					self.game.golevels = list(filter(self.game.filter_func, self.game.golevels))
					try:
						if int(platform.id_number / 10) >= self.level and self.game.gameIsRunning: #len(self.game.golevels) == self.level:
							self.level += 1
							if self.level-1 > self.game.statistics["best_game_level"]:
								self.game.statistics['best_game_level'] = self.level-1
							if self.game.settings_button.dict["popups"]["value"] == 1 and self.game.settings_button.dict["popups"]["levels"] == 1:
								messagebox.showinfo("lavaPlatformer", "You passed level {0}".format(self.level-1)) #HERE
					except Exception as e:
						print("Error", e)
				#	print(self.game.golevels)
					self.game.statistics["platforms_jumped"] += 1
					self.game.shop.job_button.jobs[0]["Jump on platforms"]["progress"] += 1
					if self.game.shop.job_button.jobs[0]["Jump on platforms"]["progress"] == self.game.shop.job_button.jobs[0]["Jump on platforms"]["number"]:
						self.game.shop.job_button.jobs[0]["Jump on platforms"]["number"] += 5
						self.game.shop.job_button.jobs[0]["Jump on platforms"]["reward"] += 4
						self.game.shop.job_button.jobs[0]["Jump on platforms"]["level"] += 1
						self.game.diamonds += self.game.shop.job_button.jobs[0]["Jump on platforms"]["reward"] - 4
						self.game.shop.job_button.jobs[0]["Jump on platforms"]["progress"] = 0
						self.game.play_sound("{0}/level.mp3".format(self.game.soundspath))
						if self.game.shop.job_button.jobs[0]["Jump on platforms"]["level"] > self.game.statistics["best_job_level"]:
							self.game.statistics["best_job_level"] = self.game.shop.job_button.jobs[0]["Jump on platforms"]["level"]
						if self.game.settings_button.dict["popups"]["value"] == 1 and self.game.settings_button.dict["popups"]["jobs"] == 1:
							messagebox.showinfo("Info", "You passed next job level in \"Jump on platforms\" reward is {0} diamonds".format(self.game.shop.job_button.jobs[0]["Jump on platforms"]["reward"]-4)) #HERE
					for x in range(2):
						if platform.next:
							last = None
							for plat in self.game.platforms:
								if plat.last:
									last = plat
									plat.last = False
									break
							c_p_pos = self.game.canvas.coords(last.id)
							nx, ny, nx1, ny1 = c_p_pos
							def check(v1, v2):
								if v1 <= 0:
										#print("IN")
									return 200, 400
								elif v2 >= 500:
										#print("Out")
									return 0,300
								else:
									return v1, v2
								
							val1, val2 = check(nx-80, nx1+80)
							x3 = random.randint(val1, val2)
							n = random.random()
							if n > 0.6:
								x = "coin"
							else:
								x = "normal"
							if len(self.game.platforms) > 17: #Next difficulty level
								dt = random.random()
								if x == "coin":
									x = "coin"
								elif dt < 0.3 and last.type != "death":
									x = "death"
								else:
									x = "normal"
							pl = Platform(self.game, x3, ny+100, 100, 15, last=True, num=self.game.platform_number, type=x, text="## LEVEL COMPLETED ##")
							self.game.platform_number += 1
							self.game.platforms.append(pl)
						
						platform.touched = True
				if platform.type == "coin" and not platform.on_coin:
					self.game.play_sound("{0}/coin.mp3".format(self.game.soundspath))
					self.game.shop.job_button.jobs[2]["Get coins"]["progress"] += 1
					if self.game.shop.job_button.jobs[2]["Get coins"]["progress"] == self.game.shop.job_button.jobs[2]["Get coins"]["number"]:
						self.game.shop.job_button.jobs[2]["Get coins"]["number"] += 5
						self.game.shop.job_button.jobs[2]["Get coins"]["reward"] += 3
						self.game.shop.job_button.jobs[2]["Get coins"]["level"] += 1
						self.game.diamonds += self.game.shop.job_button.jobs[2]["Get coins"]["reward"] - 4
						self.game.shop.job_button.jobs[2]["Get coins"]["progress"] = 0
						self.game.play_sound("{0}/level.mp3".format(self.game.soundspath))
						if self.game.settings_button.dict["popups"]["value"] == 1 and self.game.settings_button.dict["popups"]["jobs"] == 1:
							messagebox.showinfo("Info", "You passed next job level in \"Get Coins\" reward is {0} diamonds".format(self.game.shop.job_button.jobs[2]["Get coins"]["reward"]-4)) #HERE
					self.game.coins += 1
					platform.on_coin = True
					platform.reset_type()
				self.y = 0		
				break
			else:
				self.game.canvas.move(platform.id, 0, -10)
				self.lava.fall = False
			x += 1
		self.damage += 1
		pos = self.game.canvas.coords(self.id)
	#	if pos[3] >= 500:
	#		self.game.gameIsRunning = False
		lava_pos = self.game.canvas.coords(self.lava.id)
		self.game.lava_dist = pos[1]-lava_pos[3]
		if self.game.lava_dist <= 0:
			self.game.gameover(errortype="Lava touched you!")
	#	print(len(self.game.platforms))
		#print(self.game.lava_dist)

			
class Platform:
	def __init__(self, game, x, y, w, h, last=False, next=True, type="normal", num=0, text=None):
		self.game = game
		self.id_number = num
		self.last = last
		if not text is None:
			self.center_text = ""
		if not text == "## LEVEL COMPLETED ##":
			self.center_text = text
		elif text == "## LEVEL COMPLETED ##" and self.id_number % 10 == 0:
			self.center_text = "LEVEL {0} END".format(self.id_number // 10)
		else:
			self.center_text = ""#self.id_number
		self.next = next
		self.type = type
		self.on_coin = False
		self.touched = False
		self.x_d, self.y_d, self.w_d, self.h_d = x, y, w, h
		self.transform(self.type)
		self.add_level_line()
		self.set_platform_text()
	def set_platform_text(self):
		centerx, centery = self.x_d+self.w_d/2, self.y_d+self.h_d/2
		self.centertxt = self.game.canvas.create_text(centerx, centery, anchor="center", text=self.center_text, tags=self.id)
	def add_level_line(self):
		x, y, x1, y1 = self.game.canvas.coords(self.id)
		ly = y+((y1-y)/2)
		if self.id_number % 10 == 0:
			self.id_line = self.game.canvas.create_line(0, ly, x, ly, tags=self.id, dash=(4,2))
			self.id_line2 = self.game.canvas.create_line(x1, ly, 500, ly, tags=self.id, dash=(4,2))
	def transform(self, type):
		x, y, w, h = self.x_d, self.y_d, self.w_d, self.h_d
		centerx, centery = x+w/2, y+h/2
		
		if type == "normal":
			self.id_x = self.game.canvas.create_rectangle(x, y, x+w, y+h, tags="normal_platform{0}".format(self.id_number), fill="red")
			self.id = "normal_platform{0}".format(self.id_number)
			self.centertxt = self.game.canvas.create_text(centerx, centery, anchor="center", text=self.center_text, tags=self.id)
		elif type == "coin":
			self.id_x = self.game.canvas.create_rectangle(x, y, x+w, y+h, fill="red", tags="coin_platform{0}".format(self.id_number))
			self.coin_id = self.game.canvas.create_oval(x+(w/2)-10, y-30, x+(w/2)-10+20, y-30+20, tags="coin_platform{0}".format(self.id_number), fill="yellow")
			self.id = "coin_platform{0}".format(self.id_number)
			self.centertxt = self.game.canvas.create_text(centerx, centery, anchor="center", text=self.center_text, tags=self.id)
			
		elif type == "death":
			self.id_x = self.game.canvas.create_rectangle(x, y, x+w, y+h, fill="gray80", tags="death_platform{0}".format(self.id_number))
			self.id = "death_platform{0}".format(self.id_number)
			self.centertxt = self.game.canvas.create_text(centerx, centery, anchor="center", text=self.center_text, tags=self.id)

	def reset_type(self):
		x, y, x1, y1 = self.game.canvas.coords(self.id_x)
		centerx, centery = x+(x1-x)/2, y+(y1-y)/2
		self.game.canvas.delete(self.id)
		self.id_x = self.game.canvas.create_rectangle(x, y, x1, y1, fill="red", tags="normal_platform{0}".format(self.id_number))
		self.id = "normal_platform{0}".format(self.id_number)
		self.centertxt = self.game.canvas.create_text(centerx, centery, anchor="center", text=self.center_text, tags=self.id)
		
class Lava:
	def __init__(self, game):
		self.game = game
		self.id = self.game.canvas.create_rectangle(0, 0, 500, 500, fill="orange")
		self.game.canvas.move(self.id, 0, -850)
		self.fall = True
	def draw(self):
		if self.fall:
			self.game.canvas.move(self.id, 0, 2)
		else:
			self.game.canvas.move(self.id, 0, -7)
		pos = self.game.canvas.coords(self.id)
		if pos[3] >= 500:
			self.game.gameover()
		pass

def main(ktc=1, st=False):
	global g, l, p, pl, pl2, pl3
	g = Game(st=st, ktc=ktc)
	g.setup_directory()
	l = Lava(g)
	p = Player(g, l)
	pl = Platform(g, 20, 150, 100, 15, num=g.platform_number, text="START")
	pl.touched = True
	g.platform_number += 1
	pl2 = Platform(g, 140, 250, 100, 15, type="coin", num=g.platform_number)
	g.platform_number += 1
	pl3 = Platform(g, 280, 350, 100, 15, last=True, num=g.platform_number)
	g.platform_number += 1
	g.platforms.append(pl)
	g.platforms.append(pl2)
	g.platforms.append(pl3)
	g.at_start()
	g.player_shop = p
	g.mainloop()
	
if __name__ == '__main__':
	main()
