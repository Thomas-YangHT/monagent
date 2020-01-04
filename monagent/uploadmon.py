import commands
import sys,urllib,urllib2
import re

secid='5toRb5lCdEU2q5H'
serverip="192.168.10.92"
serverip2=""
port="18000"
monroot="./"
NETWORK="192.168.10"
#(status,ETH) = commands.getstatusoutput('/sbin/ip a|grep ' + NETWORK +' |sed \'s/noprefixroute//\'|awk \'{print $7}\'|grep -v "lo:"|head -n 1')
#print("eth:"+ETH)
def Sys():
	(status,system)  = commands.getstatusoutput('uname -ro')
	return system

def Tz():
	(status,tz) = commands.getstatusoutput('tail -n 1 /etc/localtime')
	return tz

def Hostname():
	(status,hostname) = commands.getstatusoutput('hostname')
	return hostname

def UserName():
	(status,username) = commands.getstatusoutput('whoami')
	return UserName

def Storage():
	(status,storage) = commands.getstatusoutput("df -h |grep '^/dev/'|awk '{print $2,$5}'| tr '\n' ':' ")
	return storage

def Cpu(system):
	cpu=''	
	if system.find('FreeBSD') != -1 :
		(status,cpu) = commands.getstatusoutput("dmesg|grep CPU:|awk '{print $2$3,$4,$6$7$8}'| tr '\n' ':'' ")
	elif system.find('Linux') != -1 :	
		(status,cpu) = commands.getstatusoutput("cat /proc/cpuinfo |grep 'model name'|awk -F':' '{print $2}'| uniq -c")
	return cpu

def Memory(system):
	memory=''
	if system.find('FreeBSD') != -1 :
		(status,memory) = commands.getstatusoutput("dmesg|grep 'real memory'|tr '=' ':'|awk '{print $1,$2$5$6}'")
	elif system.find('Linux') != -1 :	
		(status,memory) = commands.getstatusoutput('cat /proc/meminfo |grep MemTotal')
	return memory

def Mac(system):
	mac=''
	ETH=Eth()
	if system.find('FreeBSD') != -1 :
		(status,mac) = commands.getstatusoutput("ifconfig em0|grep ether|awk '{print $2}'")
	elif system.find('Linux') != -1 :	
		(status,mac) = commands.getstatusoutput("(ifconfig "+ETH+" |grep ether||ifconfig "+ETH+" |grep HWaddr)|grep -Po '..:..:..:..:..:..'")
	return mac

def Eth():
	(status,ETH) = commands.getstatusoutput('/sbin/ip a|grep ' + NETWORK +' |sed \'s/noprefixroute//\'|awk \'{print $7}\'|grep -v "lo:"|head -n 1')
	return ETH

def GetIp():
	system=Sys()
	ETH=Eth()
	ip=''
	netmask=""
	if system.find('FreeBSD') != -1 :
		#(status,mac) = commands.getstatusoutput('ifconfig |grep ether|awk \'{print $2}\'')
		(status,ip) = commands.getstatusoutput("ifconfig em0| egrep 'inet[^0-9].*' | grep -v '127.0.0.1' | awk '{print $2,$4}'")
		(ip,netmask)=ip.split()
		#print status,ip
		#print ip,netmask
	elif system.find('Linux') != -1 :	
		#example: take internal ip addr
		(status,ip) = commands.getstatusoutput("/sbin/ifconfig "+ETH+"| egrep 'inet[^0-9].*' | grep -v '127.0.0.1' | awk '{print $2,$4}'|sed -e 's/addr://' -e 's/Mask://'")
		(ip,netmask)=ip.split()
		#print status,ip
		#print ip,netmask
	return ip,netmask

def ExtIp():
	#example: obtain external network IP addr
	ETH=Eth()
	(status,ip) = commands.getstatusoutput("/sbin/ifconfig "+ETH+"| egrep 'inet[^0-9].*' | grep -v '127.0.0.1' | awk '{print $2,$4}'|sed -e 's/addr://' -e 's/Mask://'")
	(ip,netmask)=ip.split()
	if ip.find('10.') !=-1  and  ip.find('192.168.') ==-1 and ip.find('172.16') ==-1 :
		(status,ip) = commands.getstatusoutput('/usr/bin/curl  whatismyip.akamai.com')
		if status != 0 :
			(status,ip) = commands.getstatusoutput('/usr/bin/curl  whatismyip.akamai.com')
		if status != 0 :
			(status,ip) = commands.getstatusoutput('/usr/bin/wget -qO - ifconfig.co')
		ip =  ip.split('\n')[-1]
		return ip

def Ports():
	(status,ports)    = commands.getstatusoutput("sudo netstat -anp|grep LISTEN|grep -v unix|sed -e 's/:::/:/g'|awk '{print $4\",\"$7}'|awk -F':' '{print $2}'|sed -e 's/\\.\\///g' -e 's/\\//,/g'|sort |uniq|awk -F',' '{printf \"%s:%s;\",$1,$3}'")
	return ports

