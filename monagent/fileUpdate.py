import commands
import sys,urllib,urllib2
import  re

secid='5toRb5lCdEU2q5H'
serverip="192.168.10.92"
serverip2=""
port="18000"
(status,who) = commands.getstatusoutput('whoami')
if who=='root':
	whodir = '/' + who
else:
	whodir = '/home/' + who
monroot = whodir + "/monagent.client/"

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
	dw=	WebDownfile('md5.txt')
	dw.downfile()
	(status,lmd5) = commands.getstatusoutput("md5sum " +sys.argv[1]+ " |awk '{print $1}'")
	(status,rmd5) = commands.getstatusoutput("grep "+sys.argv[1]+" md5.txt|awk '{print $1}'")
	if lmd5 != rmd5 :
		downloadfile = WebDownfile(sys.argv[1])
		downloadfile.downfile()
else: print help
