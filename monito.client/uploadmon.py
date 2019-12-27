import commands
import sys,urllib,urllib2
import  re

secid='5toRb5lCdEU2q5H'
serverip="192.168.10.92"
serverip2=""
#serverip2="119.254.98.237"
port="18000"
monroot="./"
NETWORK="192.168.10"
#(status,ETH) = commands.getstatusoutput('($(which ip) a||/sbin/ip a)|grep ' + NETWORK +' |sed \'s/noprefixroute//\'|awk \'{print $7}\'|grep -v "lo:"|head -n 1')
(status,ETH) = commands.getstatusoutput('/sbin/ip a|grep ' + NETWORK +' |sed \'s/noprefixroute//\'|awk \'{print $7}\'|grep -v "lo:"|head -n 1')
print("eth:"+ETH)

def GetIp():
	(status,system)  = commands.getstatusoutput('uname -a')
	if system.find('FreeBSD') != -1 :
		#(status,mac) = commands.getstatusoutput('ifconfig |grep ether|awk \'{print $2}\'')
		(status,ip) = commands.getstatusoutput("ifconfig em0| egrep 'inet[^0-9].*' | grep -v '127.0.0.1' | awk '{print $2,$4}'")
		(ip,netmask)=ip.split()
		print status,ip
		print ip,netmask
	elif system.find('Linux') != -1 :	
		#example: take internal ip addr
		(status,ip) = commands.getstatusoutput("ifconfig "+ETH+"| egrep 'inet[^0-9].*' | grep -v '127.0.0.1' | awk '{print $2,$4}'|sed -e 's/addr://' -e 's/Mask://'")
		(ip,netmask)=ip.split()
		print status,ip
		print ip,netmask
		#example: obtain external network IP addr
		if ip.find('10.') !=-1  and  ip.find('192.168.') ==-1 and ip.find('172.16') ==-1 :
			(status,ip) = commands.getstatusoutput('/usr/bin/curl  whatismyip.akamai.com')
			if status != 0 :
				(status,ip) = commands.getstatusoutput('/usr/bin/curl  whatismyip.akamai.com')
			if status != 0 :
				(status,ip) = commands.getstatusoutput('/usr/bin/wget -qO - ifconfig.co')
			ip =  ip.split('\n')[-1]
	return ip,netmask

#upload portinfo (self's port process message)
class WebForm3(): 
	url_login="http://"+serverip+":"+port 
	if serverip2 != "" :
		url_login2="http://"+serverip2+":"+port 	
	secidd=secid
	typename='portinfo'
	(status,hostname) = commands.getstatusoutput('hostname')
	print status,hostname
	(status,ports)    = commands.getstatusoutput("netstat -anp|grep LISTEN|grep -v unix|sed -e 's/:::/:/g'|awk '{print $4\",\"$7}'|awk -F':' '{print $2}'|sed -e 's/\\.\\///g' -e 's/\\//,/g'|sort |uniq|awk -F',' '{printf \"%s:%s;\",$1,$3}'")
	(ip,netmask)=GetIp()
	
	the_page = '' 
	def login3(self): 
		values = {
		'secid' : self.secidd,
		'type'  : self.typename,
		'hostname' : self.hostname, 
		'ip' : self.ip, 
		'ports'  : self.ports,
		} 
		print values
		print self.url_login
		postdata = urllib.urlencode(values) 
		req = urllib2.Request(self.url_login, postdata) 
		response = urllib2.urlopen(req)
		self.the_page = response.read()
		if serverip2 != "" :
			print "server2 uploading..."
			req = urllib2.Request(self.url_login, postdata) 
			response = urllib2.urlopen(req)
			self.the_page = response.read()			
		#print self.the_page

#upload moninfo (self's monitor message)
class WebForm2(): 
	url_login="http://"+serverip+":"+port
	if serverip2 != "" :
		url_login2="http://"+serverip2+":"+port	 
	secidd=secid
	typename='moninfo'
	(status,hostname) = commands.getstatusoutput('hostname')
	print status,hostname
	(status,storage) = commands.getstatusoutput("df -h |grep -w '/'|awk '{print $5}'")
	(status,net) = commands.getstatusoutput("tail -n 1 ./nettrafic.log|awk '{print $1,$4,$6}'")
	(ip,netmask)=GetIp()
	(status,system) = commands.getstatusoutput('uname -a')
        if system.find('FreeBSD') != -1 :
                (status,cpu) = commands.getstatusoutput("top -d 2 |grep CPU:|awk -F',' '{print $5}'")
                (status,memory) = commands.getstatusoutput("top -d 1|grep Mem:|awk -F, '{print $6}'")
        elif system.find('Linux') != -1 :
                (status,cpu) = commands.getstatusoutput("top -bn1 |grep Cpu|grep -v grep|awk -F',' '{print $4\"%\"}'|sed 's/id//g'|sed 's/%%/%/g'|sed 's/ //g'")
                #For ubuntu linux memory:
                if system.find('Ubuntu') != -1 :
                        (status,memory) = commands.getstatusoutput("top -bn1|grep Mem|awk -F',' '{print $1,$3}'|sed 's/k//g'|awk '{printf \"%.1fM/%.1fM\\n\",$2/1024,$4/1024}'")
                else :
                        (status,memory) = commands.getstatusoutput("top -bn1 |grep 'Mem'|grep -v grep|grep -v Swap|awk -F',' '{print $1,$2}'|awk '{printf \"%.1fM/%.1fM\\n\",$4/1024,$6/1024}'")
                (status,swap) = commands.getstatusoutput("top -bn1 |grep 'Swap'|grep -v grep|awk -F',' '{print $1,$2}'")

	the_page = '' 
	def login2(self): 
		values = {
		'secid' : self.secidd,
		'type'  : self.typename,
		'hostname' : self.hostname, 
		'ip' : self.ip, 
		'cpu' : self.cpu,
		'memory' : self.memory,
		'storage' : self.storage,
		'net' : self.net,
		} 
		print values
		print self.url_login
		postdata = urllib.urlencode(values) 
		req = urllib2.Request(self.url_login, postdata) 
		response = urllib2.urlopen(req)
		self.the_page = response.read()
		if serverip2 != '' :
			print "server2 uploading..."			
			req = urllib2.Request(self.url_login, postdata) 
			response = urllib2.urlopen(req)
			self.the_page = response.read()		
		#print self.the_page

