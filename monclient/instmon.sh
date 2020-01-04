#instmon.sh
#in all server need to monitor:
NETWORK=192.168.10
ETH=`ip a|grep $NETWORK|sed 's/noprefixroute//g'|awk '{print $7}'|grep -v "lo:"|head -n 1`
KEYname=xwx@k8host
USER=`whoami`
HOMEDIR=${HOME}/monagent.client

crontab -l|grep -vP "uploadmon.py|nettrafic" >/var/spool/cron/${USER}

echo "*/5 * * * * sleep 5;/usr/bin/python $HOMEDIR/uploadmon.py upmoninfo >$HOMEDIR/upmoninfo.log 2>&1 "  >>/var/spool/cron/${USER}
echo "*/5 * * * * /bin/bash $HOMEDIR/nettrafic.sh $ETH >>$HOMEDIR/nettrafic.log 2>&1"  >>/var/spool/cron/${USER}
echo "*/5 * * * * sleep 5;/usr/bin/python $HOMEDIR/uploadmon.py upportinfo >$HOMEDIR/upportinfo.log 2>&1"  >>/var/spool/cron/${USER}
echo "*/5 * * * * /usr/bin/python $HOMEDIR/fileUpdate.py uploadmon.py >$HOMEDIR/fileupdate.log 2>&1"  >>/var/spool/cron/${USER}
echo "* */1 * * * /usr/bin/python $HOMEDIR/uploadmon.py upbaseinfo >$HOMEDIR/upbaseinfo.log 2>&1"  >>/var/spool/cron/${USER}

/usr/bin/python $HOMEDIR/uploadmon.py upbaseinfo 
[ "`grep $KEYname  ~/.ssh/authorized_keys`" ] && echo "Already install server key" || /usr/bin/python $HOMEDIR/uploadmon.py downkey
