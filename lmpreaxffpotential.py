# _*_ coding: utf-8 _*_

import sys,os,string
import re
import numpy as np
import pandas as pd
import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt

if len(sys.argv) !=4:
	print("Syntax: python lmpreaxffpotential.py *.pot totstep frequency")
	sys.exit()
	
# read inFileName
inFileName=sys.argv[1]
inFile=open(inFileName,"r")
lines=inFile.readlines()
inFile.close()

totstep=int(sys.argv[2])
frequency=int(sys.argv[3])

totframe=int(totstep/frequency)

name=["step","ebond","eatom","elp","eang","ecoa","ehb","etor","econj","evdw","ecoul","epol"]

for line in lines:
	line_chunk=line.strip()
	line_chunk = re.split(r"\s+",line)
	if line_chunk[0] == "step":
		num=len(line_chunk)

print("#-----------------------------------------#")
print("There have %d columns in file"%(num))
print("#-----------------------------------------#")

data=np.array([totframe,num])
data=np.genfromtxt(inFileName,skip_header=1)
print(data.shape)

# Draw plot
for i in range(num-1):
	plt.figure(i+1)
	plt.plot(data[:,0],data[:,i+1],"g-",label=name[i+1])
	plt.plot(data[:,0],data[:,i+1],"g-")
	plt.xlabel(name[0])
	plt.ylabel(name[i+1])
	plt.title("%s energy in reaxff system"%(name[i+1]))
	plt.legend(loc="best")
	plt.savefig("%s.jpg"%(name[i+1]),dpi=300)
	#plt.show()

