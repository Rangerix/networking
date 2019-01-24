def pos_error(string,bit):
	if string[bit]=='1':
		string=string[:bit]+'0'+string[bit+1:]
	else:
		string=string[:bit]+'1'+string[bit+1:]
	return string

def hardcodederror(string,error):
	for pos in error:
		string=pos_error(string,pos)
	return string