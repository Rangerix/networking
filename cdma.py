import sys,numpy

class Station:
	code="" 
	data=""

def convert(x):
	if x=='1':
		return 1
	if x=='0':
		return -1
	if x=='i':
		return 0

infile=sys.argv[1]

stcount=input("how many station? ")
stcount=int(stcount)
r=range(stcount)
walsh_table=[[int(bin(x&y),13)%2or-1for x in r]for y in r]

for i in walsh_table:
	print(i)

with open(infile,"r") as f:
	alldata=f.read().splitlines()

datalength=len(alldata[0])
stations=[]
index=0
for data in alldata:
	temp=Station()
	temp.code=walsh_table[index]
	temp.data=alldata[index]
	stations.append(temp)
	index+=1

print(datalength)
for bit in range(datalength):
	channel=numpy.zeros(stcount)
	#print("bit : ",bit)
	for index in range(stcount):
		temp=stations[index]
		d=temp.data[bit]
		d=convert(d)
		c=temp.code
		#print(c)
		c=numpy.array(c)
		x=d*c
		#print(x)
		channel+=x
	print("data in channel : ",channel)
	print("\ndecoding channel data")
	for index in range(stcount):
		c=stations[index].code
		c=numpy.array(c)
		val=numpy.multiply(c,channel)
		res=numpy.sum(val)
		print("station",index,"data",res/stcount)
