#coding=utf-8
#用作监控、备份、基础信息的上传和下载中转服务
#日志默认都写在了/root/log/下，待修改
# use TCPServer
import commands
import SocketServer
#from SocketServer import StreamRequestHandler as SRH
#import MySQLdb
import sys,urllib,urllib2
import time
reload(sys)
sys.setdefaultencoding('utf-8')

HOST = ''
PORT = 18000

text_content = '''Status: OK - 200
Date: Sun, 01 Jun 2008 12:35:47 GMT
Server: Apache/2.0.61 (Unix)
Last-Modified:Sun, 01 Jun 2008 12:35:30 GMT
Accept-Ranges:bytes
Content-Length:2000
Cache-Control:max-age=120
Expires:Sun, 01 Jun 2008 12:37:47 GMT
Content-Type:application/xml
Age:2
Connection:close

<!doctype html> 
<html>
<head>
<title>WOW</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<p>Upload Control Messages</p>
<form name="input" action="/" method="post">
secid:<input type="text" name="secid"><br>
hostname:<input type="text" name="hostname"><br>
ip:<input type="text" name="ip"><br>
system:<input type="text" name="system"><br>
cpu:<input type="text" name="cpu"><br>
memory:<input type="text" name="memory"><br>
storage:<input type="text" name="storage"><br>
timezone:<input type="text" name="timezone"><br>
<input type="submit" value="Submit">
</form> 
</html>
'''

secid = '5toRb5lCdEU2q5H'

