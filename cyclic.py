import sys,os
from random import randint
from gen_err import hardcodederror
#==============================================
def generaterror(string):
	print(string)	
	bound=len(string)
	numerror=randint(0,bound)					#number of error bit
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
def myxor(a,b):
	l=len(b)
	xor=[]
	for i in range(1,l):
		if a[i]==b[i]:
			xor.append("0")
		else:
			xor.append("1")
	xor="".join(xor)
	return xor

#==============================================
def division(dividend,divisor):
	pick=len(divisor)
	tmp=dividend[0:pick]
	while pick<len(dividend):
		if tmp[0]=='1' :
			tmp=myxor(divisor,tmp)+dividend[pick]
		else:
			tmp=myxor("0"*pick,tmp)+dividend[pick]
		pick+=1
	if tmp[0]=='1':
		tmp=myxor(divisor,tmp)
	else:
		tmp=myxor("0"*pick,tmp)
	return tmp

#==============================================
def encode(dataword,divisor):
	l=len(divisor)
	appendeddata=dataword+"0"*(l-1)
	remainder=division(appendeddata,divisor)
	#print("remainder : ",remainder)
	codeword=dataword+remainder
	return codeword

#==============================================
def receivedata_crc(receivedframes):
	check=0
	flag=0
	for i in receivedframes:
		val=division(i,divisor)
		#print("check val :",val)
		if val.count("0") != len(val):
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
divisor="10001001"
def cy(infile,errorlist):
	framesize=8
	divisor="10001001"
	with open(infile,"r") as f1:
		inputstream=f1.read()
	length=len(inputstream)
	inputs=[ inputstream[i:i+framesize] for i in range(0,length,framesize) ]
	outputs=[]


	sublist=inputs[:]
	count=0
	iserror=0
	for senddata in sublist:
		#print(senddata)
		count+=1
		senddata=encode(senddata,divisor)
			
		errorsend=[]
		val= 0#randint(0,1)
		if count%2==1 :
			temp=hardcodederror(senddata,errorlist)
		else:
			temp=senddata
		errorsend.append(temp)
		iserror+=receivedata_crc(errorsend)
	if iserror!=0:
		print("error")
	else:
		print("noerror")