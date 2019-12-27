#while [ "1" ]
#do
#ifconfig $eth| grep bytes |grep RX | awk '{print $5}' 
eth=$1
RXpre=$(ifconfig $eth| grep bytes |grep RX | awk '{print $5}')
TXpre=$(ifconfig $eth| grep bytes |grep TX | awk '{print $5}')
sleep 1
RXnext=$(ifconfig $eth| grep bytes |grep RX | awk '{print $5}')
TXnext=$(ifconfig $eth| grep bytes |grep TX | awk '{print $5}')
#clear
#echo  -e  "\t RX `date +%k:%M:%S` TX"
RX=$((${RXnext}-${RXpre}))
TX=$((${TXnext}-${TXpre}))
if [[ $RX -lt 1024 ]];then
RX="${RX}B/s"
elif [[ $RX -gt 1048576 ]];then
RX=$(echo $RX | awk '{print $1/1048576 "MB/s"}')
else
RX=$(echo $RX | awk '{print $1/1024 "KB/s"}')
fi
if [[ $TX -lt 1024 ]];then
TX="${TX}B/s"
elif [[ $TX -gt 1048576 ]];then
TX=$(echo $TX | awk '{print $1/1048576 "MB/s"}')
else
TX=$(echo $TX | awk '{print $1/1024 "KB/s"}')
fi
echo -e "`date +%k:%M:%S`  $eth  RX  $RX  TX  $TX "
#done
