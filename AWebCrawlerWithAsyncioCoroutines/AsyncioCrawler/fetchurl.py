
from selectors import DefaultSelector,EVENT_WRITE

selector = DefaultSelector()

def fetch(url):
	fetcher = Fetcher('/353/')
	fetcher.fetch()

	while True:
		events = selector.select()

		for event_key,event_mask in events:
			callback = event_key.data
			callback(event_key,event_mask)

def connected():
	selector.unregister(sock.fileno())
	print('connected')

def loop():
	while  True:
		events = selector.select()
		for event_key, event_mask in events :
			callback = event_key.data
			callback()

selector.register(sock.fileno(),EVENT_WRITE,connected)

urls_todo = set(['/'])
seen_urls = set(['/'])

class Fetcher:
	def __init__(self,url):
		self.response = b''
		self.url = url
		self.sock = None

	def fetch(self):
		self.sock = socket.socket()
		self.sock.setblocking(False)
		try:
			self.sock.connect(('xkcd.com',80))
		except BlockingIOError:
			pass

		selector.register(self.sock.fileno(),
			EVENT_WRITE,self.connected
			)

	def connected(self,key,mask):
		print('connected')

		selector.unregister(key.fd)
		request = 'Get {} HTTP/1.0\r\nHost:xkcd.com\r\n\r\n'.format(self.url)
		self.sock.send(request.encode('ascii'))

		selector.register(key.fd,EVENT_READ,self.read_response)



if __name__ == '__main__':
	fetch()
