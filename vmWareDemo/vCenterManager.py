from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import requests

class VCenterConnection:
    def __init__(self, host, user, passwd, ssl_context=None):
        """
        初始化 vCenter 連接信息
        """
        self.host = host
        self.user = user
        self.passwd = passwd
        self.ssl_context = ssl_context or ssl._create_unverified_context()
        self.si = None

    def connect(self):
        """
        連接到 vCenter
        """
        self.si = SmartConnect(
            host=self.host,
            user=self.user,
            pwd=self.passwd,
            sslContext=self.ssl_context
        )
        if self.si:
            print(f"Successfully connected to vCenter at {self.host}.")
        else:
            raise ConnectionError("Failed to connect to vCenter.")

    def disconnect(self):
        """
        斷開與 vCenter 的連接
        """
        if self.si:
            Disconnect(self.si)
            print("Disconnected from vCenter.")
        self.si = None

    def get_content(self):
        """
        獲取 vCenter 的內容對象
        """
        if self.si:
            return self.si.RetrieveContent()
        else:
            raise ConnectionError("Not connected to vCenter.")


class VCenterOperations(VCenterConnection):
    def __init__(self, host, user, passwd, ssl_context=None):
        super().__init__(host, user, passwd, ssl_context)

    def find_vm_by_name(self, vm_name):
        """
        根據名稱查找虛擬機
        """
        content = self.get_content()
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.VirtualMachine], True
        )
        for vm in container.view:
            if vm.name == vm_name:
                container.Destroy()
                return vm
        container.Destroy()
        return None

    def get_esxi_hosts(self):
        """
        檢索所有 ESXi 主機清單
        """
        content = self.get_content()
        container = content.viewManager.CreateContainerView(
            content.rootFolder, [vim.HostSystem], True
        )
        hosts = container.view
        container.Destroy()
        return hosts

    def get_vms_ips(self):
        """
        列出所有 VM 的名稱和 IP 地址
        """
        dicT = {}
        content = self.get_content()
        for datacenter in content.rootFolder.childEntity:
            if hasattr(datacenter, 'vmFolder'):
                vmFolder = datacenter.vmFolder
                vmList = vmFolder.childEntity
                for vm in vmList:
                    if isinstance(vm, vim.VirtualMachine):
                        if vm.runtime.powerState == "poweredOn":
                            print(f"VM Name: {vm.name}")
                            if vm.guest is not None and vm.guest.ipAddress:
                                print(f"IP Address: {vm.guest.ipAddress}\n")
                                dicT[vm.name] = vm.guest.ipAddress
                            else:
                                print("No IP Address assigned.")
                                dicT[vm.name] = "No IP Address assigned."
        return dicT

    def power_on_vm(self, vm_name):
        """
        開啟指定虛擬機的電源
        """
        vm = self.find_vm_by_name(vm_name)
        if not vm:
            print(f"VM {vm_name} not found.")
            return

        if vm.runtime.powerState == "poweredOn":
            print(f"{vm.name} is already powered on.")
        else:
            print(f"Powering on {vm.name}...")
            task = vm.PowerOn()
            self.wait_for_task(task)
            print(f"{vm.name} is now powered on.")

    def power_off_vm(self, vm_name):
        """
        關閉指定虛擬機的電源
        """
        vm = self.find_vm_by_name(vm_name)
        if not vm:
            print(f"VM {vm_name} not found.")
            return

        if vm.runtime.powerState == "poweredOff":
            print(f"{vm.name} is already powered off.")
            self.send_msg_to_discord(f"{vm.name} is already powered off.")
        else:
            print(f"Powering off {vm.name}...")
            self.send_msg_to_discord(f"Powering off {vm.name}...")
            task = vm.PowerOff()
            self.wait_for_task(task)
            print(f"{vm.name} is now powered off.")
            self.send_msg_to_discord(f"{vm.name} is now powered off.")




    def find_host_by_ip(self, ip):
        content = self.get_content()
        for datacenter in content.rootFolder.childEntity:
            if hasattr(datacenter, 'hostFolder'):
                host_folder = datacenter.hostFolder
                for cluster in host_folder.childEntity:
                    for host in cluster.host:
                        if host.name == ip:
                            return host
        return None

    def put_host_in_maintenance_mode(self, ip):
        host = self.find_host_by_ip(ip)
        print(f"Putting host {host.name} into maintenance mode...")
        self.send_msg_to_discord(f"Putting host {host.name} into maintenance mode...")
        task = host.EnterMaintenanceMode_Task(timeout=0)
        self.wait_for_task(task)
        print(f"Host {host.name} is now in maintenance mode.")
        self.send_msg_to_discord(f"Host {host.name} is now in maintenance mode.")

    def shutdown_host(self, ip):
        host = self.find_host_by_ip(ip)
        print(f"Shutting down host {host.name}...")
        self.send_msg_to_discord(f"Shutting down host {host.name}...")
        task = host.ShutdownHost_Task(force=True)
        self.wait_for_task(task)
        print(f"Host {host.name} is now shut down.")
        self.send_msg_to_discord(f"Host {host.name} is now shut down.")



























    def send_msg_to_discord(msg:str):
        token = "your discord bot token"
        message = msg
        channel_id = "your discord channel id"

        headers = {
            #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Authorization': f"Bot {token}",
            "Content-Type": "application/json"
        }

        json_data = {
            'content': message
        }

        response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=json_data)
        print(response)








    @staticmethod
    def wait_for_task(task):
        """
        等待任務完成
        """
        while task.info.state == "running":
            pass
        if task.info.state == "success":
            print("Task completed successfully.")
        else:
            print(f"Task failed: {task.info.error}")


















'''
import requests
import json


requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


class vCenterManager:

    __api_url = None
    __username = None
    __password = None
    __headers = None



    def __init__( self, useR: str, passWD: str, mainurL: str):
        self.__username = useR
        self.__password = passWD
        self.__api_url = mainurL
        self.__headers = self.get_session_id()
        



    def get_session_id(self):
 #       vcenter_url = self.__api_url
 #       username = self.__username
 #       password = self.__password
        

        # 登录 vCenter 并获取会话 ID
        login_url = f"{self.__api_url}/rest/com/vmware/cis/session"
        response = requests.post(login_url, auth=(self.__username, self.__password), verify=False)

        if response.status_code == 200:
            session_id = response.json()['value']
    #        print(f"Session ID: {session_id}")

            headers = {
                "vmware-api-session-id": session_id,
                'Content-Type': 'application/json'
            }

            return headers
        else:
            print(f"Failed to login: {response.status_code}")
            print(response.text)




    def get_hosts_info(self):

        host_url = f"{self.__api_url}/rest/vcenter/host"
        response = requests.get(host_url, headers=self.__headers, verify=False)

        if response.status_code == 200:
            return response.json()['value']


    def get_vm_info(self):

        host_url = f"{self.__api_url}/rest/vcenter/vm"
        response = requests.get(host_url, headers=self.__headers, verify=False)

        if response.status_code == 200:
            return response.json()


    def get_all_turnOnVM_list(self):
        vm_name_data = {}
        for vm in self.get_vm_info()['value']:
            if vm.get('power_state') == 'POWERED_ON':
                vm_name_data[vm.get('name')] = vm.get('vm')
        return vm_name_data
            



    def get_vm_status(self, vm_name):

        for vm in self.get_vm_info()['value']:
            vm_name_ = vm.get('name')
            if vm_name_ == vm_name:
                power_state = vm.get('power_state')
                vm_id = vm.get('vm')

                cpu_usage = self.get_vm_cpu_usage(vm_id)

                metrics_url = f"{self.__api_url}/rest/vcenter/vm/{vm_id}/hardware/cpu"
                cpu_response = requests.get(metrics_url, headers=self.__headers, verify=False)

                metrics_url = f"{self.__api_url}/rest/vcenter/vm/{vm_id}/hardware/memory"
                memory_response = requests.get(metrics_url, headers=self.__headers, verify=False)

                metrics_url = f"{self.__api_url}/rest/vcenter/vm/{vm_id}/hardware/disk"
                disk_response = requests.get(metrics_url, headers=self.__headers, verify=False)

                metrics_url = f"{self.__api_url}/rest/vcenter/vm/{vm_id}/guest"
                ip_response = requests.get(metrics_url, headers=self.__headers, verify=False)



                if cpu_response.status_code == 200 and memory_response.status_code == 200:
                    cpu_info = cpu_response.json()
                    memory_info = memory_response.json()
                    disk_info = disk_response.json()
                    ip_address = ip_response.json().get('ip_address')

                    # 取得 CPU 和記憶體使用率
                    cpu_cores = cpu_info.get('count', 'N/A')
                    memory_size = memory_info.get('size_MiB', 'N/A')

                    #print(f"VM: {vm_name}, Power State: {power_state}, CPU Cores: {cpu_cores}, Memory Size: {memory_size} MiB")
                    return power_state, vm_id, vm_name_, cpu_info, memory_info, disk_info, cpu_usage, ip_address
                else:
                    print(cpu_response.status_code)
                    print(memory_response.status_code)
                    print(f"Failed to retrieve CPU/Memory info for VM: {vm_name}")


    def get_vm_IP(self, vm_id):
        metrics_url = f"{self.__api_url}/rest/vcenter/vm/{vm_id}/guest"
        ip_response = requests.get(metrics_url, headers=self.__headers, verify=False)

        print(ip_response.status_code)
        if ip_response.status_code == 200:
            
            ip_address = ip_response.json().get('ip_address')
            return ip_address



    # 獲取 VM CPU 使用情況
    def get_vm_cpu_usage(self, vm_id):
        vm_perf_url = f"{self.__api_url}/rest/vcenter/vm/{vm_id}/hardware"
        response = requests.get(vm_perf_url, headers=self.__headers, verify=False)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get VM CPU usage: {response.text}")






    def log_out_vcenter(self):
        logout_url = f"{self.__api_url}/com/vmware/cis/session"
        requests.delete(logout_url, headers=self.__headers, verify=False)


    def turnOn_vm(self, vm_id: str):
        vm_start_url = f"{self.__api_url}/rest/vcenter/vm/{vm_id}/power/start"
        response = requests.post(vm_start_url, headers=self.__headers, verify=False)

        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Failed to get VM CPU usage: {response.text}")

    def turnOff_vm(self, vm_id: str):
        vm_stop_url = f"{self.__api_url}/rest/vcenter/vm/{vm_id}/power/stop"
        response = requests.post(vm_stop_url, headers=self.__headers, verify=False)

        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Failed to get VM CPU usage: {response.text}")
'''
