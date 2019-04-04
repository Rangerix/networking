import socket
import sys  

infile=sys.argv[1]
s = socket.socket()        
host = socket.gethostname()
port = 12345               
s.bind((host, port))       
f = open(infile,'wb')
s.listen(5)                
while True:
	c, addr = s.accept()   
	print 'Got connection from', addr
	print "Receiving..."
	l = c.recv(1024)
	while (l):
		print "Receiving..."
		f.write(l)
		l = c.recv(1024)
	f.close()
	print "Done Receiving"
	c.close()
s.close()