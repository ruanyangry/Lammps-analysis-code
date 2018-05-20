# Lammps-analysis-code
This repository contained Fortran and python code used to analysis lammps output file.

lmpreaxffspecies.py: used to analysis lammps reax module output file species.out.  

    Usage: python lmpreaxffspecies.py species.out totstep writefrequecny
         
lmpreaxffpotential.py: used to display the potential, input file *.pot.  
    
    Usage: python lmpreaxffpotential.py *.pot totstep frequency
  
lmpdump.py: used to read *.lammpstrj file.   
  
    Usage: python lmpdump.py *.lammpstrij totstep frequency totatom
    
    if you used it ,please accroding you  dump command setting modified the following content and output setting:
       dump command
       dump 1 all custom 500000 nvtcl.lammpstrj id type x y z
       id type x y z
       if line_chunks[0] !="ITEM:" and len(line_chunks) == 5:
            number 5 = len(id type x y z)
            
Lmpplot.py: Read lammps output file fix ave/chunk, fix ave/time, log and lammps trajectory file

    Usage:https://github.com/ruanyangry/gromacs-lammps-process-simulation  
    