#upload baseinfo (self's configure)
class WebForm(): 
	url_login="http://"+serverip+":"+port 
	if serverip2 != "" :
		url_login2="http://"+serverip2+":"+port	
	secidd=secid
	typename='baseinfo'
	(status,hostname) = commands.getstatusoutput('hostname')
	print status,hostname
	(status,tz) = commands.getstatusoutput('tail -n 1 /etc/localtime')
	(status,storage) = commands.getstatusoutput("df -h |grep '^/dev/'|awk '{print $2,$5}'| tr '\n' ':' ")
	(status,username) = commands.getstatusoutput('whoami')
	(status,system) = commands.getstatusoutput('uname -ro')
	(ip,netmask)=GetIp()
       	if system.find('FreeBSD') != -1 :
		(status,cpu) = commands.getstatusoutput("dmesg|grep CPU:|awk '{print $2$3,$4,$6$7$8}'| tr '\n' ':'' ")
		(status,memory) = commands.getstatusoutput("dmesg|grep 'real memory'|tr '=' ':'|awk '{print $1,$2$5$6}'")
		(status,mac) = commands.getstatusoutput("ifconfig em0|grep ether|awk '{print $2}'")
	elif system.find('Linux') != -1 :	
		(status,cpu) = commands.getstatusoutput("cat /proc/cpuinfo |grep 'model name'|awk -F':' '{print $2}'| uniq -c")
		(status,memory) = commands.getstatusoutput('cat /proc/meminfo |grep MemTotal')
		(status,mac) = commands.getstatusoutput("ifconfig "+ETH+" |grep ether|awk '{print $2}'")
		#example: take internal ip addr


	the_page = '' 
	def login(self): 
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
		} 
                print values
                print self.url_login
		postdata = urllib.urlencode(values) 
		req = urllib2.Request(self.url_login, postdata) 
		response = urllib2.urlopen(req)
		self.the_page = response.read()
		if serverip2 != "" :
			print "server2 uploading..."			
			req = urllib2.Request(self.url_login, postdata) 
			response = urllib2.urlopen(req)
			self.the_page = response.read()		
		#print self.the_page

#download pub key
class WebDownfile():
	url_down="http://"+serverip+":"+port+"/.ssh/id_rsa.pub?secid="+secid
	the_page=''
	def downfile(self):
		req = urllib2.Request(self.url_down) 
		response = urllib2.urlopen(req) 
		self.the_page = response.read()	
		print self.the_page
		f = open('.ssh/authorized_keys','a')
		f.write(self.the_page + '\n')

#download self's update
class WebDownfile2():
	url_down="http://"+serverip+":"+port+"/uploadmon.py?secid="+secid
	the_page=''
	def downfile2(self):
		req = urllib2.Request(self.url_down) 
		response = urllib2.urlopen(req) 
		self.the_page = response.read()	
		print self.the_page
		f = open(monroot+'uploadmon.py','w')
		f.write(self.the_page)

#download self IP's configure
class WebDownload():
	(status,system) = commands.getstatusoutput('uname -ro')
	if system.find('FreeBSD') != -1 :
		(status,ip) = commands.getstatusoutput("ifconfig em0 | egrep 'inet[^0-9].*' | grep -v '127.0.0.1' | awk '{print $2,$4}'")
		(ip,netmask)=ip.split()
	elif system.find('Linux') != -1 :
		#example: obtain external network IP addr
		(status,ip) = commands.getstatusoutput('curl  ip.6655.com/ip.aspx')
		ip =  ip.split('\n')[-1]
		
	print 'ip:'+ip	
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
3. python uploadmon.py dwselfinfo ----download self info;
4. python uploadmon.py upmoninfo  ----upload monitor message;
5. python uploadmon.py selfupdate ----update by self;
5. python uploadmon.py upportinfo ----upload portinfo message;
'''
if len(sys.argv) == 2:
	if sys.argv[1] == 'upbaseinfo':
		web=WebForm()
		web.login()
	if sys.argv[1] == 'upmoninfo':
		web=WebForm2()
		web.login2()		
	if sys.argv[1] == 'upportinfo':
		web=WebForm3()
		web.login3()	
	if sys.argv[1] == 'downkey':
		downloadfile = WebDownfile()
		downloadfile.downfile()
	if sys.argv[1] == 'dwselfinfo':
		downresource = WebDownload()
		downresource.download()	
	if sys.argv[1] == 'selfupdate':
		downloadfile = WebDownfile2()
		downloadfile.downfile2()
else: print help
