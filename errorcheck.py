import sys
from vertical_pairity import vp
from linear_pairity import lp
from checksum import cs
from cyclic import cy




infile=sys.argv[1]
errorlist=[]

print("checksum")
cs(infile,errorlist)
print("\ncyclic")
cy(infile,errorlist)
print("\nlinear")
lp(infile,errorlist)
print("\nvertical")
vp(infile,errorlist)