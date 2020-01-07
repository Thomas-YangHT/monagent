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
class WebDownfile():
	url_down="http://"+serverip+":"+port+"/dwbaseinfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/dwbaseinfo?secid="+secid
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
			conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='cmdb',port=3306,charset='utf8')
			cur=conn.cursor()
			#sql=("LOAD DATA LOW_PRIORITY INFILE '/root/baseinfo' REPLACE INTO TABLE `cmdb`.`basetmp` CHARACTER SET gbk FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\\n' (`hostname`, `ip`, `username`, `cpu`, `mem`, `storage`, `system`, `timezone`);")
			sql=("delete from cmdb.basetmp")
			print sql
			count=cur.execute(sql)
			sql=("LOAD DATA LOCAL INFILE '"+monroot+"/baseinfo'  INTO TABLE basetmp  CHARACTER SET utf8  FIELDS TERMINATED BY ',' (`hostname`, `ip`, `system`, `cpu`, `mem`, `storage`, `timezone`,`username`,`mac`);")
			print sql
			count=cur.execute(sql)
			sql=("insert into base(`hostname`, `ip`, `username`, `cpu`, `mem`, `storage`, `system`, `timezone`)  select  `hostname`, `ip`, `username`, `cpu`, `mem`, `storage`, `system`, `timezone` from basetmp where ip not in (select ip from base)")
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
class WebDownfile2():
	url_down="http://"+serverip+":"+port+"/dwmoninfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/dwmoninfo?secid="+secid
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
				conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='moninfo',port=3306,charset='utf8')
				cur=conn.cursor()
				sql=('delete from moninfo.moninfo')
		   		print sql
				count=cur.execute(sql)			
			  	#sql=("LOAD DATA LOW_PRIORITY LOCAL INFILE '/root/moninfo' REPLACE INTO TABLE `moninfo`.`moninfo` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\\n' (`date`, `hostname`, `ip`, `cpu`, `mem`, `storage`, `net`);")
				sql=("LOAD DATA LOCAL INFILE '"+monroot+"/moninfo' INTO TABLE `moninfo` FIELDS TERMINATED BY ','  (`date`, `hostname`, `ip`, `cpu`, `mem`, `storage`, `net`);")
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
class WebDownfile3():
	url_down="http://"+serverip+":"+port+"/dwportinfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/dwportinfo?secid="+secid
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
				conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='moninfo',port=3306,charset='utf8')
				cur=conn.cursor()
				sql=('delete from moninfo.portinfo')
		   		print sql
				count=cur.execute(sql)			
			  	#sql=("LOAD DATA LOW_PRIORITY LOCAL INFILE '/root/moninfo' REPLACE INTO TABLE `moninfo`.`moninfo` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"' ESCAPED BY '\"' LINES TERMINATED BY '\\n' (`date`, `hostname`, `ip`, `cpu`, `mem`, `storage`, `net`);")
				sql=("LOAD DATA LOCAL INFILE '"+monroot+"/portinfo' INTO TABLE `portinfo` FIELDS TERMINATED BY ','  (`date`, `hostname`, `ip`, `port`);")
				print sql
				count=cur.execute(sql)
				(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
			   	f.write(datevalue + " loaddata from "+monroot+"/portinfo\n")
				conn.commit()
				cur.close()
				conn.close()
			except MySQLdb.Error,e:
				print "Mysql Error %d: %s" % (e.args[0], e.args[1])

#download bakinfo
class WebDownfile4():
	url_down="http://"+serverip+":"+port+"/dwbakinfo?secid="+secid
	url_down2="http://"+serverip2+":"+port+"/dwbakinfo?secid="+secid
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
1. python stepone_reghost.py dwbaseinfo	 ----download baseinfo;
2. python stepone_reghost.py dwmoninfo	 ----download recently moninfo;
3. python stepone_reghost.py dwportinfo	 ----download recently portinfo;
4. python stepone_reghost.py dwbakinfo	 ----download recently bakinfo;
'''

if len(sys.argv) == 2:
	if sys.argv[1] == 'dwbaseinfo':
		downloadfile = WebDownfile()
		downloadfile.downfile()
	if sys.argv[1] == 'dwmoninfo':
		downloadfile = WebDownfile2()
		downloadfile.downfile2()
	if sys.argv[1] == 'dwportinfo':
		downloadfile = WebDownfile3()
		downloadfile.downfile3()
	if sys.argv[1] == 'dwbakinfo':
		downloadfile = WebDownfile4()
		downloadfile.downfile4()
else: print help
