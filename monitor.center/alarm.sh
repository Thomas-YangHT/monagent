#!/usr/bin/sh
#清空报警文件
echo >alarm

#检查硬盘空间大于85%的
more /root/moninfo|awk -F',' '{print $3","$6}'|sed 's/%//g'| awk -F',' '{if ($2>85) print $1,"disk",$2,"%"}' >/root/alarm

#检查端口连接状态，默认5分钟连一次，连续3次没连上的，只在Center监控机上可用；
#/usr/bin/php /usr/share/nginx/html/qinmonitor/portscheck.php >>/root/alarm

#检查最后一次获得负载信息的时间，如与当前时间相差超过15分钟，则报警
#20170119 10:15:08	192.168.200.8
dbdates=(`echo "select a.date,a.ip from moninfo as a inner join hostip as b on trim(a.ip)=trim(b.ip)"|mysql -uyanght -pyanght -h192.168.100.71 -D moninfo`)
curdate=(`date '+%Y%m%d %T'`)
length=${#dbdates[@]}
rows=$[($length+1) / 3]
for ((i=1;i<$rows;i++));
do
        #echo ${dbdates[$i*3-1]} ${dbdates[$i*3]} ${dbdates[$i*3+1]}
        #echo ${curdate[0]} ${curdate[1]}
        date1=`date +%s -d "${dbdates[$i*3-1]} ${dbdates[$i*3]}"`
        date2=`date +%s -d "${curdate[0]} ${curdate[1]}"`
        cha=$(($date2-$date1))
        if(( "$cha" >900 ));then
                echo "IP:" ${dbdates[$i*3+1]} "can't connect for" $cha "seconds. last connect on" ${dbdates[$i*3-1]} ${dbdates[$i*3]} >>/root/alarm
        fi

done

#--------------------------------
#以微信公众号报警
/usr/local/bin/python /root/sendmesstowx.py
#以邮件方式报警
flag=`cat /root/alarm`
if [ -n "${flag}" ];then
  /usr/bin/sh /root/sendmailXHY.sh
fi
