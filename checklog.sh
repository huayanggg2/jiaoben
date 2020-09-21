#!/bin/bash  
#需要检测的日志路径，后面加组件，用分号隔开，多个路径用空格" "隔开
all_logpath='/usr/local/opentsdb-2.4.0/build;tomcat /var/log;nginx'
#获取当前日期
now_time=`date '+%Y-%m-%d'`
#转换当前日期为时间戳
t1=`date -d "$now_time" +%s`
#手机号
phone='13893***'
#第一个循环，循环所有的日志目录
for alpth in $all_logpath
do
#设置两个变量，一个获取all_logpath分号;前面的日志路径，一个用来获取分号;后面的组件名称，用awk通过分号获取
mode=`echo $alpth|awk -F';' '{print $2}'`
logpath=`echo $alpth|awk -F';' '{print $1}'`
#设置一个变量，来计算循环次数
num=0
#找出目录下面所有.log日志文件个数
len=`ls $logpath/*.log|wc -l`
#第二个循环，循环当前目录下的所有日志文件
for logfile in $logpath/*.log
do
#获取日志文件最后更新时间
last_updatetime=`stat -c %y  $logfile|awk '{print $1}'`
#转换当前日志文件更新时间
t2=`date -d "$last_updatetime" +%s`
#比较两个时间，如果相等，说明今日有新日生成，则结束循环
if [ $t1 = $t2  ];then
	echo "$logpath 今日已生成新日志"
	break
fi
#每执行一次加1
num=$[$num+1]
#判断所有.log文件个数和循环次数，如果相等，说明循环结束，并且没有日志文件被修改
if [ $num = $len ];then
	content=' 今日无日志更新，请处理'
        curl --data "mobile=$phone&content=$content&rd=1" "短信url?method=Submit"
fi
done
done
exit
