from tkinter import *
from threading import Thread, BoundedSemaphore
import random

##Semaphores
paint_sema = BoundedSemaphore(value=1)
queue_sema = BoundedSemaphore(value=1)

class ThDisplayer(Thread):
	def __init__(self,frame):
		Thread.__init__(self)
		self.fr=frame
		self.colors = {}
	
	def setColor(self,char):
		"""
		r="%03x" % random.randint(0x555,0x888)
		g="%03x" % random.randint(0x444,0x999)
		b="%03x" % random.randint(0x555,0xCCC)
		"""
		r="%03x" % random.randint(0x888,0xDDD)
		g="%03x" % random.randint(0x444,0x666)
		b="%03x" % random.randint(0x555,0xCCC)		
		self.colors[char]="#"+str(r)+str(g)+str(b)
	
	def paint_queue(self,queue):
		if(hasattr(self.fr,'canvas')):
			for t in queue:
				if(t[2] not in self.colors):
					self.setColor(t[2])
					self.fr.canvas.create_text(t[0],t[1],text=t[2])
				if(t[2] in self.colors):
					size=1
					self.fr.canvas.create_rectangle(t[0]-size,t[1]-size,t[0]+size,t[1]+size,fill=self.colors[t[2]],outline=self.colors[t[2]])
				
	
	def run(self):
		master = Tk()
		self.fr.width = self.fr.env.width
		self.fr.height = self.fr.env.height
		self.fr.canvas = Canvas(master,width=self.fr.width,height=self.fr.height)
		self.fr.canvas.pack()
		mainloop()

class Frame(Thread):
	def __init__(self,env):
		Thread.__init__(self)
		self.env = env
		self.disp=ThDisplayer(self)
		self.env.subscribe(self)
		self.disp.start()
		self.queue=[]
		
	def alert(self,x,y,c):
		queue_sema.acquire()
		self.queue.append((x,y,""+c))
		queue_sema.release()
		if(len(self.queue)>10):
			self.paint_queue()
		
		

	def paint_queue(self):
		paint_sema.acquire()
		if(not self.isAlive() and len(self.queue)>10):
			self.start()
			#self.join()
		paint_sema.release()
		
	def run(self):
		queue_sema.acquire()
		quecpy = self.queue.copy()
		self.disp.paint_queue(quecpy)
		self.queue=[]
		queue_sema.release()
		Thread.__init__(self)

		