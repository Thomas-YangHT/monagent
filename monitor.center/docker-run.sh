docker rm -f moncenter
docker run --name moncenter \
--restart=always \
--dns=192.168.100.1 \
-e TZ='Asia/Shanghai' \
-v /export/opt/cmp_mysql2/mysql/info/:/export/opt/cmp_mysql2/mysql/info/  \
-v $PWD/rootcron:/etc/crontabs/root \
-d moncenter sh START.sh

#/export/opt/cmp_mysql2/mysql/info/  ��mysql������Ŀ¼��ͬdwloadmon.py���MYHOME����
