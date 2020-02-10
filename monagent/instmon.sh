#instmon.sh
#in all server need to monitor:
NETWORK=192.168.10
ETH=`ip a|grep $NETWORK|sed 's/noprefixroute//g'|awk '{print $7}'|grep -v "lo:"|head -n 1`
KEYname=xwx@k8host
USER=`whoami`
HOMEDIR=${HOME}/monagent.client
DownloadURL=http://192.168.10.92/monagent.client
crontab -l|grep -vP "uploadmon.py|nettrafic|collcron" >${USER}
echo "*/5 * * * *  (cd $HOMEDIR;/bin/bash ./collcron.sh)"  >>${USER}
sudo cp ${USER} /var/spool/cron/
sudo chown ${USER}:${USER} /var/spool/cron/${USER}
sudo chmod 600 /var/spool/cron/${USER}
#echo "*/5 * * * * /bin/bash $HOMEDIR/nettrafic.sh $ETH >>$HOMEDIR/nettrafic.log 2>&1"  >>/var/spool/cron/${USER}
#echo "*/5 * * * * sleep 10;/usr/bin/python $HOMEDIR/uploadmon.py upbaseinfo >$HOMEDIR/upbaseinfo.log 2>&1"  >>/var/spool/cron/${USER}
#echo "*/5 * * * * sleep 15;/usr/bin/python $HOMEDIR/uploadmon.py upportinfo >$HOMEDIR/upportinfo.log 2>&1"  >>/var/spool/cron/${USER}
#echo "*/5 * * * * /usr/bin/python $HOMEDIR/fileUpdate.py uploadmon.py >$HOMEDIR/fileupdate.log 2>&1"  >>/var/spool/cron/${USER}
#echo "*/5 * * * * sleep 5;/usr/bin/python $HOMEDIR/fileUpdate.py collexec.sh >$HOMEDIR/fileupdate.log 2>&1 "  >>/var/spool/cron/${USER}
#echo "*/5 * * * * /usr/bin/python $HOMEDIR/fileUpdate.py collfunc >$HOMEDIR/fileupdate.log 2>&1"  >>/var/spool/cron/${USER}
#echo "*/5 * * * * /usr/bin/python $HOMEDIR/fileUpdate.py collconf >$HOMEDIR/fileupdate.log 2>&1"  >>/var/spool/cron/${USER}

[ -d "$HOMEDIR" ] && rm $HOMEDIR/*err $HOMEDIR/*log || mkdir $HOMEDIR
cd $HOMEDIR && \
#curl -O  $DownloadURL/fileUpdate.py  &&  \
curl -o fileUpdate.py  http://192.168.10.92:18000/fileUpdate.py?secid='5toRb5lCdEU2q5H' && \
python $HOMEDIR/fileUpdate.py collcron.sh && \
sh collcron.sh
[ "`grep $KEYname  ~/.ssh/authorized_keys`" ] && echo "Already install server key" || /usr/bin/python $HOMEDIR/uploadmon.py downkey
