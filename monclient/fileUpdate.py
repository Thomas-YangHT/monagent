import commands
import sys,urllib,urllib2
import  re

secid='5toRb5lCdEU2q5H'
serverip="192.168.10.92"
serverip2=""
port="18000"
monroot="/home/xwx/monagent.client/"

#download self's update
class WebDownfile():
	def __init__( self, filename ):
		self.filename = filename
		self.url_down="http://"+serverip+":"+port+"/"+self.filename+"?secid="+secid
		self.url_down2="http://"+serverip2+":"+port+"/"+self.filename+"?secid="+secid	
	the_page=''
	def downfile(self):
		try:
			req = urllib2.Request(self.url_down) 
			response = urllib2.urlopen(req)
			self.the_page = response.read() 
		except urllib2.URLError,e:
			print e.reason
			req = urllib2.Request(self.url_down2) 
			response = urllib2.urlopen(req)
			self.the_page = response.read()			
		print self.the_page
		f = open(monroot + self.filename,'w')
		f.write(self.the_page)

help='''
1. python fileUpdate.py <filename> ----exp: uploadmon.py  ;
'''
if len(sys.argv) == 2:
	#if sys.argv[1] == 'uploadmon.py':
	downloadfile = WebDownfile(sys.argv[1])
	downloadfile.downfile()
else: print help
