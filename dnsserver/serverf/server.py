iptoname = {1: "Geeks", 2: "For", 3: "Geeks"} 
nametoip= {"Geeks":1,  "For":2, "Geeks":3}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port =2889
sock.bind(('',port))

while True:
	data,addr=sock.recvfrom(512)
	data=data.decode()
	if data in iptoname :
		xyz=iptoname[data]
	elif data in nametoip :
		xyz=nametoip[data]
	else :
		xyz="vulval request"
	sock.sendto(data.encode(),0,addr)
sock.close()