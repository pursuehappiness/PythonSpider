import urllib.request
#from sgmllib import SGMLParser
#
#class ListName(SGMLParser):
#
#	def __init__(self):
#		SGMLParser.__init__(self)
#		self.is_h4 = ""  
#		self.name = []
#	def start_h4(self, attrs):
#		self.is_h4 = 1
#	def end_h4(self):  
#		self.is_h4 = ""  
#	def handle_data(self, text):  
#		if self.is_h4 == 1:  
#			self.name.append(text)  

if __name__ == '__main__':
    response = urllib.request.urlopen('http://www.baidu.com')  
    content = response.read()
    print(content.decode('gbk','ignore').encode('utf-8'))
    #listname = ListName()  
    #listname.feed(content)  
    #for item in listname.name:  
    #    print(item.decode('gbk').encode('utf8'))



