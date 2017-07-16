
def fetch(url):
	sock = socket.socket()
	socket.connect(('xkcd.com',80))
	request = 'Get {} HTTP/1.0\r\nHost: xkcd.com\r\n\r\n'.format(url)

	sock.send(request.encode('ascii'))
	response = b''
	chunk = sock.recv(4096)

	while chunk:
		response += chunk
		chunk = sock.recv(4096)

	links = parse_links(response)
	q.add(links)


if __name__ == '__main__':
	fetch()
