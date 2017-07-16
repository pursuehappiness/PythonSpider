
from selectors import DefaultSelector,EVENT_WRITE

selector = DefaultSelector()

def fetch(url):
	sock = socket.socket()
	sock.setblocking(False)
	try:
		socket.connect(('xkcd.com',80))
	except BlockingIOError:
		pass

def connected():
	selector.unregister(sock.fileno())
	print('connected')

selector.register(sock.fileno(),EVENT_WRITE,connected)

if __name__ == '__main__':
	fetch()
