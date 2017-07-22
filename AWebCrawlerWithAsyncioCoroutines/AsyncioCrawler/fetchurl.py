#new start

#using thread

from queue import Queue 
from threading import Lock,Thread 
import urllib.parse
import socket
import re
import time

seen_urls = set(['/'])
lock = Lock()
idlethreadnum = 0

class Fethcher(Thread):
	def __init__(self,tasks,name):
		Thread.__init__(self)
		self.tasks = tasks
		self.deamon = True
		#self.idlethreadnum = 0
		self.name = name
		self.start()

	def run(self):
		global idlethreadnum
		while True:
			
			url = self.tasks.get()
			print(url)
			sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			try:
				sock.connect(('xkcd.com',80))
			except:
				print('connect error happend')

			get = 'Get {} HTTP/1.0\r\nHost: localhost\r\n\r\n'.format(url)
			sock.send(get.encode('ascii'))
			response = b''
			chunk = sock.recv(4096)

			while chunk:
				response += chunk
				chunk = sock.recv(4096)

			print('response:',response)
			links = self.parse_links(url,response)

			lock.acquire()
			for link in links.difference(seen_urls):
				self.tasks.put(link)
			seen_urls.update(links)
			lock.release()

			self.tasks.task_done()
		self.tasks.task_done()
		print("exit run func")

	def parse_links(self,fetched_url,response):
		if not response:
			print('error: {}'.format(fetched_url))
			return set()

		if not self._is_html(response):
			return set()

		urls = set(re.findall(r'''(?i)href=["']?([^\s"'<>]+)''',
			self.body(response)))

		links = set()

		for url in urls:
			normalized = urllib.parse.urljoin(fetched_url,url)
			parts = urllib.parse.urlparse(normalized)
			if parts.scheme not in ('','http','https'):
				continue
			host,port = urllib.parse.splitport(parts.netloc)
			if host and host.lower() not in ('localhost'):
				continue
			defragmented,frag = urllib.parse.urldefrag(parts.path)
			links.add(defragmented)

		return links

	def body(self,response):
		body = response.split(b'\r\n\r\n',1)[1]
		return body.decode('utf-8')

	def _is_html(self,response):
		head,body = response.split(b'\r\n\r\n',1)
		headers = dict(h.split(': ') for h in head.decode().split('\r\n')[1:])
		return headers.get('Content-Type','').startswith('text/html')

class ThreadPool:
	"""docstring for ThreadPool"""
	def __init__(self, num_thread):
		self.tasks = Queue()
		for _ in range(num_thread):
			Fethcher(self.tasks,_)

	def add_task(self,url):
		self.tasks.put(url)

	def wait_completion(self):
		self.tasks.join()

if __name__ == '__main__':
	#pass

	start = time.time()
	print('start time',start)
	pool = ThreadPool(4)
	print('created thread pool')
	pool.add_task("/")
	print('add task')
	pool.wait_completion()
	print('thread complete')
	print('{} URLs fetched in {:.1f} seconds'.format(len(seen_urls),time.time() - start))
			












