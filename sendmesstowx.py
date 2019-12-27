#!/usr/bin/python
import json
import commands
import sys,urllib,urllib2
import ssl 

ssl._create_default_https_context = ssl._create_unverified_context 

CorpID = "wx5b316e874036047e"
Secret = "Fr8zfhkaQUGR1IOzi47IJ_WGx4J580WpNnCmX0KMSpoeGx4hF0JThPD0ImTV0v_w" 
class wxmessage(): 
	url_get ="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + CorpID + "&corpsecret=" + Secret
	url_post ="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="
	the_page = ''
	decode_page  = {}
	def getwxtokey(self):
		req = urllib2.Request(self.url_get) 
		response = urllib2.urlopen(req) 
		self.the_page = response.read()	
		print self.the_page
		self.decode_page= json.loads(self.the_page)
		print self.decode_page['access_token']
	def sendwxmess(self):
		self.url_post += self.decode_page['access_token']
		print self.url_post
		values = {
			"touser": "@all",
			"toparty": " PartyID1 | PartyID2 ",
			"totag": " TagID1 | TagID2 ",
			"msgtype": "text",
			"agentid": "0",
			"text": {
				"content": content
			},
			"safe":"0",
		} 
		postdata = json.dumps(values).encode('UTF-8')
		print "postdate:" + postdata
		req = urllib2.Request(self.url_post, postdata) 
		response = urllib2.urlopen(req)
		self.the_page = response.read()
		self.decode_page= json.loads(self.the_page) 
		print self.decode_page

if len(sys.argv) == 2:
    content = sys.argv[1]
else:
    f1 = open('/root/alarm','rb')
    content = f1.read()
    f1.close()    
if content != None :
	wx = wxmessage()
	wx.getwxtokey()
	wx.sendwxmess()



	