import sys,os
from random import randint
from gen_err import hardcodederror

#==============================================
def generaterror(string):
	#print(string)	
	bound=len(string)
	numerror=randint(0,bound)					#number of error bit
	for _ in range(numerror):
		bit=randint(0,bound-1)
		if string[bit]=='1':
			string=string[:bit]+'0'+string[bit+1:]
		else:
			string=string[:bit]+'1'+string[bit+1:]
	#print(string)
	#print()
	return string
#==============================================
def receivedata(receivedframes):
	check=0
	for i in receivedframes:
		val=i.count('1')
		if val%2 == 1:
			print("error : ",i)
		else:
			print("noerror : ",i)
#==============================================
infile=sys.argv[1]
framesize=8
with open(infile,"r") as f1:
	inputstream=f1.read()
length=len(inputstream)
inputs=[ inputstream[i:i+framesize] for i in range(0,length,framesize) ]
outputs=[]
print(outputs)

sublist=inputs[:]
for senddata in sublist:
	print(senddata)
	
	#even pairity
	val=senddata.count('1')
	if val % 2 == 1 : #odd number of 1's
		senddata+="1"
	else:
		senddata+="0"

	errorsend=[]
	val=1 #randint(0,1)
	if val==1 :
		temp=hardcodederror(senddata,[0])
	else:
		temp=senddata
	errorsend.append(temp)
	receivedata(errorsend)
