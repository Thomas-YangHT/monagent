#k8s 从给定的任意服务名，取得相对应IP和PORT
[ "$1"='' ] &&  NAME='monagent' ||  NAME=$1
podIp=`kubectl get pods --all-namespaces -o wide|grep $NAME|awk '{print $7}'`
a=(`kubectl get svc --all-namespaces -o wide|grep $NAME|awk '{print $4":"$6}'|sed -e 's/:/ /g' -e 's#/TCP##'`)
svc=${a[0]}
svcPort=${a[1]}
nodePort=${a[2]}
tee <<EOF
{
  "podIp:" "$podIp"
  "svc:" "$svc"
  "svcPort:" "$svcPort"
  "nodePort:" "$nodePort"
}
EOF

