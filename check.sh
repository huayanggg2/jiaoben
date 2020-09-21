cat result.txt | while read line
do
nober=$(echo $line | awk -F':' '{print $1}');
active=$(echo $line | awk -F' ' '{print $6}');
if [ "$active" == "YES" ];then
     echo $nober 'yes'
	#lotus-miner sectors update-state --really-do-it=true $nober Proving 
  elif [ "$active" == "NO" ];then
     echo $nober 'no'
	#lotus-miner sectors update-state --really-do-it=true $nober Committing 
fi
done
exit




 ping -c 1 -w 1 ${net}.${i} &> /dev/null