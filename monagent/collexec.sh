#!(which bash)
source ./collfunc
source ./collconf
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/opt/bin:/sbin:/bin
#define information for help
osInfo="os type"
timestampInfo="timestamp"
netdevInfo="network device"
ipInfo="ip"
cpuidleInfo="cpu idle%"
memInfo="memory TOTAL USED"
netspeedInfo="net speed RX TX"
diskrootrateInfo="root Usage %"
diskioInfo="disk IO await util%"
netportsInfo="opened Ports"
snInfo="series number"
megaerrInfo="error of raid or disk"
baseinfo="get baseinfo"
moninfo="get moninfo"
portsinfo="get portsinfo"
bakinfo="get bakinfo"
errinfo="get errinfo"
funclist=(baseinfo moninfo portsinfo bakinfo errinfo os timestamp netdev ip cpuidle mem netspeed diskrootrate diskio netports sn megaerr)
funcinfo=("$baseinfo" "$moninfo" "$portsinfo" "$bakinfo" "$errinfo" "$osInfo" "$timestampInfo" "$netdevInfo" "$ipInfo" "$cpuidleInfo" "$memInfo" "$netspeedInfo" "$diskrootrateInfo" "$diskioInfo" "$netportsInfo" "$snInfo" "$megaerrInfo")
#把获取的信息分成五组：
#		baseinfo		基本信息
#		moninfo			监控信息
#		portsinfo   端口信息
#		bakinfo			备份信息
#		errinfo			错误信息：如硬盘故障
#   webinfo     访问信息：WEB
case $1 in
baseinfo)
  func_baseinfo
;;
moninfo)
  func_OS 
  func_TIMESTAMP
  func_NETDEV
  func_IP
  func_CPUIDLE
  func_MEM
  func_NETSPEED
  func_DISKROOTRATE
  func_DISKIO
  echo "$TIMESTAMP, $IP, $CPUIDLE, $MEMTOTAL, $MEMUSED, $RX, $TX, $DISKROOTRATE, $IOAWAIT, $IOUTIL"
;;
portsinfo)
  func_NETPORTS
  cat /tmp/netports.csv  
;;
bakinfo)
  func_bakinfo
;;
errorinfo)
  func_MegaERR  &&  echo "$MegaERR"
;;
webinfo)
  func_web
;;
1|os)
  func_OS &&   echo $sys
;;
2|sn)
  func_SN &&   echo $SN
;;
3|cpuidle)
  func_CPUIDLE &&   echo $CPUIDLE
;;
4|timestamp)
  func_TIMESTAMP &&   echo $TIMESTAMP
;;
5|ip)
  func_NETDEV
  func_IP &&   echo $IP
;;
6|mem)
  func_MEM &&  echo $MEMTOTAL $MEMUSED
;;	
7|netspeed)
  func_OS
  func_NETDEV
  func_NETSPEED &&  	echo $RX $TX
;;	
8|diskrootrate)
    func_DISKROOTRATE  &&  echo $DISKROOTRATE
;;
9|diskio)
  func_DISKIO &&  	echo $IOAWAIT $IOUTIL
;;
diskerr)
  func_MegaERR  &&  echo $MegaERR || echo "No disk err"
;;
help|*)
  echo "usage: $0 [`echo ${funclist[@]}|sed 's/ /|/g'`] [-ip <ip> |-ipfile <filename>]"
  for ((i=1;i<${#funclist[@]};i++))
  do 
    echo  "        "${funclist[i]}"           :"${funcinfo[i]}
  done
;;
esac
