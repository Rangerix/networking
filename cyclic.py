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
	for i in receivedframes:
		val=division(i,divisor)
		#print("check val :",val)
		if val.count("0") != len(val):
			print("error : ",i)
		else:
			print("noerror : ",i)

#==============================================
infile=sys.argv[1]
framesize=8
divisor="10001001"
with open(infile,"r") as f1:
	inputstream=f1.read()
length=len(inputstream)
inputs=[ inputstream[i:i+framesize] for i in range(0,length,framesize) ]
outputs=[]


sublist=inputs[:]
for senddata in sublist:
	print(senddata)
	
	senddata=encode(senddata,divisor)
		
	errorsend=[]
	val= 1#randint(0,1)
	if val==1 :
		temp=hardcodederror(senddata,[0])
	else:
		temp=senddata
	errorsend.append(temp)
	receivedata_crc(errorsend)
