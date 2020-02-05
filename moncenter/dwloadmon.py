#Download  info  from monagent, and save to mysqlDB
import json
import commands
import MySQLdb
import sys,urllib,urllib2
#modify these item to suit your monitor system:

monroot="."             #the directory of mysql server think
MYHOME='./'             #the directory used for sql "LOAD DATA LOCAL INFILE...", modified as .  no need mount 
f = open('./server8000.log','a')

def readConf():
    f = open('monitor.conf','r')
    content = f.read()
    f.close() 
    dicconf={}   
    dicconf=json.loads(content)
    return dicconf
dicconf={}
dicconf=readConf()
secid=dicconf['secid']
serverip=dicconf['serverip']
serverip2=dicconf['serverip2']
port=dicconf['port']
MYHOST=dicconf['MYHOST']
MYUSER=dicconf['MYUSER']
MYPWD=dicconf['MYPWD']

#download baseinfo
class BaseInfo():
	url_down="http://"+serverip+":"+port+"/baseinfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/baseinfo?secid="+secid
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
		f1 = open( MYHOME + 'baseinfo','wb')
		f1.write(self.the_page)
		f1.close()
		try:
			conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='monitor',port=3306,charset='utf8')
			cur=conn.cursor()
			#sql=("LOAD DATA LOW_PRIORITY INFILE '/root/baseinfo' REPLACE INTO TABLE `cmdb`.`basetmp` CHARACTER SET gbk FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\\n' (`hostname`, `ip`, `username`, `cpu`, `mem`, `storage`, `system`, `timezone`);")
			sql=("delete from monitor.basetmp")
			print sql
			count=cur.execute(sql)
			sql=("LOAD DATA LOCAL INFILE '"+monroot+"/baseinfo'  INTO TABLE monitor.basetmp  CHARACTER SET utf8  FIELDS TERMINATED BY ',' (`hostname`, `kernel`, `tz`, `mac`, `ip`, `cpu`, `memory`, `disk`, `seriesno`);")
			print sql
			count=cur.execute(sql)
			sql=("insert into monitor.baseinfo(`hostname`, `kernel`, `tz`, `mac`, `ip`, `cpu`, `memory`, `disk`, `seriesno`)  select  `hostname`, `kernel`, `tz`, `mac`, `ip`, `cpu`, `memory`, `disk`, `seriesno` from basetmp where ip not in (select ip from monitor.baseinfo)")
			print sql
			count=cur.execute(sql)			 
			(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
			f.write(datevalue + " loaddata from "+monroot+"/baseinfo\n")
			conn.commit()
			cur.close()
			conn.close()
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#download moninfo
class MonInfo():
	url_down="http://"+serverip+":"+port+"/moninfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/moninfo?secid="+secid
	the_page=''
	def downfile2(self):
		try:
			req = urllib2.Request(self.url_down) 
			response = urllib2.urlopen(req) 
		except urllib2.URLError,e:
			print e.reason
			req = urllib2.Request(self.url_down2) 
			response = urllib2.urlopen(req)
		self.the_page = response.read()	
		print self.the_page
		content = self.the_page
		try:
			f2 = open(MYHOME + 'moninfo','wb')
			f2.write(content)
			f2.close()
		finally:
			filewrited = 1
		if filewrited == 1:
			try:
				conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='monitor',port=3306,charset='utf8')
				cur=conn.cursor()
				sql=('delete from basemon where ip is null')
		   		print sql
				count=cur.execute(sql)			
			  	#sql=("LOAD DATA LOW_PRIORITY LOCAL INFILE '/root/moninfo' REPLACE INTO TABLE `moninfo`.`moninfo` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\\n' (`date`, `hostname`, `ip`, `cpu`, `mem`, `storage`, `net`);")
				sql=("LOAD DATA LOCAL INFILE '"+monroot+"/moninfo' INTO TABLE `basemon` FIELDS TERMINATED BY ','  (`timestamp`, `ip`, `cpuidle`, `memtotal`, `memused`, `rx`, `tx`, `diskrootrate`, `ioawait`, `ioutil`);")
				print sql
				count=cur.execute(sql)
				(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
			   	f.write(datevalue + " loaddata from "+monroot+"/moninfo\n")
				conn.commit()
				cur.close()
				conn.close()
			except MySQLdb.Error,e:
				print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#download portinfo
class PortInfo():
	url_down="http://"+serverip+":"+port+"/portinfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/portinfo?secid="+secid
	the_page=''
	def downfile3(self):
		try:
			req = urllib2.Request(self.url_down) 
			response = urllib2.urlopen(req) 
		except urllib2.URLError,e:
			print e.reason
			req = urllib2.Request(self.url_down2) 
			response = urllib2.urlopen(req)
		self.the_page = response.read()	
		print self.the_page
		content = self.the_page
		try:
			f2 = open(MYHOME + 'portinfo','wb')
			f2.write(content)
			f2.close()
		finally:
			filewrited = 1
		if filewrited == 1:
			try:
				conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='monitor',port=3306,charset='utf8')
				cur=conn.cursor()
				sql=('delete from ports')
		   		print sql
				count=cur.execute(sql)			
			  	#sql=("LOAD DATA LOW_PRIORITY LOCAL INFILE '/root/moninfo' REPLACE INTO TABLE `moninfo`.`moninfo` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\\n' (`date`, `hostname`, `ip`, `cpu`, `mem`, `storage`, `net`);")
				sql=("LOAD DATA LOCAL INFILE '"+monroot+"/portinfo' INTO TABLE `ports` FIELDS TERMINATED BY ','  (`timestamp`, `ip`, `protocol`, `ipl`, `port`, `pid`, `procname`);")
				print sql
				count=cur.execute(sql)
				(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
			   	f.write(datevalue + " loaddata from "+monroot+"/portinfo\n")
				conn.commit()
				cur.close()
				conn.close()
			except MySQLdb.Error,e:
				print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#download webinfo
class WebInfo():
	url_down="http://"+serverip+":"+port+"/webinfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/webinfo?secid="+secid
	the_page=''
	def downfile3(self):
		try:
			req = urllib2.Request(self.url_down) 
			response = urllib2.urlopen(req) 
		except urllib2.URLError,e:
			print e.reason
			req = urllib2.Request(self.url_down2) 
			response = urllib2.urlopen(req)
		self.the_page = response.read()	
		print self.the_page
		content = self.the_page
		try:
			f2 = open(MYHOME + 'webinfo','wb')
			f2.write(content)
			f2.close()
		finally:
			filewrited = 1
		if filewrited == 1:
			try:
				conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='monitor',port=3306,charset='utf8')
				cur=conn.cursor()
				sql=('delete from webinfo')
		   		print sql
				count=cur.execute(sql)			
			  	#sql=("LOAD DATA LOW_PRIORITY LOCAL INFILE '/root/moninfo' REPLACE INTO TABLE `moninfo`.`moninfo` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\\n' (`date`, `hostname`, `ip`, `cpu`, `mem`, `storage`, `net`);")
				sql=("LOAD DATA LOCAL INFILE '"+monroot+"/webinfo' INTO TABLE `webinfo` FIELDS TERMINATED BY ','  (`timestamp`, `ip`, `webname`, `num`, `content`, `class`);")
				print sql
				count=cur.execute(sql)
				(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
			   	f.write(datevalue + " loaddata from "+monroot+"/webinfo\n")
				conn.commit()
				cur.close()
				conn.close()
			except MySQLdb.Error,e:
				print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#download errinfo
class ErrInfo():
	url_down="http://"+serverip+":"+port+"/errinfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/errinfo?secid="+secid
	the_page=''
	def downfile3(self):
		try:
			req = urllib2.Request(self.url_down) 
			response = urllib2.urlopen(req) 
		except urllib2.URLError,e:
			print e.reason
			req = urllib2.Request(self.url_down2) 
			response = urllib2.urlopen(req)
		self.the_page = response.read()	
		print self.the_page
		content = self.the_page
		try:
			f2 = open(MYHOME + 'errinfo','wb')
			f2.write(content)
			f2.close()
		finally:
			filewrited = 1
		if filewrited == 1:
			try:
				conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='monitor',port=3306,charset='utf8')
				cur=conn.cursor()
				sql=('delete from errinfo')
		   		print sql
				count=cur.execute(sql)			
			  	#sql=("LOAD DATA LOW_PRIORITY LOCAL INFILE '/root/moninfo' REPLACE INTO TABLE `moninfo`.`moninfo` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\\n' (`date`, `hostname`, `ip`, `cpu`, `mem`, `storage`, `net`);")
				sql=("LOAD DATA LOCAL INFILE '"+monroot+"/errinfo' INTO TABLE `errinfo` FIELDS TERMINATED BY ','  (`timestamp`, `ip`, `errcontent`, `type`);")
				print sql
				count=cur.execute(sql)
				(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
			   	f.write(datevalue + " loaddata from "+monroot+"/errinfo\n")
				conn.commit()
				cur.close()
				conn.close()
			except MySQLdb.Error,e:
				print "Mysql Error %d: %s" % (e.args[0], e.args[1])

class K8sInfo():
	url_down="http://"+serverip+":"+port+"/k8sinfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/k8sinfo?secid="+secid
	the_page=''
	def downfile(self):
		try:
			req = urllib2.Request(self.url_down) 
			response = urllib2.urlopen(req) 
		except urllib2.URLError,e:
			print e.reason
			req = urllib2.Request(self.url_down2) 
			response = urllib2.urlopen(req)
		self.the_page = response.read()	
		print self.the_page
		content = self.the_page
		try:
			f2 = open(MYHOME + 'k8sinfo','wb')
			f2.write(content)
			f2.close()
		finally:
			filewrited = 1
		if filewrited == 1:
			try:
				conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='monitor',port=3306,charset='utf8')
				cur=conn.cursor()
				sql=('delete from k8sinfo')
		   		print sql
				count=cur.execute(sql)			
				sql=("LOAD DATA LOCAL INFILE '"+monroot+"/k8sinfo' INTO TABLE `k8sinfo` FIELDS TERMINATED BY ','  (`timestamp`, `ip`, `content`, `type`);")
				print sql
				count=cur.execute(sql)
				(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
			   	f.write(datevalue + " loaddata from "+monroot+"/k8sinfo\n")
				conn.commit()
				cur.close()
				conn.close()
			except MySQLdb.Error,e:
				print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#download bakinfo
class BakInfo():
	url_down="http://"+serverip+":"+port+"/bakinfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/bakinfo?secid="+secid
	the_page=''
	def downfile4(self):
		try:
			req = urllib2.Request(self.url_down) 
			response = urllib2.urlopen(req) 
		except urllib2.URLError,e:
			print e.reason
			req = urllib2.Request(self.url_down2) 
			response = urllib2.urlopen(req)
		self.the_page = response.read()	
		print self.the_page
		content = self.the_page
		try:
			f2 = open(MYHOME + 'bakinfo','wb')
			f2.write(content)
			f2.close()
		finally:
			filewrited = 1
		if filewrited == 1:
			try:
				conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='moninfo',port=3306,charset='utf8')
				cur=conn.cursor()
				sql=('delete from moninfo.bakinfo')
		   		print sql
				count=cur.execute(sql)			
			  	#sql=("LOAD DATA LOW_PRIORITY LOCAL INFILE '/root/moninfo' REPLACE INTO TABLE `moninfo`.`moninfo` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\\n' (`date`, `hostname`, `ip`, `cpu`, `mem`, `storage`, `net`);")
				sql=("LOAD DATA LOCAL INFILE '"+monroot+"/bakinfo' INTO TABLE `bakinfo` FIELDS TERMINATED BY ','  (`date`, `ip`, `filename`, `count`,`space`);")
				print sql
				count=cur.execute(sql)
				(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
			   	f.write(datevalue + " loaddata from "+monroot+"/bakinfo\n")
				conn.commit()
				cur.close()
				conn.close()
			except MySQLdb.Error,e:
				print "Mysql Error %d: %s" % (e.args[0], e.args[1])

help='''
1. python dwloadmon.py dwbaseinfo	 ----download baseinfo;
2. python dwloadmon.py dwmoninfo	 ----download recently moninfo;
3. python dwloadmon.py dwportinfo	 ----download recently portinfo;
4. python dwloadmon.py dwbakinfo	 ----download recently bakinfo;
5. python dwloadmon.py dwwebinfo	 ----download recently webinfo;
6. python dwloadmon.py dwerrinfo	 ----download recently errinfo;
7. python dwloadmon.py dwk8sinfo	 ----download recently k8sinfo;
'''

if len(sys.argv) == 2:
	if sys.argv[1] == 'dwbaseinfo':
		dw = BaseInfo()
		dw.downfile()
	elif sys.argv[1] == 'dwmoninfo':
		dw = MonInfo()
		dw.downfile2()
	elif sys.argv[1] == 'dwportinfo':
		dw = PortInfo()
		dw.downfile3()
	elif sys.argv[1] == 'dwwebinfo':
		dw = WebInfo() 
		dw.downfile3()
	elif sys.argv[1] == 'dwerrinfo':
		dw = ErrInfo() 
		dw.downfile3()
	elif sys.argv[1] == 'dwk8sinfo':
		dw = K8sInfo() 
		dw.downfile()
	elif sys.argv[1] == 'dwbakinfo':
		dw = BakInfo()
		dw.downfile4()
	else: print help
else: print help
