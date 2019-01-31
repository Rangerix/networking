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
	flag=0
	for i in receivedframes:
		val=i.count('1')
		if val%2 == 1:
			#print("error : ",i)
			flag=1
		else:
			a=1
			#print("noerror : ",i)
	if flag==1:
		return 1
	else:
		return 0
#==============================================
def lp(infile,errorlist):
	framesize=8
	with open(infile,"r") as f1:
		inputstream=f1.read()
	length=len(inputstream)
	inputs=[ inputstream[i:i+framesize] for i in range(0,length,framesize) ]
	outputs=[]

	sublist=inputs[:]
	iserror=0
	for senddata in sublist:
		#print(senddata)
		
		#even pairity
		val=senddata.count('1')
		if val % 2 == 1 : #odd number of 1's
			senddata+="1"
		else:
			senddata+="0"

		errorsend=[]
		val=0 #randint(0,1)
		if val==1 :
			temp=hardcodederror(senddata,errorlist)
		else:
			temp=senddata
		errorsend.append(temp)
		iserror+=receivedata(errorsend)
	if iserror!=0:
		print("error")
	else:
		print("noerror")