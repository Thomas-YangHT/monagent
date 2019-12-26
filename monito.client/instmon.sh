#instmon.sh
#in all server need to monitor:
NETWORK=192.168.10
ETH=`ip a|grep $NETWORK|awk '{print $7}'|grep -v "lo:"`
USER=xwx
HOMEDIR=/home/xwx/monagent.client
KEYname=xwx@k8host

crontab -l|grep -vP "uploadmon.py|nettrafic" >>/var/spool/cron/${USER}

echo "*/5 * * * * sleep 5;/usr/bin/python $HOMEDIR/uploadmon.py upmoninfo >/root/monitor/upmoninfo.log"  >>/var/spool/cron/${USER}
echo "*/5 * * * * /bin/bash $HOMEDIR/nettrafic.sh $ETH >>$HOMEDIR/nettrafic.log"  >>/var/spool/cron/${USER}
echo "*/5 * * * * sleep 5;/usr/bin/python $HOMEDIR/uploadmon.py upportinfo >/root/monitor/upportinfo.log"  >>/var/spool/cron/${USER}
echo "*/5 * * * * /usr/bin/python $HOMEDIR/fileUpdate.py uploadmon.py >/root/monitor/fileupdate.log"  >>/var/spool/cron/${USER}

/usr/bin/python /root/monitor/uploadmon.py upbaseinfo 
[ "`grep $KEYname  ~/.ssh/authorized_keys`" ] && echo "Already install server key" || /usr/bin/python $HOMEDIR/uploadmon.py downkey
