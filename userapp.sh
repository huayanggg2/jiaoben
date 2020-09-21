#menu:需要操作的菜单栏
menu(){
	echo "\033[33m操作菜单!\033[0m"
	echo "\033[33mInput 1 : 查询当前所有用户的记录!\033[0m"
	echo "\033[33mInput 2 : 查询特定用户信息!\033[0m"
	echo "\033[33mInput 3 : 向passwd文件里添加一个新的用户记录!\033[0m"
	echo "\033[33mInput 4 : 从passwd文件里删除某个用户记录!\033[0m"
	echo "\033[33mInput 5 : 批量添加用户如user01-user10，初始密码为123456!\033[0m"
	echo "\033[33mInput 6 : 批量删除用户!\033[0m"
	echo "\033[33mInput 7 : 批量修改用户!\033[0m"
	echo "\033[33mInput 8 : 退出操作!\033[0m"
	echo ""
}
#获取菜单栏输入的数字，执行具体操作
branch(){
	#读取输入的数字
        read -p "请输入您需要操作的数字: " num 
        case $num in
		#如果输入数字为1	
		"1")	
			#查看passwd文件所有用户信息
			cat /etc/passwd | nl
			echo "\033[32m以上为所有用户的信息!\033[0m"
			;;
		"2")
			read -p "请输入您要查找的用户名:" user1
			#在passwd文件里面查找终端输入的用户名
			grep -n "$user1" /etc/passwd
					#判断，如果没有这个用户，则提示用户不存在
			                if [ $? -eq 1 ]; then
							echo "从用户不存在!"
					fi
			;;
		"3")
			read -p "请输入您要添加的用户名:" user2
			#新建用户命令
			sudo useradd $user2
			#新建该用户的家目录
			sudo mkdir /home/$user2
			#判断用户是否建立成功
			#grep $user2 /etc/passwd >/dev/null
                        awk -F: '{print $1}' /etc/passwd | grep ^$user2$
			if [ $? -eq 0 ]; then
				echo "\033[32m用户添加成功!\033[0m"
                        else
                                echo "\033[31m用户已存在！\033[0m"
			fi
			;;
		"4")                                     
			read -p "请输入您要删除的用户名:" user3
			#判断用户是否存在如果存在，则删除用户，不存在则提示用户不存在
			grep "$user3" /etc/passwd >/dev/null
			if [ $? -eq 0 ]; then
				#删除用户命令
				sudo userdel $user3
				#删除用户家目录
				sudo rm -r /home/$user3
				echo "\033[32m删除用户$user3成功!\033[0m"
			else		
				echo "\033[31m用户名不存在!\033[0m"
			fi
			;;
		"5")    
			#循环1-10并建立是个用户
			for i in $(seq 1 10)  
			do   
			#新建用户命令
			sudo useradd user$i;
		      	#新建用户家目录
			sudo mkdir /home/user$i
			if [ $? -eq 0 ];then
			#修改密码
			echo user$i:'123456' |sudo chpasswd
			echo "\033[32m添加用户user$i成功!\033[0m"
			else
				echo "\033[31muser$i该用户已存在！\033[0m"
			fi
			done 
			;;
		 "6")
			read -p "请输入您要批量删除的用户名，用空格隔开:" user4
			#循环终端输入的所有用户名
			for unme in $user4
			do
                                awk -F: '{print $1}' /etc/passwd | grep ^$user4$
                                if [ $? -eq 0 ];then
				    sudo userdel $unme
				    sudo rm -r /home/$unme
				echo "\033[32m删除用户$unme成功!\033[0m"
                                else
                                    echo "\033[31muser$i该用户不存在！\033[0m"
                                fi
			done	
			;;
		 "7")
			read -p "请输入您要批量修改的用户名和密码（如usera,passa userb,passb），用空格隔开:" allusernm
			#read -p "请输入您要批量修改的密码，用空格隔开" allpasswd
			#
			for unm in $allusernm
			do
				name=`echo $unm|awk -F, '{print $1}'`
				pass=`echo $unm|awk -F, '{print $2}'`
				grep "$name" /etc/passwd >/dev/null
				if [ $? -eq 0 ]; then
				echo $name:$pass |sudo chpasswd
				echo "\033[32m$name 用户密码修改成功！\033[0m"
				else
					echo "\033[31m$name用户不存在！\033[0m"
				fi
				
			done
			;;
		 "8")   
			echo "\033[31mBye bye！\033[0m"
			exit 0
			;;
		 *)#当终端输入非数字时，提示输入错误
			echo "\033[31m输入有误！\033[0m"
			;;
	esac
}

for i in $( seq 1 100)
do
menu
branch
if [ $i -eq 100 ]; then
	echo "error"
fi
echo "\033[34m本次操作结束！\033[0m"
echo "\r"
done
