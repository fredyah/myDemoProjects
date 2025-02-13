from vCenterManager import VCenterOperations
from ESXIManager import ESXiOperations
import time
import argparse




parser = argparse.ArgumentParser( "VMWareShutDwonProcess" )  # https://stackoverflow.com/questions/4033723/how-do-i-access-command-line-arguments
parser.add_argument( "--vmWareType", dest = "vmWareType", help = "Accept 'vCenter', 'ESXI'", type = str, default = None, required = True )
parser.add_argument( "--method", dest = "method", help = "turnOn, turnOff", type = str, default = None, required = True )


args = parser.parse_args()
if args.vmWareType not in [ 'vCenter', 'ESXI' ]:
    print( "Argument '--vmWareType' error." )
    exit( 1 )



if args.vmWareType == 'vCenter' and args.method == "turnOff":

    vCenterIP = "192.168.1.20"
    vCenterUser = "admin@vsphere.me"
    pasS = "1123456"


    vcenter = VCenterOperations(
        host=vCenterIP,
        user=vCenterUser,
        passwd=pasS
    )


    ## 除了 vCenter VM, Host ，所有VM, ESXI host 關機
    try:
        # 連接到 vCenter
        vcenter.connect()
        
        ## VM 關機順序
        vm_TurnOFF_order = ['ingress-nginx', 'mars-summarizer', 'n-node-2-QAS', 'n-node-1-QAS', 'n-node-3', 'rancher-2.7.9', 'opensearch', 'db', 'db-mysql-8', 'redis-server', 'RollCall_Door', 'ubuntu-rke2-master-fred', 'ubuntu-clotho', 'mars-registry', 'gitlab', 'win10_SAN2', 'ffmpeg-convertor', 'ubunturancher-fred1', 'gitlab-runner-shared2', 'fred-win11', 'u22Desktop-200', 'gitlab-runner-256', 'ERP-server2012R2', 'win10(146)', 'ubuntu-rke2-worknode-fred', 'mars-odoo-erp', 'odoo-erp', 'win-11-joanne(27)', 'Peter-vm', 'win-11-clotho', 'ubuntu-22-server-template', 'u24-server-template', 'ubuntu-22-desktop-template-vm', 'logstash', 'james-wins', 'ubuntu-desktop-22-template', 'mars-access', 'rancher-test-m', 'marsun-didi-stress-testing', 'selenium-template-2024-4', 'macOS_sonova']
        #vm_TurnOFF_order = ['ffmpeg-convertor', 'Peter-vm', 'ubuntu-rke2-master-fred', 'ubuntu-rke2-worknode-fred', 'win10_SAN2']
        # 獲取所有 power on 的 VM 名稱
        vmList = [k for k, v in vcenter.get_vms_ips().items() if "vcenter" not in k.lower()]



        
        ## VM 關機順序
        for vmt in vm_TurnOFF_order:
            if vmt in vmList:
                vcenter.power_off_vm(vmt)
                vmList.remove(vmt)

        if len(vmList) != 0:
            for vmt in vmList:
                vcenter.power_off_vm(vmt)
        
        vmListCHK = [k for k, v in vcenter.get_vms_ips().items() if "vcenter" not in k.lower()]
        if len(vmListCHK) == 0:
            print("VM 已確認全部都關機完畢！！")
            esxiIPList = ['192.168.1.5', '192.168.1.5', '192.168.1.7']
            for eip in esxiIPList:
                vcenter.put_host_in_maintenance_mode(eip)
                time.sleep(20)
                vcenter.shutdown_host(eip)

        else:
            print("VM 沒有關機完全，請再確認")









    finally:
        # 斷開連接
        vcenter.disconnect()



elif args.vmWareType == 'ESXI' and args.method == "turnOff":

    ESXI_IP = "192.168.1.8"
    ESXI_User = "root"
    ESXI_Passwd = "1@3WaSd@mars"

    esxi_ops = ESXiOperations(
        host=ESXI_IP,
        user=ESXI_User,
        passwd=ESXI_Passwd
    )

    try:
        esxi_ops.connect()
        vmList  = esxi_ops.list_powered_on_vms()
        print(vmList)

        for vml in vmList:
            esxi_ops.power_off_vm(vml)

        vmList  = esxi_ops.list_powered_on_vms()

        if len(vmList) == 0:
            print("vcenter VM 已關閉，準備關機 ESXI HOST")
            esxi_ops.enter_maintenance_mode(ESXI_IP)
            esxi_ops.shutdown_host(ESXI_IP)
        else:
            print(f"發現尚有 VM 未關閉完成( {', '.join(vmList)} )，請手動進行關閉，再關機 ESXI HOST")



    finally:
        # 斷開連接
        esxi_ops.disconnect()
