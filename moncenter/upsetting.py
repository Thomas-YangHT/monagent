import commands
import sys,urllib,urllib2
import MySQLdb
import  re
import json

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

def readMysql(SQL):
	try:
		conn=MySQLdb.connect(host=MYHOST,user=MYUSER,passwd=MYPWD,db='monitor',port=3306,charset='utf8')
		cur=conn.cursor()
		cur.execute("SET NAMES gbk");
		sql=SQL
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
	return result


#upload baksetting message
class UpSetting(): 
	url_login="http://"+serverip+":"+port 
	the_page = '' 
	def up(self,typename,result): 
		values = {
		'secid' : secid,
		'type'  : typename,
		'setting' : result, 
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
1. python upsetting.py bak   ----upload bak setting;
2. python upsetting.py label ----upload label setting;
'''
if len(sys.argv) == 2:
	if sys.argv[1] == 'bak':
		typename='baksetting'
		sql=("select ip,baktype,baknames,bakpolicy from baksetting")
		result=readMysql(sql)
		web=UpSetting()
		web.upbak(typename,result)
	if sys.argv[1] == 'label':
		typename='labelset'
		sql=("select ip,label from baseinfo where label is not null")
		result=readMysql(sql)
		web=UpSetting()
		web.up(typename,result)
else: print help