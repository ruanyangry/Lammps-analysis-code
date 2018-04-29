# Lammps-analysis-code
This repository contained Fortran and python code used to analysis lammps output file.

1 lmpreaxffspecies.py code used to analysis lammps reax module output file species.out.
  usage: python lmpreaxffspecies.py species.out totstep writefrequecny
         
2 lmpreaxffpotential.py code used to display the potential, input file *.pot.
  usage: python lmpreaxffpotential.py *.pot totstep frequency
  
3 lmpdump.py code used to read *.lammpstrj file. 
  usage: python lmpdump.py *.lammpstrij totstep frequency totatom
  if you used it ,please accroding you  dump command setting modified the following content and output setting:
  # dump command
  # dump 1 all custom 500000 nvtcl.lammpstrj id type x y z
  # id type x y z
  if line_chunks[0] !="ITEM:" and len(line_chunks) == 5:
  number 5 = len(id type x y z)
