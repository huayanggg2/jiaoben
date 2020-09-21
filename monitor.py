#!/usr/bin/env python3
 
import os
import time
import re
import sys
import datetime
import psutil  #用于获取CPU信息
#集群状态方法
def clusterstat():
    print("\033[31mceph集群状态:\033[0m")
    with os.popen('/var/lib/ceph/bin/ceph -s') as f:#通过命令获取输出结果
      cont = True
      li = []#定义一个list，用来存输出结果的每一项
      while cont:
          cont = f.readline()
          li.append(cont)
          if cont ==' \n':
              if li[0].strip().split(':')[0] =='cluster':#获取list的第一个值，如cluster,services,data,io等
                  print("".join(li))
                  li = []                   #如果等于data,则跳过循环，否则输出
              else:
                 #print("".join(li))
                  li = []
#clusterst = os.popen('/var/lib/ceph/bin/ceph -s').readlines()
def cephstat():#获取ceph存储信息
    print("\033[31mceph存储容量:\033[0m")
    #clusterst = os.popen('/var/lib/ceph/bin/ceph -s').readlines()
    with os.popen('/var/lib/ceph/bin/ceph -s') as f:
      cont = True
      li = []
      while cont:
          cont = f.readline()
          li.append(cont)
          if cont ==' \n':
              if li[0].strip().split(':')[0] =='data':#获取list的第一个值，如果为data，则为存储容量信息，输出
                  print("".join(li))
                  li = []
              else:
                  li = []
def clusterinfo():#获取集群信息，IOPS,MBPS等
    clusterinfo = os.popen('sudo /var/lib/ceph/bin/ceph osd pool stats|grep client').readline()#将查看集群状态命令输出内容放到clusterinfo变量
    print("\033[31m集群IOPS,MBPS:\033[0m")                                            
    print(clusterinfo.strip())#输出集群状态信息
def cephinfo():#获取存储信息，IOPS,MBPS等
    cephinfo = os.popen('/var/lib/ceph/bin/ceph -s|grep client').readline()#将查看存储状态命令输出内容放到clusterinfo变量
    print("\033[31m存储IOPS,MBPS:\033[0m")
    print(cephinfo.strip())
def mysqlstat():#获取mysql进程状态信息
    mysqlst = os.popen('systemctl status mysqld|grep Active').readline()
    print("\033[31mmysql进程状态:\033[0m")
    mstatus = mysqlst.split()[2]#通过空格分割字符串，取第三个值
    print(mstatus[1:-1])#去掉括号
def sysinfo():#获取系统用户连接数信息
    user_conn = os.popen('w').readline().split('users')[0].split('up')[1].strip()[-1]#通过w命令获取用户连接信息
    print("\033[31muserconn:\033[0m")
    print("用户连接数:     {0}".format(user_conn))
def cpuinfo():#获取cpu使用率信息
    cpuif = os.popen('top -bn2 -d1|grep Cpu|sed -n 2p').readline()#通过top命令读取cpu信息
    cpu_use = cpuif.split()[1]#截取cpu使用率
    print("\033[31mcpuinfo: \033[0m")
    #print("cpu使用率:     %.2f%%" %cpu_use)
    print("cpu使用率:       "+cpu_use+"%")
 
def meminfo():#获取内存使用率信息
    mem = psutil.virtual_memory()
    total = mem.total
    user_use = mem.used
    user_usemem_rate = user_use / total * 100
    print("内存使用率:      %.2f%%"%user_usemem_rate)
 
def diskinfo():#获取磁盘使用信息
    disk = os.popen('df -h').readlines()[1:]#通过命令获取磁盘使用和挂载信息
    print("\033[31mdisk_info:\033[0m")
    print('%-25s' % "挂载区:"+"使用率:")
    for info in disk:#循环和遍历每一行信息
        disk_item = info.split()
        mount = disk_item[5]
        disk_data_rate = disk_item[4]
       # print("挂载区: "+'%-30s' % mount+"使用率: "+disk_data_rate)
        print('%-30s' % mount+disk_data_rate)

def netinfo():#获取网卡信息
    print('\033[31mnet_info\033[0m')
    net_item = list(psutil.net_if_addrs())#通过psutil库的net_if_addrs方法获取网卡信息并赋值给net_item
    for net in net_item:
        if re.search(r'bond.*|em.*|en.*|^eth.*',net):#循环遍历并查找网卡名称
            network_card = net
            ip = psutil.net_if_addrs()[net][0].address#获取服务器Ip
            recv_1,recv_2,send_1,send_2=0,0,0,0#初始化网卡流量信息
            with open ('/proc/net/dev','r') as f:#从/proc/net/dev文件获取网卡流量使用信息
                net_info = f.readlines()[2:]
                #net_list = str(net_info).lower().split()
                #net_list = net_info.split()
                for num in net_info:
                    net_list=num.strip().split()
                    if net_list[0][0:-1] == net:
                        recv_1 = float(net_list[1])#获取接受字节数
                        send_1 = float(net_list[9])#获取发送字节数
            print("网卡名称%-20s  ip%-12s received%-8s  transmit%-10s "%('','','(kb/s)','(kb/s)'))
            #print("network_card: %-10s  ip: %-20s received: %-.3f Kb/s transmit: %-.3f kb/s" % (network_card,ip,(recv_2/1024 - recv_1/1024),(send_2/1024 - send_1/1024)))
            print("%-21s   %-22s %-.3f%13s  %-.3f " % (network_card,ip,(recv_1/1024),'',(send_1/1024)))

 
 
if __name__ == '__main__':
    #while True:
       # try:
            os.system('clear')
            sysinfo()
            print("********************************************************")
            cpuinfo()
            print("========================================================")
            meminfo()
            print("########################################################")
            diskinfo()
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            netinfo()
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            clusterstat()
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            cephstat()
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            clusterinfo()
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            cephinfo()
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            mysqlstat()
            #time.sleep(5)
        #except KeyboardInterrupt as e:
       #     print ('')
        #    print("Bye-Bye")
         #  sys.exit(0)
