pyname=$1
action=$2
logfile='/var/log/'

case "$2" in
  start)
    nohup python3 $pyname &
    ;;
  stop)
    pids=`ps -ef | grep python|grep ${pyname%.*} | awk '{ print $2 }'`
    for pid in $pids
    do
    kill -9 $pid
    done
    ;;
  *)
    echo "输入有误"
    exit 1
esac
exit 0
