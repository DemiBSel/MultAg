import numpy as np

class Environment:
	def __init__(self,x,y):
		self.width = x
		self.height = y
		self.observers=[]
		self.grid = np.zeros((x,y),dtype='object')

	def subscribe(self,observer):
		self.observers.append(observer)
		
	def notify_all(self,x,y,c):
		for observer in self.observers :
			observer.alert(x,y,c)
		
	def get_sense(self,x,y,r):
		ret=[]
		max_back = x-r
		max_for = x+r
		max_top = y-r
		max_bot = y+r
		
		
		it=max_back
		jt=max_top
		while(it<=max_for):
			jt=max_top
			while(jt<=max_bot):
				if(it<=0 or it>=self.width or jt<=0 or jt>=self.height):
					#detect boundaries
					ret.append((it-x,jt-y,0)) ##perception
				else:
					#detect obstacles
					if (self.grid[it][jt] != 0 ):
						ret.append((it-x,jt-y,self.grid[it][jt])) ##perception
				jt=jt+1
			it=it+1
	
		return ret
		
	def get_pos(self,x,y):
		return(self.grid[x][y])
	
	def place(self,id,x,y):
		self.grid[x][y]=id
		self.notify_all(x,y,id)
	
	def move_vect(self,x,y,mx,my,id,trace=True):
		if(x+mx>0 and y+my>0 and x+mx<self.width and y+my<self.height):
			self.grid[x+mx][y+my]=id
			##draw trace of the move
			if(trace):
				i=x+mx
				j=y+my
				while(i!=x and j!=y):
					if(i>x):
						i=i-1
					else:
						if(i<x):
							i=i+1
					if(j>y):
						j=j-1
					else:
						if(j<y):
							j=j+1
					self.grid[i][j]=id
					
			self.notify_all(x+mx,y+my,id)
			return True
		else:
			print("refused "+str((x,y))+" + "+str((mx,my))+" for "+self.grid[x][y],flush=True)
			return False
