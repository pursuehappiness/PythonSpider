from selectors import DefaultSelector,EVENT_WRITE

urls_todo = set(['/'])
seen_urls = set(['/'])

concurrency_achieved = 0
selector = DefaultSelector()
stopped = False

class Fetcher:

	def __init__(self,url):
		self.response = b''
		self.url = url
		self.sock = None

	def fetch(self):
		global concurrency_achieved
		concurrency_achieved = max(concurrency_achieved,len(urls_todo))

		self.sock = socket.socket()
		self.sock.setblocking(False)
		try:
			self.sock.connect(('xkcd.com',80))
		except BlockingIOError:
			pass
		selector.register(self.sock.fileno(),EVENT_WRITE,self.connected)





