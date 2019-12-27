truth=`ps auxwww|grep "python monagent.py"|grep -v grep`
if [ ! -n "${truth}" ]; then 
   nohup /usr/bin/python /root/monitor/monagent.py >monagent.out 2>&1 &
else
   echo "Already running monagent!"
fi  
