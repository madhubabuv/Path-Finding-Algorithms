import numpy as np
import cv2
import time
from random import randint
gamma=0.8
iterate=250
actions=8
cur_node=0


Q=[]
top=[0]
bottom=[]
right=[]
left=[0]	
pose=[]
count=0
path_cost=[0,10,0,10,0,10,0,10]	
img1=cv2.imread('images/example.jpg',-1)
img=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
img = cv2.medianBlur(img1,5)
frame = cv2.Canny(img,100,200)
kernel_d= np.ones((3,3),np.uint8)
edges = cv2.dilate(frame,kernel_d,iterations = 5)
height, width = img.shape[:2]
comp_h=int(width/43)+1
comp_v=int(height/43)+1
nodes=(((height/43)+1)*((width/43)+1))
print nodes,comp_h,comp_v
print "Conside a gird of",comp_h,"X",comp_v,"and Give Start and Goal "
node=input("enter the staring node\t")
goal=input('enter the goal\t')
print 'calculating the path...'
# Draw a blue line with thickness of 1 px
for i in range(0,height,43):
	cv2.line(img1,(0,i),(width,i),(255,0,0),1)
for j in range(0,width,43):
	cv2.line(img1,(j,0),(j,height),(255,0,0),1)
for k in range (0,height,43):
	for l in range(0,width,43):
		pose.append([])
		pose[count].append(l)
		pose[count].append(k)
		count+=1
		#cv2.circle(img,(l,k), 4, (0,0,255), -1)	
for i in xrange(nodes+1):
	Q.append([])
	for j in range(0,actions):
		Q[i].append(0.0)

if comp_h > comp_v:
	go=comp_h
else :
	go=comp_v
for i in range(1,comp_h):
	top.append(i)
for i in range(1,go):
	left.append(i*(comp_h))
	right.append(i*(comp_h)-1)
for j in range(max(left),nodes):
	bottom.append(j)
right.append(nodes-1)

def possible_node(state,action):
	if state in top:
		if action==5 or action==6 or action==7 :
			return nodes
	if state in left:
		if action==3 or action==4 or action==5:
			return nodes
	if state in right:
		if action==7 or action==0 or action==1:
			return nodes
	if state in bottom:
		if action==1 or action==2 or action==3:
			return nodes
	if (action==0):
		state+=1
	elif (action==1):
		state+=comp_h+1
	elif (action==2):
		state+=comp_h
	elif (action==3):
		state+=comp_h-1
	elif (action==4):
		state-=1
	elif (action==5):
		state-=comp_h+1
	elif (action==6):
		state-=comp_h
	elif(action==7):
		state-=comp_h-1
	if( state<0 or state >nodes-1):
		return nodes
	else:
		return state

def chooseAnaction(i):
	
	node=i
	count=0
	#print cur_node
	action=randint(0,actions-1)	
	node_to_go=possible_node(node,action)
	x1,y1,x2,y2=0,0,0,0
	if node_to_go !=nodes:
		node_1=pose[node]
		node_2=pose[node_to_go]
		x1=node_1[1]
		y1=node_1[0]
		x2=node_2[1]
		y2=node_2[0]
		#print x1,y1,x2,y2
		#print edges[x1,y1],edges[x2,y2]
		if x2 < x1 :
			temp=x1
			x1=x2
			x2=temp
		if y2 < y1:
			temp=y1
			y1=y2
			y2=temp
		if x1==x2:
			for i in range(y1,y2,5):
				if edges[x1,i]==255:
					count+=1
		elif y1==y2:
			for j in range(x1,x2,5):
				if edges[j,y1]==255:
					count+=1
		else:
			for k,l in zip(range(x1,x2,5),range(y1,y2,5)):
				if edges[k,l]==255:
					count+=1
		if count>=1:
			node_to_go=nodes
	if (node_to_go==goal):
		reward=100
	elif (node_to_go==nodes):
		reward=-100
	else:
		reward=-1
	if (reward >=-1):
		Q[node][action]=int(reward+gamma*(max(Q[node_to_go])))
		#cur_node=node_to_go

start_time=0
def shortest():
	global start_time
	start_time = time.clock()
	for i in range(0,iterate):
		for j in range(0,nodes):	
			chooseAnaction(j)

shortest()
edges=cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)
def path(node,goal):
	count=0
	if (max(Q[node])==0):
		print '''
				
	oooops !!! I cant reach the node obstacle is there
		
	change the goal node to adjacent nodes
			
				'''
	else:
		while(node!=goal):
			ind=[j for j,x in enumerate(Q[node]) if x==max(Q[node])]
			action=ind[0]
			for l in range(len(ind)):
				if (path_cost[ind[l]] < path_cost[action]):
					action=ind[l]
			print node,action
			state=possible_node(node,action)
			#print state
			cv2.circle(edges,(pose[state][0],pose[state][1]), 4, (0,0,255), -1)	
			cv2.line(edges,(pose[node][0],pose[node][1]),(pose[state][0],pose[state][1]),(0,0,200),5)
			cv2.circle(img1,(pose[state][0],pose[state][1]), 4, (0,0,255), -1)	
			cv2.line(img1,(pose[node][0],pose[node][1]),(pose[state][0],pose[state][1]),(0,0,200),5)

			node=state	
			print node
path(node,goal)
print "Total time taken",time.clock() - start_time, "seconds"
cv2.imshow('edges',edges)
cv2.imshow('grid',img1)
#cv2.imshow('edges',edges)
cv2.waitKey(0)


