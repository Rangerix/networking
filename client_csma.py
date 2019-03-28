import socket
import sys
import pickle
from time import sleep
import threading
import random
probability_factor = 0.9

class Receive(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "receive"
		self.alive = True

	def stop(self):
		self.alive = False

	def run(self):
		while self.alive:

			response, server = sock.recvfrom(4096)
			response = pickle.loads(response)

			if response["response"] == "data" and response["to"] == portname:
				print("\n{}: {}".format(response["from"], response["data"]))


class Sender(threading.Thread):
	def __init__(self, server_address):
		threading.Thread.__init__(self)
		self.server_address = server_address
		self.name = "sender"
		self.alive = True

	def stop(self):
		self.alive = False

	def run(self):
		k=1
		senderSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		while self.alive:
			to = str(input("Send to port number : "))
			if to == "q":
				break
			msg = str(input("Data to be transmitted : "))
			backoff = 1
			while True:
				senderSocket.sendto(pickle.dumps({"type":"isbusy"}), self.server_address)
				response, server = senderSocket.recvfrom(4096)
				response = pickle.loads(response)

				probability_outcome = random.random()
				print("Probability Outcome = {}".format(probability_outcome))

				if response["response"] == "ready":
					if probability_outcome <= probability_factor:
						print("Transmitting Data")
						print("Got Connection With... {}".format(to))
						senderSocket.sendto(pickle.dumps({"type":"makebusy"}), self.server_address)
						sleep(5)
						senderSocket.sendto(pickle.dumps({"type":"data", "data":msg, "to":to, "from":portname}), self.server_address)
						print("Packet delivered")
						print("**************************************\n")
						break
					else:
						print("channel busy. sending jamming signal. Backoff = {}s".format(backoff))
						sleep(backoff)
						backoff = random.randint(1,2**k)
						k=k+1
						if backoff == 64:
							k=1
							print("Packet died. Try again later")
							print("**************************************\n")
							break
				elif response["response"] == "busy":
					print("channel busy. sending jamming signal. Backoff = {}s".format(backoff))
					sleep(backoff)
					backoff = random.randint(1,2**k)
					k=k+1
					if backoff == 64:
						k=1
						print("Backoff for too long. Sending aborted")
						print("**************************************\n")
						break
		senderSocket.close()


if len(sys.argv) == 2:
	portname = str(sys.argv[1])
	print("New Host {}".format(portname))
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	server_address = ('localhost', 10000)
	lock = threading.RLock()
	send_thread = Sender(server_address)
	receive_thread = Receive()
	try:
		while True:
			sock.sendto(pickle.dumps({"type":"connect"}), server_address)
			response, sender_address = sock.recvfrom(4096)
			if pickle.loads(response)["response"] == "connected":
				print("Connected to channel network...")
				print("**************************************\n")
				break

		send_thread.start()
		receive_thread.start()
	except KeyboardInterrupt:
		send_thread.stop()
		receive_thread.stop()
	finally:
		send_thread.join()
		receive_thread.stop()

		print("Killing Thread")
		while True:
			sock.sendto(pickle.dumps({"type":"close"}), server_address)
			break
			response, sender_address = sock.recvfrom(4096)
			if pickle.loads(response)["response"] == "disconnected":
				print("Disconnected from channel network...")
				break
		print('Closing socket')
		sock.close()
else:
	print('One arg is reqd')