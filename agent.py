from environment import Environment
from frame import Frame
import random
from threading import Thread, BoundedSemaphore, Lock, Event
import time

NB_AGENTS = 15
AGENTS_COUNT = 0
LOCKED_COUNT = 0


##Semaphores
env_sema = BoundedSemaphore(value=NB_AGENTS)
count_sema = Lock()
release_lock = Event()

class Agent(Thread):
	def __init__(self,env,id):
		Thread.__init__(self)
		self.sense_distance = 3
		self.env = env
		self.position=(random.randint(0,self.env.width-1),random.randint(0,self.env.height-1))
		self.id = id
		
		self.isRunning=False
		self.init_movements()
		self.init_position()
	
	def init_movements(self):
		self.movements=[]
		range=2
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
	
	def process_sense(self,rec):
		pos = self.movements.copy()
		for sense in rec :		
			(x,y)=(sense[0],sense[1])
			if((x,y) in pos and self.avoid(sense)):
				pos.remove((x,y))
		return pos
		
	def move(self,rec,do):
		pos = self.process_sense(rec)
		if(len(pos)>0):
			mov = int(random.randint(0,len(pos)-1))
			
			if(do):
				if(self.env.move_vect(self.position[0],self.position[1],pos[mov][0],pos[mov][1])):
					self.position=(self.position[0]+pos[mov][0],self.position[1]+pos[mov][1])			
		else:
			self.die()
			return 0		
		return pos[mov]
	
	def die(self):
		global NB_AGENTS
		print(self.id+" could not move")
		NB_AGENTS = NB_AGENTS - 1
		self.isRunning=False
				
	def avoid(self,sense):
		return(sense[2]==0 or sense[2]!=self.id or sense[2]==self.id)
	
	def loop_control(self):
		global LOCKED_COUNT
		global NB_AGENTS
		count_sema.acquire()
		LOCKED_COUNT = LOCKED_COUNT + 1
		if(LOCKED_COUNT==NB_AGENTS-1):
				release_lock.set()
				time.sleep(0.1)
				release_lock.clear()
				LOCKED_COUNT=0	
		count_sema.release()
		release_lock.wait()
	
	def run(self):
		global AGENTS_COUNT		
		AGENTS_COUNT=AGENTS_COUNT+1
		
		self.isRunning=True
		while(self.isRunning):
			self.move(self.env.get_sense(self.position[0],self.position[1],self.sense_distance),True)
			self.loop_control()

			



			
env = Environment(800,600)
frame = Frame(env)
i=0
while(i<NB_AGENTS):
	ag=Agent(env,"ag"+str(i))
	ag.start()
	i = i+1
