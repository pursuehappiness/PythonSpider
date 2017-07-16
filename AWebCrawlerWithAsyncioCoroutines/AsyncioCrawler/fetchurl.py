
def fetch(url):
	sock = socket.socket()
	sock.setblocking(False)
	try:
		socket.connect(('xkcd.com',80))
	except BlockingIOError:
		pass

	request = 'Get {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(url)
	encoded = request.encode('ascii')

	while True:
		try:
			sock.send(encoded)
			break
		except OSError as e:
			pass

	print('sent')


if __name__ == '__main__':
	fetch()
