# _*_ coding: utf-8 _*_

import sys,os,string
import re
import numpy as np
import pandas as pd
import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt

if len(sys.argv) !=5:
	print("Syntax: python lmpdump.py *.lammpstrij totstep frequency totatom")
	sys.exit()
	
inFileName=sys.argv[1]
totstep=int(sys.argv[2])
frequency=int(sys.argv[3])
totatom=int(sys.argv[4])

totframe=int(totstep/frequency)
print(totframe)

#data=np.zeros([totframe,totatom,5])
data=[]

# dump command
# dump 1 all custom 500000 nvtcl.lammpstrj id type x y z
# id type x y z
with open(inFileName,"r") as f:
	for line in f:
		line_chunks=line.split()
		if line_chunks[0] !="ITEM:" and len(line_chunks) == 5:
			data.append(line_chunks)
								
data=np.array(data)
data=data.reshape([totframe+1,totatom,5])
			
with open("data.txt","w") as f:
	for i in range(totframe):
		print("Frame %d"%(i+1),file=f)
		for j in range(totatom):
			print("%8d %8d %8.3f %8.3f %8.3f"%(int(data[i,j,0]),int(data[i,j,1]),float(data[i,j,2]),\
			float(data[i,j,3]),float(data[i,j,4])),file=f)
		
					
			
			
