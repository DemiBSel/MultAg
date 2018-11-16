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
mov_sema = BoundedSemaphore(value=1)
count_sema = Lock()
release_lock = Event()

class Agent(Thread):
	def __init__(self,env,id):
		Thread.__init__(self)
		self.range = 2
		self.sense_distance = self.range
		self.env = env
		self.position=(random.randint(1,self.env.width-1),random.randint(1,self.env.height-1))
		self.id = id
		
		self.isRunning=False
		self.init_movements()
		self.init_position()
	
	def init_movements(self):
		self.movements=[]
		i=-1*self.range
		while(i<=self.range):
			j=-1*self.range
			while(j<=self.range):				
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
				if(self.env.move_vect(self.position[0],self.position[1],pos[mov][0],pos[mov][1],self.id)):
					self.position=(self.position[0]+pos[mov][0],self.position[1]+pos[mov][1])
					
		else:
			self.die()
			return 0		
		return pos[mov]
	
	def die(self):
		global NB_AGENTS
		print(self.id+" died")
		NB_AGENTS = NB_AGENTS - 1
		print(str(NB_AGENTS)+" remaining",flush=True)
		self.isRunning=False
		
				
	def avoid(self,sense):
		return(sense[2]==0 or sense[2]!=self.id or sense[2]==self.id)
	
	def loop_control(self):
		global LOCKED_COUNT
		global NB_AGENTS
		if(NB_AGENTS>1):
			count_sema.acquire()
			LOCKED_COUNT = LOCKED_COUNT + 1
			if (LOCKED_COUNT / NB_AGENTS) >= 0.5 :
					release_lock.set()
					time.sleep(0.1)
					release_lock.clear()
					LOCKED_COUNT=0	
			count_sema.release()
			release_lock.wait()
		else:
			release_lock.set()
			time.sleep(0.1)
			release_lock.clear()
	
	def run(self):
		global AGENTS_COUNT		
		AGENTS_COUNT=AGENTS_COUNT+1
		
		self.isRunning=True
		while(self.isRunning):
			if(self.isRunning):
				self.move(self.env.get_sense(self.position[0],self.position[1],self.sense_distance),True)
			self.loop_control()

			
class ColoriAgent(Agent):
	def __init__(self,env,id):
		Agent.__init__(self,env,id)
		self.previous_move=(0,1)

	def init_movements(self):
		self.movements=[]
		i=-1*self.range
		while(i<=self.range):
			self.movements.append((0,i))
			i=i+1
		self.movements.append((1,0))
		self.movements.append((-1,0))
	
	def move(self,rec,do=True):
		
		mov_sema.acquire()
		pos=self.process_sense(rec)
		mov_sema.release()
		mov=(0,0)
		if(len(pos)>0):
			for val in pos:
					if(val[1]>0):
						mov=val
						break
					if(val[1]<0):
						mov=val
						break
					else:
						mov=val
			if(do):
				mov_sema.acquire()
				if(self.env.move_vect(self.position[0],self.position[1],mov[0],mov[1],self.id)):
					self.previous_move=mov
					self.position=(self.position[0]+mov[0],self.position[1]+mov[1])	
				mov_sema.release()
		else:	
			self.die()
			return 0
		return mov
		
		
env = Environment(80,60)
frame = Frame(env)
i=0
while(i<NB_AGENTS):

	if(i%2 == 0):
		ag=Agent(env,"ag"+str(i))
	else:
		ag=ColoriAgent(env,"cag"+str(i))
	ag.start()
	i = i+1
