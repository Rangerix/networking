import socket

name=str(input("input : "))
host=
port=2889
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((host,port))
sock.sendto(name.encode(),0,(host,port))

data,addr=sock.recvfrom(512)
data=data.decode()
print(data)
sock.close()