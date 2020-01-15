#instmon.sh
#in all server need to monitor:
NETWORK=192.168.10
ETH=`ip a|grep $NETWORK|sed 's/noprefixroute//g'|awk '{print $7}'|grep -v "lo:"|head -n 1`
KEYname=xwx@k8host
USER=`whoami`
HOMEDIR=${HOME}/monagent.client
DownloadURL=http://192.168.10.92/monagent.client
crontab -l|grep -vP "uploadmon.py|nettrafic" >/var/spool/cron/${USER}

echo "*/5 * * * * sleep 5;/usr/bin/python $HOMEDIR/uploadmon.py upmoninfo >$HOMEDIR/upmoninfo.log 2>&1 "  >>/var/spool/cron/${USER}
#echo "*/5 * * * * /bin/bash $HOMEDIR/nettrafic.sh $ETH >>$HOMEDIR/nettrafic.log 2>&1"  >>/var/spool/cron/${USER}
echo "*/5 * * * * sleep 10;/usr/bin/python $HOMEDIR/uploadmon.py upbaseinfo >$HOMEDIR/upbaseinfo.log 2>&1"  >>/var/spool/cron/${USER}
echo "*/5 * * * * sleep 15;/usr/bin/python $HOMEDIR/uploadmon.py upportinfo >$HOMEDIR/upportinfo.log 2>&1"  >>/var/spool/cron/${USER}
echo "*/5 * * * * /usr/bin/python $HOMEDIR/fileUpdate.py uploadmon.py >$HOMEDIR/fileupdate.log 2>&1"  >>/var/spool/cron/${USER}
echo "*/5 * * * * sleep 5;/usr/bin/python $HOMEDIR/fileUpdate.py collexec.sh >$HOMEDIR/fileupdate.log 2>&1 "  >>/var/spool/cron/${USER}
echo "*/5 * * * * /usr/bin/python $HOMEDIR/fileUpdate.py collfunc >$HOMEDIR/fileupdate.log 2>&1"  >>/var/spool/cron/${USER}
echo "*/5 * * * * /usr/bin/python $HOMEDIR/fileUpdate.py collconf >$HOMEDIR/fileupdate.log 2>&1"  >>/var/spool/cron/${USER}

[ -d "$HOMEDIR" ] || mkdir $HOMEDIR
cd $HOMEDIR && \
curl -O  $DownloadURL/fileUpdate.py  &&  \
python fileUpdate.py uploadmon.py && \
python $HOMEDIR/fileUpdate.py collexec.sh && \
python $HOMEDIR/fileUpdate.py collfunc && \
python $HOMEDIR/fileUpdate.py collconf && \
/usr/bin/python $HOMEDIR/uploadmon.py upbaseinfo 
[ "`grep $KEYname  ~/.ssh/authorized_keys`" ] && echo "Already install server key" || /usr/bin/python $HOMEDIR/uploadmon.py downkey
