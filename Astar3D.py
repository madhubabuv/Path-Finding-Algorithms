# A-star Algorithm
# Madhu Babu.V
# 13-12-2015

import math

map_size,f_size,c_size,length=125,0,1,5
print "Think of 5 X 5 X 5 cube and give start and goal nodes"
start=input("enter the Starting Node   ")
goal=input('Enter the goal node  ')
cur_location=0
prev_node=0
tmp2=[]
f_list=[]
c_list=[]
top=[0]
bottom=[]
right=[]
left=[0]
for i in range(1,length):
	top.append(i)
	left.append(i*(length))
	right.append(i*(length)-1)
for j in range(max(left),map_size):
	bottom.append(j)
right.append(map_size-1)


#print top,left,right,bottom

def dist(start,goal):
	x1=int(start/length)
	x2=int(goal/length)
	y1=int(start%length)
	y2=int(goal%length)
	z1=int(start/(5**2))
	z2=int(goal/(5**2))	
	if z1>0 :
		x1-=z1*length
	if z2>0:
		x2-=z2*length
	disp=math.sqrt((x2-x1)**2+(y2-y1)**2+(z1-z2)**2)
	return round(disp,3)



def init():
	global f_list,c_list
	for i in range(map_size):
		f_list.append([])
		c_list.append([])
		for j in range(4):
			f_list[i].append(0.0)
			c_list[i].append(-1.0)
	cur_location=start
	#print f_list
	f_list[0][0]=cur_location
	f_list[0][1]=0.0
	f_list[0][2]=0.0
	f_list[0][3]=dist(cur_location,goal)
def grid(node):
	prev_node=0
	x1=int(start/length)
	x2=int(goal/length)
	y1=int(start%length)
	y2=int(goal%length)
	
		
	if node< 0 or node > map_size:
		return 0
	else:
		return 1

def check_for_node(node,bool):
	
	if bool==True:		
		for i in range(len(f_list)):		
			if c_list[i][0]==node or f_list[i][0]==node:
				return False
			else:
				return True
	else:
		for i in range(len(c_list)):
			if c_list[i][0]==node:
				return False
			else:
				return True
def remove_node():
	global f_size
	
	del f_list[0]
	
	f_size-=1
def sort_list():
	for i in range(1,f_size+1):
		j=i
		while(j>0 and f_list[j-1][3] > f_list[j][3]):
			f_list[j-1],f_list[j]=f_list[j],f_list[j-1]
			j-=1

def add_child(node):
	global f_size
	k=node-(length+1)
	tmp=[]

	for j in range(3):
		for i in range(3):
			tmp.append(k)
			k+=1
		k+=2
	for i in range(len(tmp)):
		if (tmp[i]+25 < 125):
			tmp.append(tmp[i]+25)
		if tmp[i]-25>0:
			tmp.append(tmp[i]-25) 
	tmp.sort()
	for i in range(len(tmp)):	
		if (grid(k)):
			if (check_for_node(k,True)):
				f_list[f_size+1][0]=tmp[i]
				f_list[f_size+1][1]=node
				f_list[f_size+1][2]=c_size
				f_list[f_size+1][3]=dist(tmp[i],goal)
				f_size+=1	
	sort_list()

def path():
	
	global cur_location,c_size

	node=f_list[0][0]
	
	if(node==None):
		return 0
	else:
		if node==goal:
			for i in range(4):
				c_list[c_size][i]=f_list[0][i]
			cur_location=goal
			return cur_location

		else:
			if(check_for_node(node,False)):
				for i in range(4):
					c_list[c_size][i]=f_list[0][i]
			cur_location==c_list[c_size][0]
			c_size+=1
			
			remove_node()
			add_child(node)
			#print f_list
			return cur_location
def trace_back():
	global tmp2
	tmp=[]
	count=0
	for i in range(c_size+1):
		tmp2.append(c_list[i])
	for i in range(len(tmp2)):
	 	parent=tmp2[i][1]
		for j in range(len(tmp2)):
			if (tmp2[j][0]>0 and tmp2[j][0]==parent):
				tmp.append(tmp2[j][0])
	tmp.append(tmp2[-1][0])
	print tmp

def go():
	init()
	while cur_location!=goal:
		path()
	trace_back()
go()
print tmp2
