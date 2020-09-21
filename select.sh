#定义路径，jar包以前的路径
path='http://download.redis.io/releases/'
#筛选出jar包
new_vsn=`curl -s $path|grep jar|sed -e 's/<a href=//' -e 's/>.*//'|sort|tail -1f`
#下载最新jar包
wget $path$new_vsn

