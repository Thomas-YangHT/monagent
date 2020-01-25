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

        if method == 'GET':          
            str1   = src.split('?')
            if len(str1)==1:
                content = text_content
            else:   
                mess1  = str1[1].split('&')
                tmp1   = mess1[0].split('=')
            DownFiles=['id_rsa.pub','md5.txt','uploadmon.py','fileUpdate.py','collexec.sh','collfunc','collconf','collcron.sh','instmon.sh','baksetting']
            DownFiles.append('dwbakinfo')
            DownFiles.append('dwbaseinfo')
            DownFiles.append('dwmoninfo')
            DownFiles.append('dwportinfo')
            DownFiles.append('dwwebinfo')
            DownFiles.append('dwerrinfo')
            for  dwfile in DownFiles :
                if src == '/' + dwfile + '?secid='+secid :
                    f1 = open(dwfile,'rb')
                    content = f1.read()
                    (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                    f.write(datevalue + ' download '+dwfile+' ' + self.client_address[0] + '\n')
                else:
                    content = text_content
            self.request.sendall(content)

'''
            #下载 ssh 认证key
            if src == '/id_rsa.pub?secid='+secid :
                f1 = open('id_rsa.pub','rb')
                content = f1.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download authkey ' + self.client_address[0] + '\n')
            #下载更新md5.txt
            elif src == '/md5.txt?secid='+secid :
                f2 = open('md5.txt','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download uploadmon.py ' + self.client_address[0] + '\n')
            #下载更新uploadmon.py
            elif src == '/uploadmon.py?secid='+secid :
                f2 = open('uploadmon.py','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download uploadmon.py ' + self.client_address[0] + '\n')
            #下载更新fileupdate.py
            elif src == '/fileUpdate.py?secid='+secid :
                f2 = open('fileUpdate.py','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download fileUpdate.py ' + self.client_address[0] + '\n')
            #下载更新collexec.sh
            elif src == '/collexec.sh?secid='+secid :
                f2 = open('collexec.sh','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download collexec.sh ' + self.client_address[0] + '\n')
            #下载更新collfunc
            elif src == '/collfunc?secid='+secid :
                f2 = open('collfunc','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download collfunc ' + self.client_address[0] + '\n')
            #下载更新collconf
            elif src == '/collconf?secid='+secid :
                f2 = open('collconf','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download collconf ' + self.client_address[0] + '\n')
            #下载更新collcron.sh
            elif src == '/collcron.sh?secid='+secid :
                f2 = open('collcron.sh','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download collcron.sh ' + self.client_address[0] + '\n')
            #下载更新instmon.sh
            elif src == '/instmon.sh?secid='+secid :
                f2 = open('instmon.sh','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download instmon.sh ' + self.client_address[0] + '\n')
            #下载备份设置baksetting
            elif src == '/dwbaksetting?secid='+secid :
                f2 = open('/root/log/baksetting','rb')
                content = f2.read()
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' dw baksetting ' + self.client_address[0] + '\n')
            #中心下载备份反馈信息
            elif src == '/dwbakinfo?secid='+secid :
                (status,getbakinfo) = commands.getstatusoutput('cat /root/log/bakinfo')
                content = getbakinfo
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download bakinfo ' + self.client_address[0] + '\n')
            #中心下载服务器配置基础信息
            elif src == '/dwbaseinfo?secid='+secid :
                (status,getbaseinfo) = commands.getstatusoutput('cat /root/log/baseinfo')
                content = getbaseinfo
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download baseinfo ' + self.client_address[0] + '\n')
            #中心下载各服务器监控信息
            elif src == '/dwmoninfo?secid='+secid :
                (status,getmoninfo) = commands.getstatusoutput('find /root/log/moninfo* -exec tail -n 1 {} \;')
                content = getmoninfo
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download moninfo ' + self.client_address[0] + '\n')
            #中心下载端口占用情况信息
            elif src == '/dwportinfo?secid='+secid :
                (status,getportinfo) = commands.getstatusoutput('find /root/log/portinfo* -exec cat {} \;')
                content = getportinfo
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download portinfo ' + self.client_address[0] + '\n')
            #中心下载webinfo信息
            elif src == '/dwwebinfo?secid='+secid :
                (status,getwebinfo) = commands.getstatusoutput('find /root/log/webinfo* -exec cat {} \;')
                content = getwebinfo
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download webinfo ' + self.client_address[0] + '\n')
            #中心下载errinfo信息
            elif src == '/dwerrinfo?secid='+secid :
                (status,geterrinfo) = commands.getstatusoutput('find /root/log/errinfo* -exec cat {} \;')
                content = geterrinfo
                (status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f.write(datevalue + ' download errinfo ' + self.client_address[0] + '\n')                                
            else:
                content = text_content
            self.request.sendall(content)
'''


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
            UpFiles=['baseinfo','baksetting','bakinfo']
            UpIpFiles=['moninfo','portinfo','webinfo','errinfo']
            for uf in UpFiles :           
                if dicmess['secid'] == secid and dicmess['type'] == uf :
                    self.request.sendall(return_content)
                    (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                    (status,novalue) = commands.getstatusoutput('if [ ! -f /root/log/'+uf+' ];then touch /root/log/'+uf+'; fi')
                    (status,novalue) = commands.getstatusoutput('trueth=\`grep' +dicmess['ip']+ '/root/log/'+uf+'\`;if [ ! -n "${trueth}" ]; then sed -i \'\' /'+dicmess['ip']+'/d /root/log/'+uf+'; fi')
                    f2 = open('/root/log/'+uf,'a')
                    content = dicmess[uf]
                    if dicmess['type'] == 'baksetting' :
                        fds=content.split(',')
                        content=''
                        for i in range(len(fds)/4) :
                            content += fds[i*4] +','+ fds[i*4+1] +','+ fds[i*4+2] +','+ fds[i*4+3] + "\n"
                    f2.write(content + '\n')

            for uf in UpIpFiles :
                if dicmess['secid'] == secid and dicmess['type'] == uf :
                    self.request.sendall(return_content)
                    filename='/root/log/' + uf + dicmess['ip']+'.log'
                    (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                    (status,novalue) = commands.getstatusoutput('if [ ! -f '+filename+' ];then touch '+filename+'; fi')
                    f3 = open(filename,'a')
                    content=dicmess[uf]  
                    f3.write(content + '\n')
                else:
                    print 'incorrect secid or type'
'''
            #上传服务器基础信息
            if dicmess['secid'] == secid and dicmess['type'] == 'baseinfo' :
                self.request.sendall(return_content)
                (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                (status,novalue) = commands.getstatusoutput('if [ ! -f /root/log/baseinfo ];then touch /root/log/baseinfo; fi')
                (status,novalue) = commands.getstatusoutput('trueth=\`grep' +dicmess['ip']+ '/root/log/baseinfo\`;if [ ! -n "${trueth}" ]; then sed -i \'\' /'+dicmess['ip']+'/d /root/log/baseinfo; fi')
                f3 = open('/root/log/baseinfo','a')
                content = dicmess['baseinfo']
                f3.write(content + '\n')
            #上传监控信息
            elif dicmess['secid'] == secid and dicmess['type'] == 'moninfo' :
                self.request.sendall(return_content)
                filename='/root/log/moninfo'+dicmess['ip']+'.log'
                (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                (status,novalue) = commands.getstatusoutput('if [ ! -f '+filename+' ];then touch '+filename+'; fi')
                #(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f4 = open(filename,'a')
                content=dicmess['moninfo']  
                f4.write(content + '\n')
            #上传端口信息
            elif dicmess['secid'] == secid and dicmess['type'] == 'portinfo' :
                self.request.sendall(return_content)
                filename='/root/log/portinfo'+dicmess['ip']+'.log'
                (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                (status,novalue) = commands.getstatusoutput('if [ ! -f '+filename+' ];then touch '+filename+'; fi')
                #(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f5 = open(filename,'wb')
                content=dicmess['portinfo']   
                f5.write(content + '\n')
            #上传web信息
            elif dicmess['secid'] == secid and dicmess['type'] == 'webinfo' :
                self.request.sendall(return_content)
                filename='/root/log/webinfo'+dicmess['ip']+'.log'
                (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                (status,novalue) = commands.getstatusoutput('if [ ! -f '+filename+' ];then touch '+filename+'; fi')
                #(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f5 = open(filename,'wb')
                #content=gzip.decompress(dicmess['webinfo']).decode("utf-8")
                content=dicmess['webinfo']
                f5.write(content + '\n')
            #上传err信息
            elif dicmess['secid'] == secid and dicmess['type'] == 'errinfo' :
                self.request.sendall(return_content)
                filename='/root/log/errinfo'+dicmess['ip']+'.log'
                (status,novalue) = commands.getstatusoutput('if [ ! -d /root/log ];then mkdir /root/log; fi')
                (status,novalue) = commands.getstatusoutput('if [ ! -f '+filename+' ];then touch '+filename+'; fi')
                #(status,datevalue) = commands.getstatusoutput('date "+ %Y%m%d %H:%M:%S"')
                f5 = open(filename,'wb')
                content=dicmess['errinfo']   
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
 '''           
            
# Create the server
server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
#server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
# Start the server, and work forever
server.serve_forever()