def RootUsage():
	(status,rootusage) = commands.getstatusoutput("df -h /|grep -w '/'|awk '{print $(NF-1)}'")
	return rootusage

def Net():
	(status,net) = commands.getstatusoutput("cd /$HOME/monagent.client && tail -n 1 ./nettrafic.log|awk '{print $1,$4,$6}'")
	return net

def CpuIdle(system):
	cpu=''
	if system.find('FreeBSD') != -1 :
		(status,cpu) = commands.getstatusoutput("top -d 2 |grep CPU:|awk -F',' '{print $5}'")
		(status,memory) = commands.getstatusoutput("top -d 1|grep Mem:|awk -F, '{print $6}'")
	elif system.find('Linux') != -1 :
		(status,cpu) = commands.getstatusoutput("top -bn1 |grep Cpu|grep -v grep|awk -F',' '{print $4\"%\"}'|sed 's/id//g'|sed 's/%%/%/g'|sed 's/ //g'")
	return cpu

def MemUsed(system):
	#For ubuntu linux memory:
	if system.find('Ubuntu') != -1 :
		(status,memory) = commands.getstatusoutput("top -bn1|grep Mem|awk -F',' '{print $1,$3}'|sed 's/k//g'|awk '{printf \"%.1fM/%.1fM\\n\",$2/1024,$4/1024}'")
	else :
		(status,memory) = commands.getstatusoutput("top -bn1 |grep 'Mem'|grep -v grep|grep -v Swap|awk -F',' '{print $1,$2}'|awk '{printf \"%.1fM/%.1fM\\n\",$4/1024,$6/1024}'")
		(status,swap) = commands.getstatusoutput("top -bn1 |grep 'Swap'|grep -v grep|awk -F',' '{print $1,$2}'")
	return memory

#upload portinfo (self's port process message)
class PortInfo(): 
	url_Upload="http://"+serverip+":"+port 
	if serverip2 != "" :
		url_Upload="http://"+serverip2+":"+port 	
	secidd=secid
	typename='portinfo'
	hostname=Hostname()
	(ip,netmask)=GetIp()
	ports=Ports()
	the_page = '' 
	def Upload(self): 
		values = {
		'secid' : self.secidd,
		'type'  : self.typename,
		'hostname' : self.hostname, 
		'ip' : self.ip, 
		'ports'  : self.ports,
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
		#print self.the_page

#upload moninfo (self's monitor message)
class MonInfo(): 
	url_Upload="http://"+serverip+":"+port
	if serverip2 != "" :
		url_Upload="http://"+serverip2+":"+port	 
	secidd=secid
	typename='moninfo'
	system=''
	system=Sys()
	hostname=Hostname()
	(ip,netmask)=GetIp()
	cpuidle=CpuIdle(system)
	memused=MemUsed(system)
	rootusage=RootUsage()
	net=Net()
	the_page = '' 
	def Upload(self): 
		values = {
		'secid' : self.secidd,
		'type'  : self.typename,
		'hostname' : self.hostname, 
		'ip' : self.ip, 
		'cpuidle' : self.cpuidle,
		'memused' : self.memused,
		'rootusage' : self.rootusage,
		'net' : self.net,
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
		#print self.the_page

#upload baseinfo (self's configure)
class BaseInfo(): 
	url_Upload="http://"+serverip+":"+port 
	if serverip2 != "" :
		url_Upload="http://"+serverip2+":"+port	
	secidd=secid
	typename='baseinfo'
	cpu=''
	system=Sys()
	hostname=Hostname()
	tz=Tz()	
	username=UserName()
	storage=Storage()
	(ip,netmask)=GetIp()
	cpu=Cpu(system)
	memory=Memory(system)
	mac=Mac(system)

	the_page = '' 
	def Upload(self): 
		values = {
		'secid' : self.secidd,
		'type'  : self.typename,
		'hostname' : self.hostname, 
		'ip' : self.ip, 
		'system' : self.system,
		'cpu' : self.cpu,
		'memory' : self.memory,
		'storage' : self.storage,
		'timezone' : self.tz,
		'username' : self.username,
		'mac': self.mac,
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
		#print self.the_page

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
	if sys.argv[1] == 'upmoninfo':
		web=MonInfo()
		web.Upload()		
	if sys.argv[1] == 'upportinfo':
		web=PortInfo()
		web.Upload()	
	if sys.argv[1] == 'downkey':
		dw = DownKey()
		dw.downfile()
	if sys.argv[1] == 'dwselfinfo':
		dw = AutoBackup()
		dw.download()	
	if sys.argv[1] == 'selfupdate':
		dw = DownKey2()
		dw.downfile2()
else: print help
