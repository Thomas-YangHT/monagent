DNS=223.5.5.5

docker rm -f moncenter
docker run --name moncenter \
--restart=always \
--dns=$DNS \
-e TZ='Asia/Shanghai' \
-v $PWD/rootcron:/etc/crontabs/root \
-d moncenter sh START.sh