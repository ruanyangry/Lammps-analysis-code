# _*_ coding: utf-8 _*_

import sys,os,string
import numpy as np
from sympy import *

if len(sys.argv) !=5:
	print("usage: python lmptable.py input.inp totatomtypes")
	sys.exit()

print('##############################################################')
print('#    usage: python lmptable-lj.py input.inp totatomtypes     #')
print('#    This code used to create lammps table potential file    #')
print('#current support pair_style in Liu Jun doctoral dissertation #')
print('#    input file input.inp need contains atom type number and #')
print('#         each types sigma epsion charge information         #')
print('##############################################################')
print(" ")	

# 这个程序中需要注意一下输入文件的格式了，将polymer的放置在最前面，nanopatricle
# 放置在后面，后续在做循环的时候就需要注意下了

# define function
# polymer-bead polymer-bead interaction
#      4*epsion*((sigma/r)**12-(sigma/r)**6+0.25) r<2*(1/6)*sigmapp
# u(r) 
#      0                                          r>2*(1/6)*sigmapp

def Epp(sigma,epsion,r):
	Energy=4*epsion*((sigma/r)**12-(sigma/r)**6+0.25)
	return Energy
	
def Fpp(sigma,epsion,r):
	Force=4*epsion*(sigma)**6*(6*((r)**(-7))-12*(sigma)**2*((r)**(-13)))
	return Force
	
# polymer bead Nanoparticles interaction
# polymer bead Nanoparticles interaction cutoff
# cutoff = rev+2.5*sigma
# rn == represent the radius of Nanoparticles
# epsion == Nanoparticles - polymer bead = 1.0
# sigma == polymer bead = 1.0
#      4*epsion*((sigma/(r-rev))**12-(sigma/(r-rev))**6+0.25) r > rev=rn-sigma/2
# u(r)
#        INF                                                  r <= rev=rn-sigma/2   

def Enp(sigma,epsion,r,rev):
	Energy=4*epsion*((sigma/(r-rev))**12-(sigma/(r-rev))**6+0.25)
	return Energy
	
def Fnp(sigma,epsion,r,rev):
	Force=4*epsion*(sigma)**6*(6*((r-rev)**(-7))-\
	12*(sigma)**2*((r-rev)**(-13)))
	return Force     
	
# Nanoparticles - Nanoparticles interaction	 
# Nanoparticles - Nanoparticles interaction	 cut-off
# cutoff=rev+2*(1/6)*sigma
# epsion == Nanoparticles = 1.0
# rn == represent the radius of Nanoparticles
#      4*epsion*((sigma/(r-rev))**12-(sigma/(r-rev))**6+0.25) r > rev=2*rn-sigma
# u(r)
#                INF                                          r <= rev=2*rn-sigma

def Enn(sigma,epsion,r,rev):
	Energy=4*epsion*((sigma/(r-rev))**12-(sigma/(r-rev))**6+0.25)
	return Energy
	
def Fnn(sigma,epsion,r,rev):
	Force=4*epsion*(sigma)**6*(6*((r-rev)**(-7))-\
	12*(sigma)**2*((r-rev)**(-13)))
	return Force
	
# load input.inp file
# N1 = total polymer bead atom type
# N2 = total Nanoparticle atom type

inFileName=sys.argv[1]
tottypes=int(sys.argv[2])
N1=int(sys.argv[3])
N2=int(sys.argv[4])
atomtype=np.zeros([tottypes,4])

head=5
atomtype[:,:]=np.genfromtxt(inFileName,skip_header=head)

# define variable
zero=0.0
rinc=0.005
rinit=4.5
rcutmax=3.0*(max(atomtype[:,1]))
n=int((rcutmax-rinit)/rinc+1.0)	
Rn=                              # the radius of Nanoparticles
INF=float(10**20)

with open("lmptable-ljcut.txt","w") as f:
	# polymer-polymer bead
	for i in range(N1):
		for j in range(i,N1):
			# L-B mixed rule
			sig=(atomtype[i,1]+atomtype[j,1])/2.0
			eps=np.sqrt(atomtype[i,2]*atomtype[j,2])
			rcut=(2**(1/6))*sig
			
			print("%s"%(str(int(atomtype[i,0]))+"-"+\
			str(int(atomtype[j,0]))),file=f)
			print("%s %d %s %.4f %.4f"%("N",n,"R",rinit,rcutmax),file=f)
			print(" ",file=f)
			for k in range(n):
				r=rinit+(k-1)*rinc
				En=Epp(sig,eps,r)
				Fc=Fpp(sig,eps,r)
				if r < rcut:
					print("%6d %.3f %.6f %.6f"%(k,r,En,Fc),file=f)
				else:
					En=zero
					Fc=zero
					print("%6d %.3f %.6f %.6f"%(k,r,En,Fc),file=f)
			print(" ")
			
	print('--------------------------------------------------------------')
	print("write polymer-polymer bead interaction done")
	print('--------------------------------------------------------------')
	print(" ")		
	
	# Nanoparticle - Nanoparticle bead
	for i in range(N1,(N2+N1)):
		for j in range(i,(N2+N1)):
			# L-B mixed rule
			sig=(atomtype[i,1]+atomtype[j,1])/2.0
			eps=np.sqrt(atomtype[i,2]*atomtype[j,2])
			rcut=2*Rn-sig
			rev=2*Rn-sig
			
			print("%s"%(str(int(atomtype[i,0]))+"-"+\
			str(int(atomtype[j,0]))),file=f)
			print("%s %d %s %.4f %.4f"%("N",n,"R",rinit,rcutmax),file=f)
			print(" ",file=f)
			for k in range(n):
				r=rinit+(k-1)*rinc
				En=Enn(sig,eps,r,rev)
				Ec=Fnn(sig,eps,r,rev)
				if r > rcut:
					print("%6d %.3f %.6f %.6f"%(k,r,En,Fc),file=f)
				else:
					En=INF
					Fc=INF
					print("%6d %.3f %.6f %.6f"%(k,r,En,Fc),file=f)
			print(" ")
			
	print('--------------------------------------------------------------')
	print("write Nanoparticle - Nanoparticle bead done")
	print('--------------------------------------------------------------')
	print(" ")		
	
	# polymer bead-Nanoparticle bead
	for i in range(N1):
		for j in range(N1,(N2+N1)):
			# L-B mixed rule
			sig=(atomtype[i,1]+atomtype[j,1])/2.0
			eps=np.sqrt(atomtype[i,2]*atomtype[j,2])
			rcut=Rn-sig/2.0
			rev=Rn-sig/2.0
			print("%s"%(str(int(atomtype[i,0]))+"-"+\
			str(int(atomtype[j,0]))),file=f)
			print("%s %d %s %.4f %.4f"%("N",n,"R",rinit,rcutmax),file=f)
			print(" ",file=f)
			for k in range(n):
				r=rinit+(k-1)*rinc
				En=Enp(sig,eps,r,rev)
				Fc=Fnp(sig,eps,r,rev)
				if r > rcut:
					print("%6d %.3f %.6f %.6f"%(k,r,En,Fc),file=f)
				else:
					En=INF
					Fc=INF
					print("%6d %.3f %.6f %.6f"%(k,r,En,Fc),file=f)
			print(" ")
			
	print('--------------------------------------------------------------')
	print("write polymer - Nanoparticle bead done")
	print('--------------------------------------------------------------')
	print(" ")		
					
			
			
					
