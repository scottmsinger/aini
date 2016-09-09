# aini
.ini based mechanism for project directory and path abstraction

a python implementation that uses .INI files to abstract file and directory path names to fascilitate bootstrapping modularity andportability in medium sized projects. 

**NOT READY FOR PRIME TIME**

supports multiple levels of includes (last reference wins)
variables stored unexpanded
defaults to a file named AINI in the calling directory


basics:
import the aini package
create an AINI object say - "aini"
read the AINI file (includes are traversed automatically)
AINI variables are then available as member variables of the aini object 

So for a media project the basic idea is to have an AINI file sitting at the shot directory which includes other AINI files from futher upstream - say at the sequence, project, facility levels. Directory information like where the root of the project is, or where assets and other data should be read from and written to, are defined in the upstream includes. These locations can be over-ridden as you progress downstream from the root include. The upstream includes can be stored in upstream files - this is inherently flexible and inherently dangerous because there's no accounting for cycles. Use responsibly.


