#coding=utf-8
#用作监控、备份、基础信息的上传和下载中转服务
#日志默认都写在了/root/log/下，待修改成k8s挂载PVC
# use TCPServer
import commands
import SocketServer
#import gzip
#from SocketServer import StreamRequestHandler as SRH
#import MySQLdb
import sys,urllib,urllib2
import time
reload(sys)
sys.setdefaultencoding('utf-8')

HOST = ''
PORT = 18000

text_content = '''HTTP/1.1 200 OK
Content-Type:text/html
Server: myserver

<html>
<head>
<title>OK</title>
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
return_content = '''HTTP/1.1 200 OK
Content-Type:text/html

<html>
<head>
<title>OK</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
</head>
<p>Received OK</p>
</html>
'''
secid = '5toRb5lCdEU2q5H'
(status,genmd5) = commands.getstatusoutput('md5sum coll* *py|grep -v err > md5.txt')

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
        print '--------------'
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

        tmp  	   = request.split(' ')
        method     = tmp[0]
        src        = tmp[1]
        #print "Method: ", method
        #print "src:", src
        content = ''

        if method == 'GET':          
            str1   = src.split('?')
            if len(str1)==1:
                content = text_content
            else:   
                mess1  = str1[1].split('&')
                tmp1   = mess1[0].split('=')
            DownFiles = ['id_rsa.pub','md5.txt','uploadmon.py','fileUpdate.py','collexec.sh','collfunc','collconf','collcron.sh','instmon.sh']
            DownFiles.append('bakinfo')
            DownFiles.append('baseinfo')
            DownFiles.append('k8sinfo')
            DownFiles.append('baksetting')
            DownFiles.append('labelset')
            DownIpFiles = ['moninfo','portinfo','webinfo','errinfo']
            for  dwfile in DownFiles :
                if src == '/' + dwfile + '?secid='+secid :
                    if src == '/baseinfo?secid='+secid :
                        filename='/root/log/baseinfo'
                    elif src == '/k8sinfo?secid='+secid :
                        filename='/root/log/k8sinfo'
                    elif src == '/labelset?secid='+secid :
                        filename='/root/log/labelset'                   
                    else:
                        filename=dwfile
                    f1 = open(filename,'rb')
                    content = f1.read()
                    (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                    f.write(datevalue + ' download '+dwfile+' ' + self.client_address[0] + '\n')
            else:
                for dwfile in DownIpFiles :
                    if src == '/' + dwfile + '?secid='+secid :
                        if src == '/moninfo?secid='+secid :
                            (status,getinfo) = commands.getstatusoutput('find /root/log/moninfo* -exec tail -n 1 {} \;')
                        else :
                            (status,getinfo) = commands.getstatusoutput('find /root/log/'+dwfile+'* -exec cat {} \;')
                        content = getinfo
                        (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                        f.write(datevalue + ' download '+dwfile+' ' + self.client_address[0] + '\n')
            if content == '' :  
                content = text_content
            self.request.sendall(content)

        elif method == 'POST':
            form = request.split('\r\n')
            #idx = form.index('')             # Find the empty line
            #entry = form[idx:]               # Main content of the request
            #messages= MySQLdb.escape_string(form[-1]).split('&')
            #print request
            #messages= urllib.unquote(MySQLdb.escape_string(form[-1])).replace('+',' ').split('&')
            head=form[0].split(' ')
            print head
            if form[0].find("Content-Type: application/json"): print "json"
            messages= urllib.unquote(form[-1]).replace('+',' ').split('&')
            messlen = len(messages)
            print messlen
            print messages
            dicmess={}
            for i in range(0,messlen):
                tmp=messages[i].split('=')
                if len(tmp)==2: dicmess.update({tmp[0]:tmp[1]})
                else: print "tmp len incorrect:"+tmp
            print 'messages',messages
            
            for key in dicmess:
                print key,dicmess[key]
            UpFiles=['baseinfo','bakinfo','k8sinfo','baksetting','labelset']
            UpIpFiles=['moninfo','portinfo','webinfo','errinfo']
            if dicmess['secid'] == secid and dicmess['type'] == 'sendtowx' :
                self.request.sendall(return_content)
                (status,novalue) = commands.getstatusoutput('python sendmesstowx.py "' + dicmess['info'] + '"')
                print 'status:',status,novalue
                content='sendtowx'
            else:
                for uf in UpFiles :           
                    if dicmess['secid'] == secid and dicmess['type'] == uf :
                        self.request.sendall(return_content)
                        (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                        (status,novalue) = commands.getstatusoutput('if [ ! -f /root/log/'+uf+' ];then touch /root/log/'+uf+'; fi')
                        if dicmess['type'] == 'baseinfo' :
                            (status,novalue) = commands.getstatusoutput('trueth=\`grep' +dicmess['ip']+ '/root/log/'+uf+'\`;if [ ! -n "${trueth}" ]; then sed -i \'/'+dicmess['ip']+'/d\' /root/log/'+uf+'; fi')
                            f2 = open('/root/log/'+uf,'a')
                        else:
                            f2 = open('/root/log/'+uf,'wb')
                        if dicmess['type'] == 'baksetting' or dicmess['type'] == 'labelset':
                            content = dicmess['setting']
                            fds=content.split(',')
                            print content
                            print fds
                            content=''
                            if dicmess['type'] == 'baksetting' :
                                for i in range(len(fds)/4) :
                                    content += fds[i*4] +','+ fds[i*4+1] +','+ fds[i*4+2] +','+ fds[i*4+3] + "\n"
                            elif dicmess['type'] == 'labelset':
                                for i in range(len(fds)/2) :
                                    content += fds[i*2] +','+ fds[i*2+1] + "\n"
                        else:
                            content = dicmess['info']
                        f2.write(content + '\n')
                        break
                else :
                    for uf in UpIpFiles :
                        if dicmess['secid'] == secid and dicmess['type'] == uf :
                            self.request.sendall(return_content)
                            filename='/root/log/' + uf + dicmess['ip']+'.log'
                            (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                            (status,novalue) = commands.getstatusoutput('if [ ! -f '+filename+' ];then touch '+filename+'; fi')
                            if dicmess['type'] == 'moninfo' :
                                f3 = open(filename,'a')
                            else:
                                f3 = open(filename,'wb')
                            content=dicmess['info']  
                            f3.write(content + '\n')
                            break
            if content == '' :
                print 'incorrect secid or type'

# Create the server
server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
#server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
# Start the server, and work forever
server.serve_forever()
