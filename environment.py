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
		##move to top left corner
		(i,j)=(x,y)
		while(i>max_back and i>=0):
			i=i-1
		while(j>max_top and j>=0 ):
			j=j-1

		##show empty env before
		ic = i
		jc = j
		while(ic>max_back):
			jc=j
			while(jc>max_top):
				ret.append((ic-x,jc-y,0)) ##perception
				jc=jc-1
			ic=ic-1
		
		
		jst=j
		
		##and move to bottom right corner
		while(i<=max_for and i<self.width):
			j=jst
			while(j<=max_bot and j<self.height):
				if (self.grid[i][j] != 0 ):
					ret.append((i-x,j-y,self.grid[i][j])) ##perception
				j=j+1				
			i=i+1
		i=i-1
		j=j-1
		#empty env after
		while(i<=max_for):
			j=jst
			while(j<=max_bot):
				ret.append((i-x,y-j,0)) ##perception
				j=j+1				
			i=i+1
		return ret
		
	def get_pos(self,x,y):
		return(self.grid[x][y])
	
	def place(self,id,x,y):
		self.grid[x][y]=id
		print(self.grid[x][y],x,y)
		self.notify_all(x,y,id)
	
	def move_vect(self,x,y,mx,my,trace=True):
		if(x+mx>0 and y+my>0 and x+mx<self.width and y+my<self.height):
			id=self.grid[x][y]
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
					self.notify_all(i,j,id)
			self.notify_all(x+mx,y+my,id)
			return True
		else:
			return False
