#Modify $MYHOME  with your mysql data directory
$MYHOME=/root/cmp_mysql/mysql/

docker rm -f moncenter
docker run --name moncenter \
--restart=always \
--dns=192.168.100.1 \
-e TZ='Asia/Shanghai' \
-v $MYHOME:/info/  \
-v $PWD/rootcron:/etc/crontabs/root \
-d moncenter sh START.sh

#/export/opt/cmp_mysql2/mysql/info/  ��mysql������Ŀ¼��ͬdwloadmon.py���MYHOME����
