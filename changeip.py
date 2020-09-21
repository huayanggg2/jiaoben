import subprocess
import wmi
import time

def test_ip_connection():
    url = 'www.baidu.com'#ping外网的地址
    num = 1 #ping次数
    ip = '172.16.26.65'#你第二个要判断的Ip地址
    wait = 2000 #延迟等待时间

    ping1 = subprocess.Popen("ping -n {} -w {} {}".format(num, wait, url), stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)  ## ping第一个url，这种方式，终端不会显示运行结果

    exit_code = ping1.wait() #ping “www.baidu.com” 的返回结果

    if exit_code != 0:#如果返回结果为0，则正常，否则无法ping通 www.baidu.com
        ping2 = subprocess.Popen("ping -n {} -w {} {}".format(num, wait, ip), stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)#ping第二个ip：172.16.26.65
        exit_code2 = ping2.wait()#ping “172.16.26.65” 的返回结果
        if exit_code2 != 0:#如果返回结果为0，则正常，否则无法ping通
            print("修改ip中...")
            colNicConfigs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)#获取系统网络适配器
            if len(colNicConfigs) < 1:
                print('没有找到可用的网络适配器')
                exit()

            objNicConfig = colNicConfigs[0]
            print(objNicConfig)
            arrIPAddresses = ['158.223.14.147']#需要替换的ip
            arrSubnetMasks = ['255.255.255.0']#子掩
            arrDefaultGateways = ['158.223.14.254']#网关
            arrGatewayCostMetrics = [1]
            intReboot = 0
            #替换ip和子掩
            returnValue = objNicConfig.EnableStatic(IPAddress = arrIPAddresses, SubnetMask = arrSubnetMasks)
            print(returnValue)
            if returnValue[0] == 0:#如果执行的返回值为0则提示成功
                print('设置IP成功')

            elif returnValue[0] == 1:#如果为1，则需要重启，intReboot+1
                print('设置IP成功')
                intReboot += 1
            else:
                print('修改IP失败: IP设置发生错误')
                exit()
            #设置网关
            returnValue = objNicConfig.SetGateways(DefaultIPGateway=arrDefaultGateways,
                                                   GatewayCostMetric=arrGatewayCostMetrics)
            if returnValue[0] == 0:
                print('设置网关成功')

            elif returnValue[0] == 1:
                print('设置网关成功')

                intReboot += 1
            else:
                print('修改IP失败: 网关设置发生错误')
                exit()
            if intReboot > 0:
                print('需要重新启动计算机')

            else:
                print('')

                print('修改后的配置为：')

                print('IP: ', ', '.join(objNicConfig.IPAddress))

                print('掩码: ', ', '.join(objNicConfig.IPSubnet))

                print('网关: ', ', '.join(objNicConfig.DefaultIPGateway))

                print('DNS: ', ', '.join(objNicConfig.DNSServerSearchOrder))

                print('修改IP结束')
        else:
            print("可以ping通 ip")
    else:
        print("可以Ping通百度")

while True:
    test_ip_connection()
    time.sleep(5)#5秒执行一次检查