# This class defines response to each request
class MyTCPHandler(SocketServer.BaseRequestHandler):
#class MyTCPHandler(SRH):
    def handle(self):
        # self.request is the TCP socket connected to the client
        request = ''
        #begin = time.time()
        #timeout = 2
        buf=''
        i=0
        while  buf.find('exit') == -1 or len(buf)==1440 and i==1:
            buf = self.request.recv(2048)
            request += buf
            i += 1
            print i
            print "buf:",len(buf)
            if not buf or len(buf)<1440 and i==1:
                break 
        #    print "time:",time.time()-begin
        #    if request and time.time()-begin > timeout:
        #        break
        #request = self.request.recv(1024)
        f = open('/root/server8000.log','a')

        print 'Connected by',self.client_address[0]
        (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
        f.write(datevalue + ' Connected by ' + self.client_address[0] + '\n')
        print 'Request is', len(request),request
        print '--------------'

        tmp  	   = request.split(' ')
        method     = tmp[0]
        src        = tmp[1]
        print "Method: ", method
        print "src:", src

        if method == 'GET':          
            str1   = src.split('?')
            if len(str1)==1:
                content = text_content
            else:   
                mess1  = str1[1].split('&')
                tmp1   = mess1[0].split('=')
            #下载 ssh 认证key
            if src == '/.ssh/id_rsa.pub?secid='+secid :
                f1 = open('id_rsa.pub','rb')
                content = f1.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' downloadauthkey ' + self.client_address[0] + '\n')
            #下载更新uploadmon.py
            elif src == '/uploadmon.py?secid='+secid :
                f2 = open('uploadmon.py','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' downloaduploadmon.py ' + self.client_address[0] + '\n')
            #下载备份设置baksetting
            elif src == '/dwbaksetting?secid='+secid :
                f2 = open('/root/log/baksetting','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' dwbaksetting ' + self.client_address[0] + '\n')
            #中心下载备份反馈信息
            elif src == '/dwbakinfo?secid='+secid :
                (status,getbakinfo) = commands.getstatusoutput('cat /root/log/bakinfo')
                content = getbakinfo
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' downloadbaseinfo ' + self.client_address[0] + '\n')
            #中心下载服务器配置基础信息
            elif src == '/dwbaseinfo?secid='+secid :
                (status,getbaseinfo) = commands.getstatusoutput('cat /root/log/baseinfo')
                content = getbaseinfo
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' downloadbaseinfo ' + self.client_address[0] + '\n')
            #中心下载各服务器监控信息
            elif src == '/dwmoninfo?secid='+secid :
                (status,getmoninfo) = commands.getstatusoutput('find /root/log/moninfo* -exec tail -n 1 {} \;')
                content = getmoninfo
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' downloadmoninfo ' + self.client_address[0] + '\n')
            #中心下载端口占用情况信息
            elif src == '/dwportinfo?secid='+secid :
                (status,getportinfo) = commands.getstatusoutput('find /root/log/portinfo* -exec tail -n 1 {} \;')
                content = getportinfo
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' downloadportinfo ' + self.client_address[0] + '\n')
            #老接口，下载备份配置信息，已用不上了，暂时保留
            elif str1[0] == '/downloadmessage' and mess1[0] == 'secid='+secid :
                tmp2   = mess1[1].split('=')
                ip     = tmp2[1]
                try:
                    conn=MySQLdb.connect(host='localhost',user='yanght',passwd='yanght',db='cmdb',port=3306,charset='utf8')
                    cur=conn.cursor()
                    sql=('select id,ip,hostname,downloadurl,downloaddest,downloadmode from base where ip =\"%s\"'%ip)
                    print sql
                    count=cur.execute(sql)
                    print 'there has %s rows record' % count
                    if count != 0 :
                        result=cur.fetchone()
                        print 'find record in db:',result[0],result[1],result[2],result[3],result[4],result[5]
                    content=''
                    for x in result:
                        if type(x) != None:
                            content+=str(x)+';'
                        else:
                            content+='empty'+';'
                    #content = str(result[0])+' '+result[1]+' '+result[2]+' '+result[3]+' '+result[4]+' '+result[5]
                    (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                    f.write(datevalue + ' downloadmessage: ' + self.client_address[0] + ' ' + content + '\n')

                    conn.commit()
                    cur.close()
                    conn.close()
                except MySQLdb.Error,e:
                    print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            else:
                content = text_content

            self.request.sendall(content)

        if method == 'POST':
            form = request.split('\r\n')
            #idx = form.index('')             # Find the empty line
            #entry = form[idx:]               # Main content of the request
            #messages= MySQLdb.escape_string(form[-1]).split('&')
            print request
            #messages= urllib.unquote(MySQLdb.escape_string(form[-1])).replace('+',' ').split('&')
            messages= urllib.unquote(form[-1]).replace('+',' ').split('&')
            messlen = len(messages)
            print messlen
            print messages
            dicmess={}
            for i in range(0,messlen):
                tmp=messages[i].split('=')
                dicmess.update({tmp[0]:tmp[1]})
            print 'messages',messages
            
            for key in dicmess:
                print key,dicmess[key]
            #上传服务器基础信息
            if dicmess['secid'] == secid and dicmess['type'] == 'baseinfo' :
                self.request.sendall(text_content + '\n <p>' + dicmess['hostname'] + dicmess['ip'] + dicmess['system'] + dicmess['cpu'] +dicmess['memory'] + dicmess['storage'] + dicmess['timezone'] + dicmess['username'] + '</p>')
                (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                (status,novalue) = commands.getstatusoutput('if [ ! -f /root/log/baseinfo ];then touch /root/log/baseinfo; fi')
                (status,novalue) = commands.getstatusoutput('trueth=\`grep' +dicmess['ip']+ '/root/log/baseinfo\`;if [ ! -n "${trueth}" ]; then sed -i \'\' /'+dicmess['ip']+'/d /root/log/baseinfo; fi')
                f3 = open('/root/log/baseinfo','a')
                content= dicmess['hostname'] +','+ dicmess['ip'] +','+ dicmess['system'] +','+ dicmess['cpu'] +','+dicmess['memory'] +','+ dicmess['storage'] +','+ dicmess['timezone'] +','+ dicmess['username'] 
                f3.write(content + '\n')
            #上传监控信息
            elif dicmess['secid'] == secid and dicmess['type'] == 'moninfo' :
                self.request.sendall(text_content + '\n <p>' + dicmess['hostname'] + dicmess['ip'] + dicmess['cpu'] +dicmess['memory'] + dicmess['storage'] + dicmess['net']  + '</p>')
                filename='/root/log/moninfo'+dicmess['ip']+'.log'
                (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                (status,novalue) = commands.getstatusoutput('if [ ! -f '+filename+' ];then touch '+filename+'; fi')
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f4 = open(filename,'a')
                content=datevalue +','+ dicmess['hostname'] +','+ dicmess['ip'] +','+ dicmess['cpu'] +','+dicmess['memory'] +','+ dicmess['storage'] +','+ dicmess['net'] 
                f4.write(content + '\n')
            #上传端口信息
            elif dicmess['secid'] == secid and dicmess['type'] == 'portinfo' :
                self.request.sendall(text_content + '\n <p>' + dicmess['hostname'] + dicmess['ip'] + dicmess['ports'] + '</p>')
                filename='/root/log/portinfo'+dicmess['ip']+'.log'
                (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                (status,novalue) = commands.getstatusoutput('if [ ! -f '+filename+' ];then touch '+filename+'; fi')
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f5 = open(filename,'a')
                content=datevalue +','+ dicmess['hostname'] +','+ dicmess['ip'] +','+ dicmess['ports']  
                f5.write(content + '\n')
            #中心上传备份信息
            elif dicmess['secid'] == secid and dicmess['type'] == 'baksetting' :
                self.request.sendall(text_content + '\n <p>' + dicmess['baksetting']  + '</p>')
                filename='/root/log/baksetting'
                (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                (status,novalue) = commands.getstatusoutput('if [ ! -f '+filename+' ];then touch '+filename+'; fi')
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f6 = open(filename,'wb')
                content=dicmess['baksetting']
                #content=content.encode('gbk')
                #s=u'\u957f\u6625\u5e02'
                #print urllib.unquote(str(s)).decode('utf8')
                #print content.decode("raw_unicode-escape"),len(content),type(content)
                print content
                fds=content.split(',')
                content=''
                for i in range(len(fds)/4) :
                    content += fds[i*4] +','+ fds[i*4+1] +','+ fds[i*4+2] +','+ fds[i*4+3] + "\n"
                f6.write(content)
            #上传备份结果信息
            elif dicmess['secid'] == secid and dicmess['type'] == 'bakinfo' :
                self.request.sendall(text_content + '\n <p>' + dicmess['bakinfo']  + '</p>')
                filename='/root/log/bakinfo'
                (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                (status,novalue) = commands.getstatusoutput('if [ ! -f '+filename+' ];then touch '+filename+'; fi')
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f7 = open(filename,'wb')
                content=dicmess['bakinfo']
                print content
                f7.write(content)
            else:
                print 'incorrect secid'
            
            
# Create the server
server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
#server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
# Start the server, and work forever
server.serve_forever()
