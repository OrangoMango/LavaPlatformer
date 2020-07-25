from tkinter import *
import tkinter.ttk as t
import os, json

filept = os.path.abspath(os.listdir()[0])

class Job:
	def __init__(self, shop):
		self.shop = shop
		self.jobs = [{"Jump on platforms":{"level":1, "number":5, "text":"Jump on {0} platforms\nin one time - dm {1}", "progress":0, "reward":10}},
                             {"Go on transparent platforms":{"level":1, "number":2, "text":"Go throw {0} transparent platforms\nin one time - dm {1}","progress":0, "reward":20}},
                             {"Get coins":{"level":1, "number":5, "text":"Get {0} coins\nin one time - dm {1}", "progress":0, "reward":3}}]
		self.widgets=[[None, None, None], [None, None, None], [None, None, None]]
	#	self.save_progress(True)
		try:
			self.load_progress()
		except:
			pass
	#	print(self.jobs)
	def show_button(self):
		self.image = PhotoImage(file="../Data/Images/jobs.gif", master=self.shop.game.tk)
		self.id_x = self.shop.game.canvas.create_image(410, 410, image=self.image, anchor="nw", tags="job_button")
	#	self.br = self.shop.game.canvas.create_text(450, 450, text="J", tags="job_button", font="Calibri 19 bold")
		self.id_y = None
		self.id = "job_button"
		self.shop.game.canvas.tag_bind(self.id, "<Button-1>", self.onclick)
	def onclick(self, event):
		self.shop.screen = False
		tk = Toplevel(self.shop.game.tk)
		tk.title("Jobs")
		def close():
			self.save_progress()
			self.shop.screen = True
			tk.destroy()
		tk.protocol("WM_DELETE_WINDOW", close)
		self.show_jobs(tk)
	def show_jobs(self, tk):
		counter = 0
		for i in self.jobs:
			for k in self.jobs[counter].keys():
				self.widgets[counter][0] = LabelFrame(tk, text=k+"- {0}".format(self.jobs[counter][k]["level"]), font="Calibri 12 bold")
				self.widgets[counter][0].pack()
				l = Label(self.widgets[counter][0], text=self.jobs[counter][k]["text"].format(self.jobs[counter][k]["number"], self.jobs[counter][k]["reward"])).pack()	
				self.widgets[counter][1] = t.Progressbar(self.widgets[counter][0], value=100/self.jobs[counter][k]["number"]*self.jobs[counter][k]["progress"])#, from_=0, to=self.jobs[k]["number"])
				self.widgets[counter][1].pack()
				self.widgets[counter][2] = Label(self.widgets[counter][0], text="{0}/{1}".format(int(self.jobs[counter][k]["progress"]), self.jobs[counter][k]["number"]))
				self.widgets[counter][2].pack()
			counter += 1
					
	def load_progress(self):
		os.chdir(os.path.abspath(filept+"/../"))
		with open(self.shop.game.path4job+"jobs.json", "r") as f:
			self.jobs = json.load(f)
		'''	dt = []
			for k in self.jobs.keys():
				dt.append({k:self.jobs[k]})
			print(dt)
			self.jobs = dt'''

	def save_progress(self):
#		print(self.shop.game.path4job)
		print(os.path.exists(self.shop.game.path4job+"jobs.json"))
		print(self.shop.game.path4job+"jobs.json")
		os.chdir(os.path.abspath(filept+"/../"))
		if not os.path.exists(self.shop.game.path4job+"jobs.json"):
			with open(self.shop.game.path4job+"jobs.json", "w") as f:
				data = {}
				x = 0
				for i in self.jobs:
					for k in i.keys():
						data[k] = {"level":self.jobs[x][k]["level"],"number":self.jobs[x][k]["number"],"text":self.jobs[x][k]["text"], "progress":self.jobs[x][k]["progress"], "reward":self.jobs[x][k]["reward"]}
					x += 1
			#	print("data",data)
				dt = []
				for k in data.keys():
					dt.append({k:data[k]})
				#print(dt)
				json.dump(dt, f, indent=4)
		else:
			with open(self.shop.game.path4job+"jobs.json", "w") as f:
				json.dump(self.jobs, f, indent=4)
