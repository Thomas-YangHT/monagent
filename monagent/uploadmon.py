import commands
import sys,urllib,urllib2
import re

secid='5toRb5lCdEU2q5H'
serverip="192.168.10.92"
serverip2=""
port="18000"
monroot="./"
NETWORK="192.168.10"
ExecDir='~/monagent.client'

def baseInfo():
	(status,baseinfo) = commands.getstatusoutput("cd "+ExecDir+";bash collexec.sh baseinfo 2>>upload.err")
	return baseinfo

def monInfo():
	(status,moninfo) = commands.getstatusoutput("cd "+ExecDir+";bash collexec.sh moninfo 2>>upload.err")
	return moninfo

def portInfo():
	(status,portinfo) = commands.getstatusoutput("cd "+ExecDir+";bash collexec.sh portsinfo 2>>upload.err")
	return portinfo

def bakInfo():
	(status,bakinfo) = commands.getstatusoutput("cd "+ExecDir+";bash collexec.sh bakinfo 2>>upload.err")
	return bakinfo

def errInfo():
	(status,errinfo) = commands.getstatusoutput("cd "+ExecDir+";bash collexec.sh errinfo 2>>upload.err")
	return errinfo

#upload portinfo (self's port process message)
class PortInfo(): 
	url_Upload="http://"+serverip+":"+port 
	if serverip2 != "" :
		url_Upload="http://"+serverip2+":"+port 	
	secidd=secid
	typename='portinfo'
	#(ip,netmask)=GetIp()
	portinfo=portInfo()
	ip=portinfo.split(',')[1]
	the_page = '' 
	def Upload(self): 
		values = {
		'secid' : self.secidd,
		'type'  : self.typename,
		'portinfo'  : self.portinfo,
		'ip'    : self.ip, 
		} 
		print values
		print self.url_Upload
		postdata = urllib.urlencode(values) 
		req = urllib2.Request(self.url_Upload, postdata) 
		response = urllib2.urlopen(req,timeout=5)
		self.the_page = response.read()
		if serverip2 != "" :
			print "server2 uploading..."
			req = urllib2.Request(self.url_Upload, postdata) 
			response = urllib2.urlopen(req)
			self.the_page = response.read()			
		print self.the_page

#upload moninfo (self's monitor message)
class MonInfo(): 
	url_Upload="http://"+serverip+":"+port
	if serverip2 != "" :
		url_Upload="http://"+serverip2+":"+port	 
	secidd=secid
	typename='moninfo'
	moninfo=monInfo()
	#TIMESTAMP, IP, CPUIDLE, MEMTOTAL, MEMUSED, RX, TX, DISKROOTUSAGE, IOAWAIT, IOUTIL
	ip=moninfo.split(',')[1]
	the_page = '' 
	def Upload(self): 
		values = {
		'secid' : self.secidd,
		'type'  : self.typename,
		'moninfo' : self.moninfo,
		'ip' : self.ip,
		} 
		print values
		print self.url_Upload
		postdata = urllib.urlencode(values) 
		req = urllib2.Request(self.url_Upload, postdata) 
		response = urllib2.urlopen(req)
		self.the_page = response.read()
		if serverip2 != '' :
			print "server2 uploading..."			
			req = urllib2.Request(self.url_Upload, postdata) 
			response = urllib2.urlopen(req)
			self.the_page = response.read()		
		print self.the_page

#upload baseinfo (self's configure)
class BaseInfo(): 
	url_Upload="http://"+serverip+":"+port 
	if serverip2 != "" :
		url_Upload="http://"+serverip2+":"+port	
	secidd=secid
	typename='baseinfo'
	baseinfo=baseInfo()
	ip=baseinfo.split(',')[4]
    #echo $HOSTNAME, $KERNEL, $TZ, $MAC, $IP, $CPU, $MEMORY, $DISK, $SERIESNO
	the_page = '' 
	def Upload(self): 
		values = {
		'secid' : self.secidd,
		'type'  : self.typename,
		'baseinfo' : self.baseinfo,
		'ip' : self.ip,
		} 
		print values
		print self.url_Upload
		postdata = urllib.urlencode(values) 
		req = urllib2.Request(self.url_Upload, postdata) 
		response = urllib2.urlopen(req)
		self.the_page = response.read()
		if serverip2 != "" :
			print "server2 uploading..."			
			req = urllib2.Request(self.url_Upload, postdata) 
			response = urllib2.urlopen(req)
			self.the_page = response.read()		
		print self.the_page

#download pub key
class DownKey():
	url_down="http://"+serverip+":"+port+"/.ssh/id_rsa.pub?secid="+secid
	the_page=''
	def downfile(self):
		req = urllib2.Request(self.url_down) 
		response = urllib2.urlopen(req) 
		self.the_page = response.read()	
		print self.the_page
		f = open('.ssh/authorized_keys','a')
		f.write(self.the_page + '\n')


#download self IP's BACKUP configure
class AutoBackup():
	system=Sys()
	(ip,netmask)=GetIp()
		
	url_down='http://'+serverip+':'+port+'/downloadmessage?secid='+secid+'&download='+ip
	the_page=''
	def download(self):
		req = urllib2.Request(self.url_down) 
		response = urllib2.urlopen(req) 
		self.the_page = response.read()	
		print self.the_page
		res =self.the_page.split(';')
		if res[3]!='empty' and res[4]!='empty' and res[5]!='empty':
			if res[5]=='wget':
				(status,retmess) = commands.getstatusoutput('sudo wget -r -np -N -c -b -P '+res[4]+' '+'-o download.log'+' '+res[3])
				print status,retmess
			if res[5]=='axel':
				#example: axel -n 10 -o /tmp/	 http://soft.vpser.net/lnmp/lnmp0.7-full.tar.gz
				(status,retmess) = commands.getstatusoutput('sudo axel -m 10 -o '+res[4]+'  '+res[3])
				print status,retmess
			if res[5]=='rsync':
				#example: /usr/bin/rsync -vzrtopg --progress --delete hening@192.168.0.217::backup /home/backup --password-file=/etc/rsync.pas
				(status,retmess) = commands.getstatusoutput('sudo rsync -vzrtopg --progress --delete '+res[3]+' '+res[4]+'>>rsync.log')
				print status,retmess

		else:
			print res[3],res[4],res[5],"has empty value,exit"



help='''
1. python uploadmon.py upbaseinfo ----upload local sys message;
2. python uploadmon.py downkey	  ----download auth key;
3. python uploadmon.py dwselfinfo ----download self backup info;
4. python uploadmon.py upmoninfo  ----upload monitor message;
5. python uploadmon.py upportinfo ----upload portinfo message;
'''

if len(sys.argv) == 2:
	if sys.argv[1] == 'upbaseinfo':
		web=BaseInfo()
		web.Upload()
	elif sys.argv[1] == 'upmoninfo':
		web=MonInfo()
		web.Upload()		
	elif sys.argv[1] == 'upportinfo':
		web=PortInfo()
		web.Upload()	
	elif sys.argv[1] == 'downkey':
		dw = DownKey()
		dw.downfile()
	elif sys.argv[1] == 'dwselfinfo':
		dw = AutoBackup()
		dw.download()	
	elif sys.argv[1] == 'selfupdate':
		dw = DownKey2()
		dw.downfile2()
	else: print help
else: print help
