# _*_ coding: utf-8 _*_

import sys,os,string
import numpy as np
from sympy import *

if len(sys.argv) !=3:
	print("usage: python lmptable.py input.inp totatomtypes")
	sys.exit()

print('##############################################################')
print('#    usage: python lmptable.py input.inp totatomtypes        #')
print('#    This code used to create lammps table potential file    #')
print('#    current support pair_style lj/cut and lj/expand         #')
print('#    input file input.inp need contains atom type number and #')
print('#         each types sigma epsion charge information         #')
print('##############################################################')
print(" ")

# define function
# pair_style lj/cut
def E(sigma,epsion,r):
	Energy=4.0*(epsion)*((sigma/r)**12-(sigma/r)**6)
	return Energy
	
# E' = F 能量的导数为力
# https://www.zhihu.com/question/35216085
# x=Symbol("r")
# df=diff((r)**(-12)-(r)**(-6),x)

def F(sigma,epsion,r):
	Force=4*epsion*(sigma)**6*(6*((r)**(-7))-12*(sigma)**2*((r)**(-13)))
	return Force

inFileName=sys.argv[1]
tottypes=int(sys.argv[2])

atomtype=np.zeros([tottypes,4])

head=5
atomtype[:,:]=np.genfromtxt(inFileName,skip_header=head)

# define variable
zero=0.0
rinc=0.008
rinit=2.0
rcutmax=3.0*(max(atomtype[:,1]))
#rcutmax=7.0
n=int((rcutmax-rinit)/rinc+1.0)

with open("lmptable-ljcut.txt","w") as f:
	for i in range(tottypes):
		for j in range(i,tottypes):
			# L-B mixed rule
			sig=(atomtype[i,1]+atomtype[j,1])/2.0
			eps=np.sqrt(atomtype[i,2]*atomtype[j,2])
			rcut=3.0*sig
			#rcut=rcutmax
			
			print("%s"%(str(int(atomtype[i,0]))+"-"+\
			str(int(atomtype[j,0]))),file=f)
			print("%s %d %s %.4f %.4f"%("N",n,"R",rinit,rcutmax),file=f)
			print(" ",file=f)
			for k in range(n):
				r=rinit+(k-1)*rinc
				En=E(sig,eps,r)
				Fc=F(sig,eps,r)
				if r <= rcut:
					print("%6d %.3f %.6f %.6f"%(k,r,En,Fc),file=f)
				else:
					En=zero
					Fc=zero
					print("%6d %.3f %.6f %.6f"%(k,r,En,Fc),file=f)
			print(" ",file=f)
					
print('--------------------------------------------------------------')
print("write pair_style lj/cut done")
print('--------------------------------------------------------------')

print(" ")
	
# pair_style lj/expand
def Eexpand(sigma,epsion,r,delt):
	Energy=4*epsion*((sigma/(r-delt))**12-(sigma/(r-delt))**6)
	return Energy
	

def Fexpand(sigma,epsion,r,delt):
	Force=4*epsion*(sigma)**6*(6*((r-delt)**(-7))-\
	12*(sigma)**2*((r-delt)**(-13)))
	return Force	
	
with open("lmptable-ljexpand.txt","w") as f:
	for i in range(tottypes):
		for j in range(i,tottypes):
			# L-B mixed rule
			sig=(atomtype[i,1]+atomtype[j,1])/2.0
			eps=np.sqrt(atomtype[i,2]*atomtype[j,2])
			rcut=3.0*sig
			#rcut=rcutmax
			
			print("%s"%(str(int(atomtype[i,0]))+"-"+\
			str(int(atomtype[j,0]))),file=f)
			print("%s %d %s %.4f %.4f"%("N",n,"R",rinit,rcutmax),file=f)
			print(" ",file=f)
			for k in range(n):
				r=rinit+(k-1)*rinc
				En=Eexpand(sig,eps,r,0.0)/10793
				Fc=Fexpand(sig,eps,r,0.0)/10793
				if r <= rcut:
					print("%6d %.3f %.6f %.6f"%(k,r,En,Fc),file=f)
				else:
					En=zero
					Fc=zero
					print("%6d %.3f %.6f %.6f"%(k,r,En,Fc),file=f)
			print(" ",file=f)	
			
print('--------------------------------------------------------------')
print("write pair_style lj/expand done")
print('--------------------------------------------------------------')		
			
			
