docker rm -f monagent
docker run --name monagent \
--restart=always \
--dns=192.168.100.1 \
-e TZ='Asia/Shanghai' \
-p 18000:18000 \
-d monagent
