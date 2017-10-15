import time
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('node-201', 8440))
sock.listen(10)

while True:
	print 'waiting for client ...'
	client_sock, client_address = sock.accept()
	print 'open client !!!', client_sock, client_address

	for i in range(10):
		data = str(i) + '\nhello\nworld\n'
		print 'send : ', data
		try: client_sock.send(data)
		except: break
		time.sleep(1)

	print 'close client !!!', client_sock, client_address
	client_sock.close()

