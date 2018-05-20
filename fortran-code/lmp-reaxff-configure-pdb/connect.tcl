#Programmed by Sobereva, 2012-Jan-25
# First need load XXX.pdb file
mol load pdb B-H-B.pdb
set natm 39
set nskipline 42
#itype=0 means reset connectivity by user-defined list, =1 means add self-defined connectivity list to the original one
set itype 0
set rdpdbcon [open "C:/Users/RY/Desktop/B-H-B.pdb" r]

#Skip other lines
for {set i 1} {$i<=$nskipline} {incr i} {
gets $rdpdbcon line
}

#Cycle each atom
set ird 1
for {set iatm 1} {$iatm<=$natm} {incr iatm} {

if {$ird==1} {
 for {set i 1} {$i<=12} {incr i} {set cn($i) 0}
 gets $rdpdbcon line
 scan [string range $line 6 84] "%d %d %d %d %d %d %d %d %d %d %d %d %d" self cn(1) cn(2) cn(3) cn(4) cn(5) cn(6) cn(7) cn(8) cn(9) cn(10) cn(11) cn(12)

 set tmplist {}
 #Formation of connectivity list
 for {set i 1} {$i<=12} {incr i} {
  if {$cn($i)==0} {break}
  lappend tmplist [expr $cn($i)-1]
 }
}

if {$self==$iatm} {
 #puts Atom\ serial:\ $iatm\ \ User-connectivity:\ $tmplist
 set sel [atomselect top "serial $iatm"]
 if {$itype==0} {
  $sel setbonds "{$tmplist}"
 } else {
  set orglist [$sel getbonds]
  $sel setbonds "{[concat [lindex $orglist 0] $tmplist]}"
 }
 $sel delete
 set ird 1
} else {
 set ird 0
}

}
close $rdpdbcon