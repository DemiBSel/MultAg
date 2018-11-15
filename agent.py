from environment import Environment
from frame import Frame
import random
from threading import Thread
import time

class Agent(Thread):
	def __init__(self,env,id):
		Thread.__init__(self)
		
		self.sense_distance = 15
		self.env = env
		self.position=(random.randint(0,self.env.width-1),random.randint(0,self.env.height-1))
		self.id = id
		
		self.isRunning=False
		self.init_movements()
		self.init_position()
	
	def init_movements(self):
		self.movements=[]
		range=3
		i=-1*range
		while(i<=range):
			j=-1*range
			while(j<=range):				
				self.movements.append((j,i))
				j=j+1
			i=i+1
	
	def init_position(self):
		if(self.env.get_pos(self.position[0],self.position[1]) != 0):
			rec = self.env.get_sense(self.position[0],self.position[1],self.sense_distance)
			rec = self.move(rec,False)
			self.position=(self.position[0]+rec[0],self.position[1]+rec[1])
		self.env.place(self.id,self.position[0],self.position[1])
		
	def move(self,rec,do):
		pos = self.movements.copy()
		for sense in rec :
			
		
			(x,y)=(sense[0],sense[1])
			if((x,y) in pos and self.avoid(sense)):
				pos.remove((x,y))
		if(len(pos)>0):
			mov = int(random.randint(0,len(pos)-1))
			if(do):
				if(self.env.move_vect(self.position[0],self.position[1],pos[mov][0],pos[mov][1])):
					self.position=(self.position[0]+pos[mov][0],self.position[1]+pos[mov][1])
		else:
			print(self.id+" could not move")
			self.isRunning=False
			
		return pos[mov]
		
	def avoid(self,sense):
		return(sense[2]==0 or sense[2]!=self.id or sense[2]==self.id)
	
	
	
	def run(self):
		self.isRunning=True
		while(self.isRunning):
			self.move(self.env.get_sense(self.position[0],self.position[1],self.sense_distance),True)
			#time.sleep(1)


			
env = Environment(800,600)
frame = Frame(env)
i=0
while(i<10):
	ag=Agent(env,"ag"+str(i))
	ag.start()
	i = i+1