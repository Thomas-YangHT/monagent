/usr/bin/python /root/monagent.client/fileUpdate.py uploadmon.py > /root/monagent.client/fileupdate.log 2>&1 && \
/usr/bin/python /root/monagent.client/fileUpdate.py collexec.sh  >>/root/monagent.client/fileupdate.log 2>&1 && \
/usr/bin/python /root/monagent.client/fileUpdate.py collfunc     >>/root/monagent.client/fileupdate.log 2>&1 && \
/usr/bin/python /root/monagent.client/fileUpdate.py collconf     >>/root/monagent.client/fileupdate.log 2>&1
/usr/bin/python /root/monagent.client/uploadmon.py upmoninfo  >/root/monagent.client/upmoninfo.log 2>&1 && \
/usr/bin/python /root/monagent.client/uploadmon.py upbaseinfo >/root/monagent.client/upbaseinfo.log 2>&1 && \
/usr/bin/python /root/monagent.client/uploadmon.py upportinfo >/root/monagent.client/upportinfo.log 2>&1