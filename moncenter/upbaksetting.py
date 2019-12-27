import commands
import sys,urllib,urllib2
import MySQLdb
import  re

secid='5toRb5lCdEU2q5H'
serverip="119.254.98.237"
port="18000"
f = open('/root/server8000.log','a')

#upload baksetting message
class UpSetting(): 
	url_login="http://"+serverip+":"+port 
	secidd=secid
	typename='baksetting'

	try:
		conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='moninfo',port=3306,charset='utf8')
		cur=conn.cursor()
		cur.execute("SET NAMES gbk");
		sql=("select ip,baktype,baknames,bakpolicy from baksetting")
		print sql
		count=cur.execute(sql)
		if count != 0 :
			#result = cur.fetchall()
			result = ''
			for i in cur.fetchall() :
				for x in i :
					print type(x)
					result += str(x)+','
					print "x:",str(x)
			#result=result.strip()
			result=result.replace('\r','').replace('\\N','none')
			print "result:\n",result
		(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
		f.write(datevalue + " upbaksetting to agent\n")
		conn.commit()
		cur.close()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])

	the_page = '' 
	def upbak(self): 
		values = {
		'secid' : self.secidd,
		'type'  : self.typename,
		'baksetting' : self.result, 
		'exit'  : 'exit'
		} 
		print values
		print self.url_login
		postdata = urllib.urlencode(values) 
		req = urllib2.Request(self.url_login, postdata) 
		response = urllib2.urlopen(req)
		self.the_page = response.read()
		#print self.the_page

help='''
1. python upbaksetting.py up ----upload local sys message;
'''
if len(sys.argv) == 2:
	if sys.argv[1] == 'up':
		web=UpSetting()
		web.upbak()
else: print help