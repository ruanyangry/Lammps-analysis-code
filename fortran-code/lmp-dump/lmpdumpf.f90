    program lmpdump
	 implicit none
	 integer i,j,k,l
	 integer totstep,frequency,totframe,totatom
	 real(kind=8) lx,ly,lz,volume
	 real(kind=8),allocatable:: coord(:,:,:)
	 real(kind=8),allocatable:: xlo(:),xhi(:),ylo(:),yhi(:),zlo(:),zhi(:)
	 character*80 filename
	 
	 open(unit=10,file="input.in",status="unknown")
	 open(unit=11,file="dump.txt",status="unknown")
	 open(unit=13,file="box.txt",status="unknown")
	 
	 read(10,*)filename
	 read(10,*)totstep
	 read(10,*)frequency
	 read(10,*)totatom
	 
	 totframe=totstep/frequency
	 
! dump 1 all custom 500000 nvtcl.lammpstrj id type x y z 
! record id type x y z  need 5 columns	 
	 allocate(coord(totframe,totatom,5))
	 allocate(xlo(totframe))
	 allocate(xhi(totframe))
	 allocate(ylo(totframe))
	 allocate(yhi(totframe))
	 allocate(zlo(totframe))
	 allocate(zhi(totframe))
	 
	 coord=0.0
	 xlo=0.0
	 xhi=0.0
	 ylo=0.0
	 yhi=0.0
	 zlo=0.0
	 zhi=0.0
	 
	 
	 open(unit=12,file=filename)
	 do i=1,totframe
	    read(12,*)
		read(12,*)
		
		read(12,*)
		read(12,*)
		
		read(12,*)
		read(12,*)xlo(i),xhi(i)
		read(12,*)ylo(i),yhi(i)
		read(12,*)zlo(i),zhi(i)
		
		read(12,*)
		
		do j=1,totatom
		    read(12,*)coord(i,j,:)
		end do
	end do
	
	do i=1,totframe
	    write(11,1001)"Frame =",i
	        do j=1,totatom
                write(11,1002)int(coord(i,j,1:2)),coord(i,j,3:)
			end do
	end do
	
	do i=1,totframe
	   write(13,1001)"Frame =",i
	   lx=xhi(i)-xlo(i)
	   ly=yhi(i)-ylo(i)
	   lz=zhi(i)-zlo(i)
	   volume=(lx*ly*lz)
	   write(13,1003)xlo(i),xhi(i),ylo(i),yhi(i),zlo(i),zhi(i),volume
	   write(13,*)
	end do
	
1001 format(A10,I8)
1002 format(2I8,3f8.3)
1003 format(6f8.3,f12.3)

     close(10)
	 close(11)
	 
	 end program lmpdump
	 
	 