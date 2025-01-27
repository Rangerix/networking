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
def wrap(chksumbin,framesize):
	chksumbin=chksumbin.split("b")
	chksumbin=chksumbin[-1]
	while len(chksumbin)>framesize :
			temp=chksumbin[:-framesize]
			chksumbin=chksumbin[-framesize:]
			chksum=int(temp,2)+int(chksumbin,2)
			chksumbin=bin(chksum)[2:]
	return chksumbin
#==============================================
def receivedata_chksum(receivedframes,framesize):
	check=0
	for i in receivedframes:
		#print(i)
		check+=int(i,2)
	check = bin(check)
	check=wrap(check,framesize)
	check=onescomplement(check)
	#print("result : ",check)
	flag=0
	if check.count("0") != len(check):
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
def onescomplement(string):
	string=string.replace('0','x')
	string=string.replace('1','0')
	string=string.replace('x','1')
	return string
#==============================================
def cs(infile,errorlist):
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
		chksum=0
		for i in senddata:
			temp=int(i,2)
			chksum+=temp
		#print("chksum",chksum)
		chksumbin=bin(chksum)[2:]
		#print(chksumbin)
		chksumbin=wrap(chksumbin,framesize)
		#print(chksumbin)
		chksumbin=onescomplement(chksumbin)
		#print("chksum ",chksumbin)
		errorsend=[]
		for i in senddata:
			val=0 #randint(0,1)
			if val==1 :
				temp=hardcodederror(i,errorlist)
			else:
				temp=i
			errorsend.append(temp)
		errorsend.append(chksumbin)
		iserror+=receivedata_chksum(errorsend,framesize)
	if iserror!=0:
		print("error")
	else:
		print("noerror")