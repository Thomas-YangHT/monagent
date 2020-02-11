#instmon.sh
#in all server need to monitor:
# config network first:
NETWORK=192.168.10
KEYname=xwx@k8host

echo "start install monclient..."
ETH=`ip a|grep $NETWORK|sed 's/noprefixroute//g'|awk '{print $7}'|grep -v "lo:"|head -n 1`
USER=`whoami`
HOMEDIR=${HOME}/monagent.client
##DownloadURL=http://192.168.10.92/monagent.client
echo "install into cron..."
crontab -l|grep -vP "uploadmon.py|nettrafic|collcron" >${USER}
echo "*/5 * * * *  (cd ${HOMEDIR};/bin/bash ./collcron.sh)"  >>${USER}
sudo cp ${USER} /var/spool/cron/
sudo chown ${USER}:${USER} /var/spool/cron/${USER}
sudo chmod 600 /var/spool/cron/${USER}
echo "install into $HOMEDIR ..."
[ -d "$HOMEDIR" ] && rm $HOMEDIR/*err $HOMEDIR/*log || mkdir $HOMEDIR
cd $HOMEDIR && \
#curl -O  $DownloadURL/fileUpdate.py  &&  \
curl -o fileUpdate.py  http://192.168.10.92:18000/fileUpdate.py?secid='5toRb5lCdEU2q5H' && \
python $HOMEDIR/fileUpdate.py collcron.sh && \
echo "first run collcron.sh..." && \
bash collcron.sh
echo "install ssh serverkey..." && \
[ "`grep $KEYname  ~/.ssh/authorized_keys`" ] && echo "Already install server key" || /usr/bin/python $HOMEDIR/uploadmon.py downkey
