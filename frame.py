from tkinter import *
from threading import Thread, BoundedSemaphore
import random

DOT_SCALE = 1
##Semaphores
paint_sema = BoundedSemaphore(value=1)
queue_sema = BoundedSemaphore(value=1)

class ThDisplayer(Thread):
	def __init__(self,frame):
		Thread.__init__(self)
		self.fr=frame
		self.colors = {}
		self.heads = {}
	
	def setColor(self,char):
		"""
		r="%03x" % random.randint(0x888,0xDDD)
		g="%03x" % random.randint(0x444,0x666)
		b="%03x" % random.randint(0x555,0xCCC)	
		"""	
		r="%03x" % random.randint(0x444,0x555)
		g="%03x" % random.randint(0x444,0xDDD)
		b="%03x" % random.randint(0x555,0xCCC)
		self.colors[char]="#"+str(r)+str(g)+str(b)
	
	def paint_queue(self,queue):
		if(hasattr(self.fr,'canvas')):
			for t in queue:
				ofX=t[0]*DOT_SCALE/self.fr.width
				ofY=t[1]*DOT_SCALE/self.fr.height
				posX=(self.fr.width*ofX)
				posY=(self.fr.height*ofY)
				if(t[2] not in self.colors):
					self.setColor(t[2])
					txt = self.fr.canvas.create_text(posX,posY,text=t[2],fill=self.colors[t[2]])
					if(t[2] not in self.heads):
						self.heads[t[2]]={'ref' : txt, 'x' : t[0], 'y' : t[1]}
				if(t[2] in self.colors and t[2] in self.heads):
					self.fr.canvas.create_rectangle(posX-DOT_SCALE/2,posY-DOT_SCALE/2,posX+DOT_SCALE/2,posY+DOT_SCALE/2,fill=self.colors[t[2]],outline=self.colors[t[2]])
					head = self.heads[t[2]]
					(x,y) = (head['x'],head['y'])
					self.fr.canvas.move(head['ref'],t[0]-x,t[1]-y)
					self.fr.canvas.tag_raise(head['ref'])
					head['x']=t[0]
					head['y']=t[1]
	
	def run(self):
		global DOT_SCALE
		master = Tk()
		self.fr.width = self.fr.env.width
		self.fr.height = self.fr.env.height
		self.fr.canvas = Canvas(master,width=self.fr.width*DOT_SCALE,height=self.fr.height*DOT_SCALE)
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

		
