#Modify $MYHOME  with your mysql data directory
MYHOME=/root/cmp_mysql/mysql/
DNS=223.5.5.5

docker rm -f moncenter
docker run --name moncenter \
--restart=always \
--dns=$DNS \
-e TZ='Asia/Shanghai' \
-v $MYHOME:/info/  \
-v $PWD/rootcron:/etc/crontabs/root \
-d moncenter sh START.sh

#/export/opt/cmp_mysql2/mysql/info/  是mysql容器的目录，同dwloadmon.py里的MYHOME配置
