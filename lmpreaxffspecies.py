# _*_ coding: utf-8 _*_

import sys,os,string
import re
import numpy as np
import pandas as pd
import matplotlib
#matplotlib.use("Agg")
import matplotlib.pyplot as plt

if len(sys.argv) !=4:
	print("Syntax: python readreaxff-v1.py species.out totstep frequency")
	sys.exit()
	
inFileName=sys.argv[1]
inFile=open(inFileName,"r")
lines=inFile.readlines()
inFile.close()

totstep=int(sys.argv[2])
frequency=int(sys.argv[3])
totframe=totstep/frequency

mol=[]
num=[]

for line in lines:
    lines = line.strip()
    lines = re.split(r"\s+", lines)
    if lines[0] == "#":
        mol.append(lines[1:])
    else:
        num.append(lines[:])
		
# make dictory
dict1= [dict(zip(mol[i], num[i])) for i in range(0,len(mol))]

# convert to pandas DataFrame
df = pd.DataFrame(dict1)

# Display options
pd.set_option('display.max_columns', 500)

# get the table information
print("#-----------------------------------------------#")
print("columns equal %d"%(df.columns.size))
for i in range(len(df.columns)):
	if df.columns[i] != "Timestep" and df.columns[i] != "No_Moles" and df.columns[i] != "No_Specs":
		print(df.columns[i])   

# None = 0
df_fill=df.fillna(0)

# string convert to integeter
format1 = lambda x :int(x)
df = df_fill.applymap(format1)

# write molecules name to file
with open("molecules-name.txt","w") as f:
	for i in range(len(df.columns)):
		if df.columns[i] != "Timestep" and df.columns[i] != "No_Moles" and df.columns[i] != "No_Specs":
			print("%s %d"%((df.columns[i]),df[df.columns[i]].sum()),file=f)

from pylab import *

x=(df["Timestep"]*0.1)/1000

# All molecules in one Figure
plt.figure(1)
for i in range(len(df.columns)):
	if df.columns[i] != "Timestep" and df.columns[i] != "No_Moles" and \
	df.columns[i] != "No_Specs":
		total=df[df.columns[i]].sum()
		if total >= 10:
			y=df[df.columns[i]]
			#plt.scatter(x,y,label=df.columns[i])
			plt.plot(x,y,label=df.columns[i])

plt.xlabel("frame (ps)")
plt.ylabel("Number")
plt.legend(loc="best")
plt.title("Number of molecules")
plt.savefig("molecules.jpg",dpi=300)		
plt.show()

print("#-----------------------------------------------#")
print("Draw done")
print("#-----------------------------------------------#") 	
