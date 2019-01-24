import sys,os
from random import randint
from gen_err import hardcodederror

#==============================================
def generaterror(string):
	print(string)	
	bound=len(string)
	numerror=randint(0,bound//2)					#number of error bit
	for _ in range(numerror):
		bit=randint(0,bound-1)
		if string[bit]=='1':
			string=string[:bit]+'0'+string[bit+1:]
		else:
			string=string[:bit]+'1'+string[bit+1:]
	print(string)
	print()
	return string
#==============================================
def receivedata_vrc(receivedframes):
	check=0
	#print("received : ",receivedframes)

	for i in receivedframes:
		val=i.count('1')
		if val%2 == 1:
			print("error : ",i)
		else:
			print("noerror : ",i)
#==============================================

infile=sys.argv[1]

framesize=2
with open(infile,"r") as f1:
	inputstream=f1.read()
length=len(inputstream)
inputs=[ inputstream[i:i+framesize] for i in range(0,length,framesize) ]
outputs=[]
print(outputs)
sendframe=8

sublist=[inputs[i:i+sendframe] for i in range(0,len(inputs),sendframe)]
for senddata in sublist:
	#print(senddata)
	
	tempdata=[]
	for bit in range(framesize):
		temp=[i[bit] for i in senddata]
		temp="".join(temp)
		#print(bit," pos : ",temp)
		tempdata.append(temp)
	errorsend=[]
	for i in tempdata:
		#pairity
		val=i.count("1")
		if val%2 == 1:
			i+= "1"
		else:
			i+= "0"

		val=1 #randint(0,1)
		if val==1 :
			temp=hardcodederror(i,[0,4,7])
		else:
			temp=i
		errorsend.append(temp)
	receivedata_vrc(errorsend)
