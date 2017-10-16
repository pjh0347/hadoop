import re
import time
import socket
from threading import Thread 

class WorkerThread(Thread):

	def __init__(self, client_sock, client_address):
		Thread.__init__(self)
		self.client_sock = client_sock
		self.client_address = client_address
		print self.client_address, '[open]'

	def run(self):
		for i in range(100):
			data = str(i) + '\nhello\nworld\n'
			print self.client_address, '[send]', data.replace('\n', '\\n')
			try: self.client_sock.send(data)
			except: break
			time.sleep(1)

		print self.client_address, '[close]'
		self.client_sock.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('node-201', 8440))
sock.listen(10)
print 'waiting for client ...'

while True:
	client_sock, client_address = sock.accept()
	WorkerThread(client_sock, client_address).start()

