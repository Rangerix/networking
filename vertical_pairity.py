import sys,os
from random import randint
from gen_err import hardcodederror

#==============================================
def generaterror(string):
	#print(string)	
	bound=len(string)
	numerror=randint(0,bound//2)					#number of error bit
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
def receivedata_vrc(receivedframes,framesize):
	check=0
	#print("received : ",receivedframes)
	tempdata=[]
	for bit in range(framesize):
		temp=[i[bit] for i in receivedframes]
		temp="".join(temp)
		#print(bit," pos : ",temp)
		tempdata.append(temp)
	flag=0
	for i in tempdata:
		val=i.count('1')
		if val%2 == 1:
			#print("error  ")
			flag=1
		else:
			a=1
			#print("noerror  ")
	if flag==1:
		return 1
	else:
		return 0
#==============================================

def vp(infile,errorlist):
	framesize=8
	with open(infile,"r") as f1:
		inputstream=f1.read()
	length=len(inputstream)
	inputs=[ inputstream[i:i+framesize] for i in range(0,length,framesize) ]
	outputs=[]
	sendframe=2

	sublist=[inputs[i:i+sendframe] for i in range(0,len(inputs),sendframe)]
	iserror=0
	for senddata in sublist:
		#print(senddata)
		
		tempdata=[]
		for bit in range(framesize):
			temp=[i[bit] for i in senddata]
			temp="".join(temp)
			#print(bit," pos : ",temp)
			tempdata.append(temp)
		errorsend=[]
		x=""
		for i in tempdata:
			#pairity
			val=i.count("1")
			if val%2 == 1:
				x+= "1"
			else:
				x+= "0"
		count=0
		for i in senddata:
			val=0 #randint(0,1)
			count+=1
			if val==1 :
				temp=hardcodederror(i,[0,4,7])
			else:
				temp=i
			errorsend.append(temp)
		errorsend.append(x)
		iserror+=receivedata_vrc(errorsend,framesize)
	if iserror!=0:
		print("error")
	else:
		print("noerror")